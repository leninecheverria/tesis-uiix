"""
Módulo de análisis de confiabilidad y validez de instrumentos.

Este módulo proporciona funciones para evaluar la confiabilidad y validez
del instrumento de medición (cuestionario/encuesta), siguiendo los lineamientos
de Hernández-Sampieri et al. (2014) en Metodología de la Investigación.

CONFIABILIDAD:
- Alpha de Cronbach (consistencia interna)
- Dos mitades (Split-half)
- KMO (Kaiser-Meyer-Olkin)
- Prueba de esfericidad de Bartlett

VALIDEZ:
- Validez de contenido (índice de acuerdo entre jueces)
- Validez de constructo (análisis factorial)
- Validez convergente y discriminante
- Validez de criterio (correlación con criterio externo)

Referencias:
Hernández-Sampieri, R., Fernández-Collado, C., & Baptista-Lucio, P. (2014).
Metodología de la investigación (6a ed.). McGraw-Hill Education.

Autor: Sistema de Análisis de Tesis
Fecha: Diciembre 2025
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import FactorAnalysis
from sklearn.model_selection import train_test_split
import logging
from typing import Dict, List, Tuple, Optional
import warnings

# Configurar logging
logger = logging.getLogger(__name__)
warnings.filterwarnings('ignore')


class ReliabilityAnalyzer:
    """
    Clase para análisis de confiabilidad y validez de instrumentos de medición.
    
    Implementa los métodos recomendados por Hernández-Sampieri et al. (2014)
    para investigación cuantitativa.
    
    Referencia:
    Hernández-Sampieri, R., Fernández-Collado, C., & Baptista-Lucio, P. (2014).
    Metodología de la investigación (6a ed.). McGraw-Hill Education.
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Inicializa el analizador de confiabilidad y validez.
        
        Args:
            data (pd.DataFrame): DataFrame con los datos a analizar
        """
        self.data = data
        self.results = {}
    
    def cronbach_alpha(self, items: List[str]) -> Dict:
        """
        Calcula el coeficiente Alpha de Cronbach para un conjunto de ítems.
        
        El Alpha de Cronbach mide la consistencia interna de un conjunto de ítems
        y es uno de los indicadores más utilizados para evaluar la fiabilidad
        de instrumentos de medición.
        
        Interpretación según Hernández-Sampieri et al. (2014):
        - α ≥ 0.90: Elevada (excelente)
        - α ≥ 0.80: Muy alta (buena)
        - α ≥ 0.70: Alta (aceptable para investigación)
        - α ≥ 0.60: Moderada (cuestionable)
        - α ≥ 0.50: Baja (pobre)
        - α < 0.50: Muy baja (inaceptable)
        
        Args:
            items (List[str]): Lista de nombres de columnas que forman la escala
            
        Returns:
            Dict: Diccionario con resultados del análisis
        """
        try:
            # Seleccionar solo los ítems especificados
            df_items = self.data[items].dropna()
            
            if len(df_items) == 0:
                logger.warning("No hay datos válidos para calcular Alpha de Cronbach")
                return None
            
            # Número de ítems
            n_items = len(items)
            
            # Varianza de cada ítem
            item_variances = df_items.var(axis=0, ddof=1)
            
            # Varianza total de la suma de ítems
            total_variance = df_items.sum(axis=1).var(ddof=1)
            
            # Fórmula del Alpha de Cronbach
            alpha = (n_items / (n_items - 1)) * (1 - item_variances.sum() / total_variance)
            
            # Interpretación
            interpretation = self._interpret_cronbach(alpha)
            
            # Calcular correlación item-total
            item_total_correlations = {}
            total_score = df_items.sum(axis=1)
            
            for item in items:
                # Correlación del ítem con el total (excluyendo el ítem)
                score_without_item = total_score - df_items[item]
                corr = df_items[item].corr(score_without_item)
                item_total_correlations[item] = corr
            
            # Calcular Alpha si se elimina cada ítem
            alpha_if_deleted = {}
            for item in items:
                remaining_items = [i for i in items if i != item]
                if len(remaining_items) > 1:
                    df_remaining = df_items[remaining_items]
                    n = len(remaining_items)
                    item_vars = df_remaining.var(axis=0, ddof=1)
                    total_var = df_remaining.sum(axis=1).var(ddof=1)
                    alpha_del = (n / (n - 1)) * (1 - item_vars.sum() / total_var)
                    alpha_if_deleted[item] = alpha_del
            
            result = {
                'alpha': alpha,
                'interpretation': interpretation,
                'n_items': n_items,
                'n_observations': len(df_items),
                'item_total_correlations': item_total_correlations,
                'alpha_if_item_deleted': alpha_if_deleted,
                'items': items,
                'mean_inter_item_correlation': df_items.corr().values[np.triu_indices_from(df_items.corr().values, k=1)].mean()
            }
            
            logger.info(f"✓ Alpha de Cronbach calculado: {alpha:.4f} ({interpretation})")
            
            return result
            
        except Exception as e:
            logger.error(f"✗ Error al calcular Alpha de Cronbach: {str(e)}")
            return None
    
    def kmo_test(self, items: List[str]) -> Dict:
        """
        Realiza la prueba KMO (Kaiser-Meyer-Olkin) para evaluar la adecuación
        muestral para análisis factorial.
        
        El KMO mide la proporción de varianza que podría ser causada por
        factores subyacentes. Valores cercanos a 1 indican que el análisis
        factorial es apropiado.
        
        Interpretación:
        - KMO ≥ 0.90: Maravilloso
        - KMO ≥ 0.80: Meritorio
        - KMO ≥ 0.70: Mediano
        - KMO ≥ 0.60: Mediocre
        - KMO ≥ 0.50: Miserable
        - KMO < 0.50: Inaceptable
        
        Args:
            items (List[str]): Lista de nombres de columnas
            
        Returns:
            Dict: Resultados de la prueba KMO
        """
        try:
            # Seleccionar datos y eliminar valores faltantes
            df_items = self.data[items].dropna()
            
            # Estandarizar los datos
            scaler = StandardScaler()
            data_scaled = scaler.fit_transform(df_items)
            
            # Matriz de correlación
            corr_matrix = np.corrcoef(data_scaled.T)
            
            # Matriz de correlación parcial (inversa de la matriz de correlación)
            corr_inv = np.linalg.inv(corr_matrix)
            
            # Calcular KMO
            n_vars = len(items)
            kmo_per_variable = np.zeros(n_vars)
            
            for i in range(n_vars):
                # Suma de correlaciones al cuadrado
                sum_sq_corr = np.sum(corr_matrix[i, :] ** 2) - 1  # -1 para excluir diagonal
                
                # Suma de correlaciones parciales al cuadrado
                sum_sq_partial = 0
                for j in range(n_vars):
                    if i != j:
                        partial_corr = -corr_inv[i, j] / np.sqrt(corr_inv[i, i] * corr_inv[j, j])
                        sum_sq_partial += partial_corr ** 2
                
                # KMO para la variable i
                kmo_per_variable[i] = sum_sq_corr / (sum_sq_corr + sum_sq_partial)
            
            # KMO global (media de los KMO individuales)
            kmo_global = np.mean(kmo_per_variable)
            
            # Interpretación
            interpretation = self._interpret_kmo(kmo_global)
            
            result = {
                'kmo_global': kmo_global,
                'interpretation': interpretation,
                'kmo_per_variable': dict(zip(items, kmo_per_variable)),
                'n_variables': n_vars,
                'n_observations': len(df_items)
            }
            
            logger.info(f"✓ KMO calculado: {kmo_global:.4f} ({interpretation})")
            
            return result
            
        except Exception as e:
            logger.error(f"✗ Error al calcular KMO: {str(e)}")
            return None
    
    def bartlett_test(self, items: List[str]) -> Dict:
        """
        Realiza la prueba de esfericidad de Bartlett.
        
        Esta prueba evalúa si la matriz de correlación es significativamente
        diferente de una matriz identidad. Un p-valor < 0.05 indica que
        las variables están lo suficientemente correlacionadas para
        realizar un análisis factorial.
        
        H0: La matriz de correlación es una matriz identidad
        H1: La matriz de correlación NO es una matriz identidad
        
        Args:
            items (List[str]): Lista de nombres de columnas
            
        Returns:
            Dict: Resultados de la prueba de Bartlett
        """
        try:
            # Seleccionar datos y eliminar valores faltantes
            df_items = self.data[items].dropna()
            n = len(df_items)
            p = len(items)
            
            # Matriz de correlación
            corr_matrix = df_items.corr()
            
            # Determinante de la matriz de correlación
            det_corr = np.linalg.det(corr_matrix)
            
            # Estadístico de Bartlett
            chi_square = -((n - 1) - (2 * p + 5) / 6) * np.log(det_corr)
            
            # Grados de libertad
            df = p * (p - 1) / 2
            
            # Valor p
            p_value = 1 - stats.chi2.cdf(chi_square, df)
            
            # Interpretación
            if p_value < 0.05:
                interpretation = "Rechazar H0: Las variables están correlacionadas (apropiado para análisis factorial)"
                suitable = True
            else:
                interpretation = "No rechazar H0: Las variables NO están suficientemente correlacionadas"
                suitable = False
            
            result = {
                'chi_square': chi_square,
                'degrees_of_freedom': int(df),
                'p_value': p_value,
                'interpretation': interpretation,
                'suitable_for_factor_analysis': suitable,
                'n_variables': p,
                'n_observations': n
            }
            
            logger.info(f"✓ Prueba de Bartlett: χ² = {chi_square:.4f}, p = {p_value:.4f}")
            
            return result
            
        except Exception as e:
            logger.error(f"✗ Error en prueba de Bartlett: {str(e)}")
            return None
    
    def comprehensive_reliability_validity(self, dimensions: Dict[str, List[str]], 
                                           include_validity: bool = True,
                                           criterion_variable: str = None) -> Dict:
        """
        Análisis completo de confiabilidad y validez del instrumento.
        
        Basado en la metodología de Hernández-Sampieri et al. (2014).
        
        Args:
            dimensions (Dict[str, List[str]]): Diccionario {nombre_dimension: [items]}
            include_validity (bool): Si True, incluye análisis de validez
            criterion_variable (str): Variable criterio para validez de criterio
            
        Returns:
            Dict: Resultados completos de confiabilidad y validez
        """
        logger.info("=" * 80)
        logger.info("ANÁLISIS COMPLETO DE CONFIABILIDAD Y VALIDEZ DEL INSTRUMENTO")
        logger.info("Metodología: Hernández-Sampieri et al. (2014)")
        logger.info("=" * 80)
        
        results = {
            'general': {},
            'by_dimension': {},
            'validity': {}
        }
        
        # =============== ANÁLISIS DE CONFIABILIDAD ===============
        logger.info("\n" + "=" * 60)
        logger.info("1. ANÁLISIS DE CONFIABILIDAD")
        logger.info("=" * 60)
        
        # Análisis por dimensión
        for dim_name, items in dimensions.items():
            logger.info(f"\n📊 Dimensión: {dim_name}")
            logger.info(f"   Ítems: {len(items)}")
            
            dim_results = {}
            
            # Alpha de Cronbach
            alpha_result = self.cronbach_alpha(items)
            if alpha_result:
                dim_results['cronbach_alpha'] = alpha_result
            
            # Dos mitades
            split_result = self.split_half_reliability(items)
            if split_result:
                dim_results['split_half'] = split_result
            
            # Prueba KMO
            if len(items) >= 3:
                kmo_result = self.kmo_test(items)
                if kmo_result:
                    dim_results['kmo'] = kmo_result
            
            # Prueba de Bartlett
            if len(items) >= 3:
                bartlett_result = self.bartlett_test(items)
                if bartlett_result:
                    dim_results['bartlett'] = bartlett_result
            
            results['by_dimension'][dim_name] = dim_results
        
        # Análisis general (todos los ítems)
        all_items = [item for items in dimensions.values() for item in items]
        logger.info(f"\n📊 ANÁLISIS GENERAL DEL INSTRUMENTO")
        logger.info(f"   Total de ítems: {len(all_items)}")
        
        results['general']['cronbach_alpha'] = self.cronbach_alpha(all_items)
        results['general']['split_half'] = self.split_half_reliability(all_items)
        results['general']['kmo'] = self.kmo_test(all_items)
        results['general']['bartlett'] = self.bartlett_test(all_items)
        
        # =============== ANÁLISIS DE VALIDEZ ===============
        if include_validity:
            logger.info("\n" + "=" * 60)
            logger.info("2. ANÁLISIS DE VALIDEZ")
            logger.info("=" * 60)
            
            # Validez de constructo (análisis factorial por dimensión)
            logger.info("\n📐 VALIDEZ DE CONSTRUCTO (Análisis Factorial)")
            for dim_name, items in dimensions.items():
                if len(items) >= 3:  # Mínimo 3 ítems para análisis factorial
                    logger.info(f"\n   Dimensión: {dim_name}")
                    factorial_result = self.construct_validity_factorial(items)
                    if factorial_result:
                        results['validity'][f'{dim_name}_factorial'] = factorial_result
            
            # Validez convergente (dentro de cada dimensión)
            logger.info("\n🔗 VALIDEZ CONVERGENTE")
            for dim_name, items in dimensions.items():
                if len(items) >= 2:
                    logger.info(f"\n   Dimensión: {dim_name}")
                    convergent_result = self.convergent_validity(items)
                    if convergent_result:
                        results['validity'][f'{dim_name}_convergent'] = convergent_result
            
            # Validez discriminante (entre dimensiones)
            logger.info("\n⚡ VALIDEZ DISCRIMINANTE")
            dim_names = list(dimensions.keys())
            if len(dim_names) >= 2:
                # Comparar primeras dos dimensiones como ejemplo
                dim1, dim2 = dim_names[0], dim_names[1]
                logger.info(f"\n   Entre: {dim1} y {dim2}")
                discriminant_result = self.discriminant_validity(
                    dimensions[dim1], 
                    dimensions[dim2]
                )
                if discriminant_result:
                    results['validity']['discriminant'] = discriminant_result
            
            # Validez de criterio (si se proporciona variable criterio)
            if criterion_variable and criterion_variable in self.data.columns:
                logger.info(f"\n🎯 VALIDEZ DE CRITERIO (criterio: {criterion_variable})")
                criterion_result = self.criterion_validity(all_items, criterion_variable)
                if criterion_result:
                    results['validity']['criterion'] = criterion_result
        
        logger.info("\n" + "=" * 80)
        logger.info("✓ ANÁLISIS DE CONFIABILIDAD Y VALIDEZ COMPLETADO")
        logger.info("=" * 80)
        
        return results
    
    def comprehensive_reliability(self, dimensions: Dict[str, List[str]]) -> Dict:
        """
        Análisis completo de confiabilidad (método legacy para compatibilidad).
        
        Nota: Se recomienda usar comprehensive_reliability_validity()
        para análisis completo según Hernández-Sampieri.
        
        Args:
            dimensions (Dict[str, List[str]]): Diccionario {nombre_dimension: [items]}
                
        Returns:
            Dict: Resultados de confiabilidad por dimensión
        """
        return self.comprehensive_reliability_validity(
            dimensions, 
            include_validity=False
        )
    
    def split_half_reliability(self, items: List[str]) -> Dict:
        """
        Calcula la confiabilidad por dos mitades (split-half).
        
        Método recomendado por Hernández-Sampieri et al. (2014) como
        complemento al Alpha de Cronbach.
        
        Args:
            items (List[str]): Lista de nombres de columnas
            
        Returns:
            Dict: Resultados del análisis de dos mitades
        """
        try:
            df_items = self.data[items].dropna()
            
            # Dividir ítems en dos mitades
            mid = len(items) // 2
            first_half = items[:mid]
            second_half = items[mid:]
            
            # Sumar puntajes de cada mitad
            score_half1 = df_items[first_half].sum(axis=1)
            score_half2 = df_items[second_half].sum(axis=1)
            
            # Correlación entre mitades
            r = score_half1.corr(score_half2)
            
            # Corrección de Spearman-Brown
            reliability = (2 * r) / (1 + r)
            
            result = {
                'correlation_halves': r,
                'spearman_brown_coefficient': reliability,
                'first_half_items': first_half,
                'second_half_items': second_half,
                'n_observations': len(df_items),
                'interpretation': self._interpret_cronbach(reliability)
            }
            
            logger.info(f"✓ Confiabilidad dos mitades: {reliability:.4f}")
            
            return result
            
        except Exception as e:
            logger.error(f"✗ Error en análisis de dos mitades: {str(e)}")
            return None
    
    def content_validity_index(self, judges_ratings: pd.DataFrame) -> Dict:
        """
        Calcula el Índice de Validez de Contenido (IVC).
        
        Validez de contenido: evalúa si el instrumento mide adecuadamente
        el dominio de contenido que se pretende medir (Hernández-Sampieri, 2014).
        
        Args:
            judges_ratings (pd.DataFrame): Matriz donde filas=ítems, columnas=jueces,
                valores=calificación de relevancia (ej: 1-4 donde 3-4=relevante)
            
        Returns:
            Dict: Índices de validez de contenido
        """
        try:
            n_judges = len(judges_ratings.columns)
            n_items = len(judges_ratings)
            
            # Calcular IVC por ítem (proporción de jueces que califican como relevante)
            # Asumimos que valores ≥3 son relevantes (escala 1-4)
            relevant_threshold = 3
            ivc_items = {}
            
            for item in judges_ratings.index:
                n_relevant = (judges_ratings.loc[item] >= relevant_threshold).sum()
                ivc_item = n_relevant / n_judges
                ivc_items[item] = ivc_item
            
            # IVC total (promedio de IVC de ítems)
            ivc_total = np.mean(list(ivc_items.values()))
            
            # Interpretación según Hernández-Sampieri
            if ivc_total >= 0.80:
                interpretation = "Excelente validez de contenido"
            elif ivc_total >= 0.70:
                interpretation = "Buena validez de contenido"
            elif ivc_total >= 0.60:
                interpretation = "Validez de contenido aceptable"
            else:
                interpretation = "Validez de contenido insuficiente - revisar ítems"
            
            result = {
                'ivc_total': ivc_total,
                'ivc_by_item': ivc_items,
                'n_judges': n_judges,
                'n_items': n_items,
                'interpretation': interpretation
            }
            
            logger.info(f"✓ IVC calculado: {ivc_total:.4f} ({interpretation})")
            
            return result
            
        except Exception as e:
            logger.error(f"✗ Error en validez de contenido: {str(e)}")
            return None
    
    def construct_validity_factorial(self, items: List[str], 
                                     n_factors: int = None) -> Dict:
        """
        Evalúa la validez de constructo mediante Análisis Factorial Exploratorio.
        
        Validez de constructo: evalúa si el instrumento mide el constructo
        teórico que pretende medir (Hernández-Sampieri, 2014).
        
        Args:
            items (List[str]): Lista de ítems
            n_factors (int): Número de factores a extraer (None=automático)
            
        Returns:
            Dict: Resultados del análisis factorial
        """
        try:
            df_items = self.data[items].dropna()
            
            # Estandarizar datos
            scaler = StandardScaler()
            data_scaled = scaler.fit_transform(df_items)
            
            # Si no se especifica, usar criterio de autovalores >1
            if n_factors is None:
                # Calcular matriz de correlación y autovalores
                corr_matrix = np.corrcoef(data_scaled.T)
                eigenvalues = np.linalg.eigvals(corr_matrix)
                n_factors = np.sum(eigenvalues > 1)
                logger.info(f"  Factores con autovalor >1: {n_factors}")
            
            # Análisis factorial
            fa = FactorAnalysis(n_components=n_factors, random_state=42)
            fa.fit(data_scaled)
            
            # Cargas factoriales
            loadings = pd.DataFrame(
                fa.components_.T,
                columns=[f'Factor_{i+1}' for i in range(n_factors)],
                index=items
            )
            
            # Varianza explicada por factor
            explained_variance = np.var(fa.transform(data_scaled), axis=0)
            explained_variance_ratio = explained_variance / explained_variance.sum()
            
            result = {
                'n_factors': n_factors,
                'factor_loadings': loadings,
                'explained_variance_ratio': explained_variance_ratio,
                'total_variance_explained': explained_variance_ratio.sum(),
                'eigenvalues': eigenvalues if n_factors is None else None
            }
            
            logger.info(f"✓ Análisis factorial: {n_factors} factores, "
                       f"{explained_variance_ratio.sum()*100:.1f}% varianza explicada")
            
            return result
            
        except Exception as e:
            logger.error(f"✗ Error en análisis factorial: {str(e)}")
            return None
    
    def convergent_validity(self, items_dimension: List[str]) -> Dict:
        """
        Evalúa la validez convergente dentro de una dimensión.
        
        Validez convergente: los ítems que miden el mismo constructo
        deben correlacionar significativamente entre sí (Hernández-Sampieri, 2014).
        
        Args:
            items_dimension (List[str]): Ítems de una dimensión
            
        Returns:
            Dict: Resultados de validez convergente
        """
        try:
            df_items = self.data[items_dimension].dropna()
            
            # Matriz de correlación entre ítems
            corr_matrix = df_items.corr()
            
            # Obtener correlaciones (triángulo superior, sin diagonal)
            correlations = []
            n_items = len(items_dimension)
            for i in range(n_items):
                for j in range(i+1, n_items):
                    correlations.append(corr_matrix.iloc[i, j])
            
            # Estadísticas
            mean_corr = np.mean(correlations)
            min_corr = np.min(correlations)
            max_corr = np.max(correlations)
            
            # Interpretación según Hernández-Sampieri
            # Correlaciones moderadas a altas indican buena validez convergente
            if mean_corr >= 0.50:
                interpretation = "Excelente validez convergente"
            elif mean_corr >= 0.30:
                interpretation = "Buena validez convergente"
            elif mean_corr >= 0.20:
                interpretation = "Validez convergente aceptable"
            else:
                interpretation = "Validez convergente insuficiente"
            
            result = {
                'mean_correlation': mean_corr,
                'min_correlation': min_corr,
                'max_correlation': max_corr,
                'correlation_matrix': corr_matrix,
                'n_correlations': len(correlations),
                'interpretation': interpretation
            }
            
            logger.info(f"✓ Validez convergente: r_media = {mean_corr:.3f} ({interpretation})")
            
            return result
            
        except Exception as e:
            logger.error(f"✗ Error en validez convergente: {str(e)}")
            return None
    
    def discriminant_validity(self, dimension1_items: List[str], 
                             dimension2_items: List[str]) -> Dict:
        """
        Evalúa la validez discriminante entre dos dimensiones.
        
        Validez discriminante: ítems de diferentes constructos deben
        correlacionar menos entre sí que los ítems del mismo constructo
        (Hernández-Sampieri, 2014).
        
        Args:
            dimension1_items (List[str]): Ítems de la primera dimensión
            dimension2_items (List[str]): Ítems de la segunda dimensión
            
        Returns:
            Dict: Resultados de validez discriminante
        """
        try:
            df_dim1 = self.data[dimension1_items].dropna()
            df_dim2 = self.data[dimension2_items].dropna()
            
            # Puntajes totales por dimensión
            score_dim1 = df_dim1.sum(axis=1)
            score_dim2 = df_dim2.sum(axis=1)
            
            # Alinear índices
            common_idx = score_dim1.index.intersection(score_dim2.index)
            score_dim1 = score_dim1.loc[common_idx]
            score_dim2 = score_dim2.loc[common_idx]
            
            # Correlación entre dimensiones
            corr_between = score_dim1.corr(score_dim2)
            
            # Interpretación según Hernández-Sampieri
            # Correlación baja indica buena validez discriminante
            if abs(corr_between) < 0.30:
                interpretation = "Excelente validez discriminante"
            elif abs(corr_between) < 0.50:
                interpretation = "Buena validez discriminante"
            elif abs(corr_between) < 0.70:
                interpretation = "Validez discriminante moderada"
            else:
                interpretation = "Validez discriminante insuficiente (dimensiones muy relacionadas)"
            
            result = {
                'correlation_between_dimensions': corr_between,
                'dimension1_items': dimension1_items,
                'dimension2_items': dimension2_items,
                'n_observations': len(common_idx),
                'interpretation': interpretation
            }
            
            logger.info(f"✓ Validez discriminante: r = {corr_between:.3f} ({interpretation})")
            
            return result
            
        except Exception as e:
            logger.error(f"✗ Error en validez discriminante: {str(e)}")
            return None
    
    def criterion_validity(self, predictor_items: List[str], 
                          criterion_var: str) -> Dict:
        """
        Evalúa la validez de criterio (predictiva o concurrente).
        
        Validez de criterio: evalúa si el instrumento se relaciona con
        un criterio externo conocido (Hernández-Sampieri, 2014).
        
        Args:
            predictor_items (List[str]): Ítems del instrumento
            criterion_var (str): Variable criterio externa
            
        Returns:
            Dict: Resultados de validez de criterio
        """
        try:
            df_pred = self.data[predictor_items].dropna()
            criterion = self.data[criterion_var].dropna()
            
            # Puntaje total del instrumento
            score_predictor = df_pred.sum(axis=1)
            
            # Alinear índices
            common_idx = score_predictor.index.intersection(criterion.index)
            score_predictor = score_predictor.loc[common_idx]
            criterion = criterion.loc[common_idx]
            
            # Correlación con criterio
            corr_criterion = score_predictor.corr(criterion)
            
            # Prueba de significancia
            n = len(common_idx)
            t_stat = corr_criterion * np.sqrt((n - 2) / (1 - corr_criterion**2))
            p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n - 2))
            
            # Interpretación según Hernández-Sampieri
            if abs(corr_criterion) >= 0.50 and p_value < 0.01:
                interpretation = "Excelente validez de criterio"
            elif abs(corr_criterion) >= 0.30 and p_value < 0.05:
                interpretation = "Buena validez de criterio"
            elif p_value < 0.05:
                interpretation = "Validez de criterio aceptable"
            else:
                interpretation = "Validez de criterio insuficiente (no significativa)"
            
            result = {
                'correlation_with_criterion': corr_criterion,
                'p_value': p_value,
                'significant': p_value < 0.05,
                'criterion_variable': criterion_var,
                'n_observations': n,
                'interpretation': interpretation
            }
            
            logger.info(f"✓ Validez de criterio: r = {corr_criterion:.3f}, p = {p_value:.4f}")
            
            return result
            
        except Exception as e:
            logger.error(f"✗ Error en validez de criterio: {str(e)}")
            return None
    
    def _interpret_cronbach(self, alpha: float) -> str:
        """
        Interpreta el valor del Alpha de Cronbach según Hernández-Sampieri.
        
        Referencia:
        Hernández-Sampieri, R. et al. (2014). Metodología de la investigación (6a ed.).
        """
        if alpha >= 0.90:
            return "Elevada (Excelente)"
        elif alpha >= 0.80:
            return "Muy alta (Buena)"
        elif alpha >= 0.70:
            return "Alta (Aceptable)"
        elif alpha >= 0.60:
            return "Moderada (Cuestionable)"
        elif alpha >= 0.50:
            return "Baja (Pobre)"
        else:
            return "Muy baja (Inaceptable)"
    
    def _interpret_kmo(self, kmo: float) -> str:
        """Interpreta el valor del KMO."""
        if kmo >= 0.90:
            return "Maravilloso"
        elif kmo >= 0.80:
            return "Meritorio"
        elif kmo >= 0.70:
            return "Mediano"
        elif kmo >= 0.60:
            return "Mediocre"
        elif kmo >= 0.50:
            return "Miserable"
        else:
            return "Inaceptable"


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def quick_cronbach_alpha(data: pd.DataFrame, items: List[str]) -> float:
    """
    Función rápida para calcular solo el valor del Alpha de Cronbach.
    
    Args:
        data (pd.DataFrame): DataFrame con los datos
        items (List[str]): Lista de ítems
        
    Returns:
        float: Valor del Alpha de Cronbach
    """
    analyzer = ReliabilityAnalyzer(data)
    result = analyzer.cronbach_alpha(items)
    return result['alpha'] if result else None


def analyze_all_reliability(data: pd.DataFrame, dimensions: Dict[str, List[str]]) -> Dict:
    """
    Función rápida para análisis completo de fiabilidad.
    
    Args:
        data (pd.DataFrame): DataFrame con los datos
        dimensions (Dict): Diccionario de dimensiones e ítems
        
    Returns:
        Dict: Resultados completos
    """
    analyzer = ReliabilityAnalyzer(data)
    return analyzer.comprehensive_reliability(dimensions)
