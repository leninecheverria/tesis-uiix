"""
Módulo de estadística descriptiva para análisis de datos de encuestas.

Este módulo proporciona funciones para realizar análisis estadísticos
descriptivos completos, incluyendo medidas de tendencia central,
dispersión, distribución y tablas de frecuencias.

Autor: Sistema de Análisis de Tesis
Fecha: Diciembre 2025
"""

import pandas as pd
import numpy as np
from scipy import stats
import logging
from typing import Dict, List, Optional, Union

# Configurar logging
logger = logging.getLogger(__name__)


class DescriptiveAnalyzer:
    """
    Clase para análisis estadístico descriptivo de datos.
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Inicializa el analizador descriptivo.
        
        Args:
            data (pd.DataFrame): DataFrame con los datos a analizar
        """
        self.data = data
    
    def basic_statistics(self, variables: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Calcula estadísticas descriptivas básicas para variables numéricas.
        
        Incluye: media, mediana, moda, desviación estándar, varianza,
        mínimo, máximo, rango, percentiles, asimetría y curtosis.
        
        Args:
            variables (List[str], optional): Lista de variables a analizar.
                Si es None, analiza todas las variables numéricas.
                
        Returns:
            pd.DataFrame: Tabla con estadísticas descriptivas
        """
        # Seleccionar variables numéricas
        if variables is None:
            df_numeric = self.data.select_dtypes(include=[np.number])
        else:
            df_numeric = self.data[variables].select_dtypes(include=[np.number])
        
        if df_numeric.empty:
            logger.warning("No hay variables numéricas para analizar")
            return None
        
        # Calcular estadísticas
        stats_dict = {}
        
        for col in df_numeric.columns:
            serie = df_numeric[col].dropna()
            
            if len(serie) == 0:
                continue
            
            stats_dict[col] = {
                'N': len(serie),
                'N_perdidos': self.data[col].isnull().sum(),
                'Media': serie.mean(),
                'Mediana': serie.median(),
                'Moda': serie.mode()[0] if len(serie.mode()) > 0 else np.nan,
                'Desv_Std': serie.std(),
                'Varianza': serie.var(),
                'Mínimo': serie.min(),
                'Máximo': serie.max(),
                'Rango': serie.max() - serie.min(),
                'Q1': serie.quantile(0.25),
                'Q3': serie.quantile(0.75),
                'IQR': serie.quantile(0.75) - serie.quantile(0.25),
                'Asimetría': serie.skew(),
                'Curtosis': serie.kurtosis(),
                'Error_Std': serie.sem(),
            }
        
        # Convertir a DataFrame
        stats_df = pd.DataFrame(stats_dict).T
        
        logger.info(f"✓ Estadísticas descriptivas calculadas para {len(stats_df)} variables")
        
        return stats_df
    
    def frequency_table(self, variable: str, sort_by: str = 'frequency') -> pd.DataFrame:
        """
        Genera tabla de frecuencias para una variable.
        
        Args:
            variable (str): Nombre de la variable
            sort_by (str): Criterio de ordenamiento ('frequency' o 'value')
            
        Returns:
            pd.DataFrame: Tabla de frecuencias
        """
        if variable not in self.data.columns:
            logger.error(f"Variable '{variable}' no encontrada")
            return None
        
        # Calcular frecuencias
        freq_counts = self.data[variable].value_counts()
        freq_percent = self.data[variable].value_counts(normalize=True) * 100
        
        # Frecuencias acumuladas
        if sort_by == 'value':
            freq_counts = freq_counts.sort_index()
            freq_percent = freq_percent.sort_index()
        
        freq_cumsum = freq_counts.cumsum()
        freq_percent_cumsum = freq_percent.cumsum()
        
        # Crear tabla
        freq_table = pd.DataFrame({
            'Valor': freq_counts.index,
            'Frecuencia': freq_counts.values,
            'Porcentaje': freq_percent.values,
            'Frec_Acumulada': freq_cumsum.values,
            'Porc_Acumulado': freq_percent_cumsum.values,
        })
        
        # Agregar fila de totales
        total_row = pd.DataFrame({
            'Valor': ['TOTAL'],
            'Frecuencia': [freq_counts.sum()],
            'Porcentaje': [100.0],
            'Frec_Acumulada': [''],
            'Porc_Acumulado': [''],
        })
        
        freq_table = pd.concat([freq_table, total_row], ignore_index=True)
        
        logger.info(f"✓ Tabla de frecuencias generada para '{variable}'")
        
        return freq_table
    
    def grouped_statistics(self, 
                          numeric_var: str, 
                          group_var: str) -> pd.DataFrame:
        """
        Calcula estadísticas descriptivas agrupadas por una variable categórica.
        
        Args:
            numeric_var (str): Variable numérica a analizar
            group_var (str): Variable categórica para agrupar
            
        Returns:
            pd.DataFrame: Estadísticas por grupo
        """
        if numeric_var not in self.data.columns or group_var not in self.data.columns:
            logger.error("Una o ambas variables no encontradas")
            return None
        
        # Agrupar y calcular estadísticas
        grouped = self.data.groupby(group_var)[numeric_var].agg([
            ('N', 'count'),
            ('Media', 'mean'),
            ('Mediana', 'median'),
            ('Desv_Std', 'std'),
            ('Mínimo', 'min'),
            ('Máximo', 'max'),
            ('Q1', lambda x: x.quantile(0.25)),
            ('Q3', lambda x: x.quantile(0.75)),
        ]).reset_index()
        
        logger.info(f"✓ Estadísticas agrupadas calculadas: {numeric_var} por {group_var}")
        
        return grouped
    
    def correlation_matrix(self, 
                          variables: Optional[List[str]] = None,
                          method: str = 'pearson') -> pd.DataFrame:
        """
        Calcula matriz de correlación entre variables.
        
        Args:
            variables (List[str], optional): Variables a correlacionar
            method (str): Método de correlación ('pearson', 'spearman', 'kendall')
            
        Returns:
            pd.DataFrame: Matriz de correlación
        """
        # Seleccionar variables
        if variables is None:
            df_numeric = self.data.select_dtypes(include=[np.number])
        else:
            df_numeric = self.data[variables]
        
        # Calcular correlaciones
        corr_matrix = df_numeric.corr(method=method)
        
        logger.info(f"✓ Matriz de correlación calculada (método: {method})")
        
        return corr_matrix
    
    def normality_tests(self, variables: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Realiza pruebas de normalidad (Shapiro-Wilk y Kolmogorov-Smirnov).
        
        Args:
            variables (List[str], optional): Variables a probar
            
        Returns:
            pd.DataFrame: Resultados de las pruebas
        """
        # Seleccionar variables numéricas
        if variables is None:
            df_numeric = self.data.select_dtypes(include=[np.number])
        else:
            df_numeric = self.data[variables]
        
        results = {}
        
        for col in df_numeric.columns:
            serie = df_numeric[col].dropna()
            
            if len(serie) < 3:
                continue
            
            # Shapiro-Wilk (mejor para n < 5000)
            if len(serie) <= 5000:
                shapiro_stat, shapiro_p = stats.shapiro(serie)
            else:
                shapiro_stat, shapiro_p = np.nan, np.nan
            
            # Kolmogorov-Smirnov
            ks_stat, ks_p = stats.kstest(serie, 'norm', 
                                         args=(serie.mean(), serie.std()))
            
            results[col] = {
                'N': len(serie),
                'Shapiro_W': shapiro_stat,
                'Shapiro_p': shapiro_p,
                'Shapiro_Normal': 'Sí' if shapiro_p > 0.05 else 'No',
                'KS_D': ks_stat,
                'KS_p': ks_p,
                'KS_Normal': 'Sí' if ks_p > 0.05 else 'No',
            }
        
        results_df = pd.DataFrame(results).T
        
        logger.info(f"✓ Pruebas de normalidad completadas para {len(results_df)} variables")
        
        return results_df
    
    def outliers_detection(self, 
                          variables: Optional[List[str]] = None,
                          method: str = 'iqr') -> Dict:
        """
        Detecta valores atípicos (outliers) en las variables.
        
        Args:
            variables (List[str], optional): Variables a analizar
            method (str): Método de detección ('iqr', 'zscore')
            
        Returns:
            Dict: Diccionario con outliers por variable
        """
        # Seleccionar variables numéricas
        if variables is None:
            df_numeric = self.data.select_dtypes(include=[np.number])
        else:
            df_numeric = self.data[variables]
        
        outliers = {}
        
        for col in df_numeric.columns:
            serie = df_numeric[col].dropna()
            
            if method == 'iqr':
                # Método IQR (Rango Intercuartílico)
                Q1 = serie.quantile(0.25)
                Q3 = serie.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers_mask = (serie < lower_bound) | (serie > upper_bound)
                
            elif method == 'zscore':
                # Método Z-Score
                z_scores = np.abs(stats.zscore(serie))
                outliers_mask = z_scores > 3
            
            outliers[col] = {
                'n_outliers': outliers_mask.sum(),
                'percent_outliers': (outliers_mask.sum() / len(serie) * 100),
                'outlier_values': serie[outliers_mask].tolist() if outliers_mask.sum() > 0 else []
            }
        
        logger.info(f"✓ Detección de outliers completada (método: {method})")
        
        return outliers
    
    def summary_report(self, variables: Optional[List[str]] = None) -> Dict:
        """
        Genera un reporte completo con todas las estadísticas descriptivas.
        
        Args:
            variables (List[str], optional): Variables a incluir en el reporte
            
        Returns:
            Dict: Diccionario con todos los análisis
        """
        logger.info("="*70)
        logger.info("GENERANDO REPORTE ESTADÍSTICO DESCRIPTIVO COMPLETO")
        logger.info("="*70)
        
        report = {}
        
        # Estadísticas básicas
        logger.info("\n1. Calculando estadísticas básicas...")
        report['basic_statistics'] = self.basic_statistics(variables)
        
        # Matriz de correlación
        logger.info("2. Calculando matriz de correlación...")
        report['correlation_matrix'] = self.correlation_matrix(variables)
        
        # Pruebas de normalidad
        logger.info("3. Realizando pruebas de normalidad...")
        report['normality_tests'] = self.normality_tests(variables)
        
        # Detección de outliers
        logger.info("4. Detectando valores atípicos...")
        report['outliers'] = self.outliers_detection(variables)
        
        logger.info("\n" + "="*70)
        logger.info("REPORTE COMPLETADO")
        logger.info("="*70)
        
        return report
    
    def crosstab_analysis(self, var1: str, var2: str, 
                         normalize: Optional[str] = None) -> pd.DataFrame:
        """
        Genera tabla de contingencia (crosstab) entre dos variables.
        
        Args:
            var1 (str): Primera variable
            var2 (str): Segunda variable
            normalize (str, optional): Normalización ('index', 'columns', 'all')
            
        Returns:
            pd.DataFrame: Tabla de contingencia
        """
        crosstab = pd.crosstab(
            self.data[var1], 
            self.data[var2],
            normalize=normalize,
            margins=True
        )
        
        if normalize:
            crosstab = crosstab * 100  # Convertir a porcentajes
        
        logger.info(f"✓ Tabla de contingencia: {var1} vs {var2}")
        
        return crosstab


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def quick_summary(data: pd.DataFrame, variables: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Función rápida para obtener resumen estadístico.
    
    Args:
        data (pd.DataFrame): Datos a analizar
        variables (List[str], optional): Variables específicas
        
    Returns:
        pd.DataFrame: Resumen estadístico
    """
    analyzer = DescriptiveAnalyzer(data)
    return analyzer.basic_statistics(variables)


def quick_frequencies(data: pd.DataFrame, variable: str) -> pd.DataFrame:
    """
    Función rápida para tabla de frecuencias.
    
    Args:
        data (pd.DataFrame): Datos a analizar
        variable (str): Variable a tabular
        
    Returns:
        pd.DataFrame: Tabla de frecuencias
    """
    analyzer = DescriptiveAnalyzer(data)
    return analyzer.frequency_table(variable)
