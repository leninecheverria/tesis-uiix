"""
Módulo de estadística inferencial para análisis de tesis.

Proporciona pruebas de hipótesis, análisis de correlación, ANOVA,
regresión y otras técnicas de estadística inferencial.

Autor: Sistema de Análisis de Tesis
Fecha: Diciembre 2025
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import logging
from typing import Dict, List, Tuple, Optional

# Configurar logging
logger = logging.getLogger(__name__)


class InferentialAnalyzer:
    """
    Clase para análisis estadístico inferencial.
    """
    
    def __init__(self, data: pd.DataFrame, alpha: float = 0.05):
        """
        Inicializa el analizador inferencial.
        
        Args:
            data (pd.DataFrame): DataFrame con los datos
            alpha (float): Nivel de significancia (por defecto 0.05)
        """
        self.data = data
        self.alpha = alpha
        self.confidence_level = 1 - alpha
    
    def t_test_one_sample(self, variable: str, 
                          population_mean: float) -> Dict:
        """
        Prueba t de Student para una muestra.
        
        H0: La media de la muestra es igual a la media poblacional
        H1: La media de la muestra es diferente
        
        Args:
            variable (str): Variable a analizar
            population_mean (float): Media poblacional de referencia
            
        Returns:
            Dict: Resultados de la prueba
        """
        serie = self.data[variable].dropna()
        
        # Realizar prueba t
        t_stat, p_value = stats.ttest_1samp(serie, population_mean)
        
        # Calcular intervalo de confianza
        ci = stats.t.interval(self.confidence_level, 
                             len(serie)-1,
                             loc=serie.mean(),
                             scale=serie.sem())
        
        result = {
            'variable': variable,
            'n': len(serie),
            'sample_mean': serie.mean(),
            'population_mean': population_mean,
            't_statistic': t_stat,
            'p_value': p_value,
            'significant': p_value < self.alpha,
            'confidence_interval': ci,
            'interpretation': self._interpret_test(p_value, 
                f"Hay diferencia significativa entre la media muestral ({serie.mean():.3f}) y poblacional ({population_mean})")
        }
        
        logger.info(f"✓ Prueba t una muestra: {variable}")
        logger.info(f"  t = {t_stat:.4f}, p = {p_value:.4f}")
        
        return result
    
    def t_test_independent(self, variable: str, 
                          group_var: str) -> Dict:
        """
        Prueba t de Student para muestras independientes.
        
        H0: Las medias de ambos grupos son iguales
        H1: Las medias de ambos grupos son diferentes
        
        Args:
            variable (str): Variable numérica a comparar
            group_var (str): Variable categórica con 2 grupos
            
        Returns:
            Dict: Resultados de la prueba
        """
        # Obtener grupos únicos
        groups = self.data[group_var].unique()
        
        if len(groups) != 2:
            logger.error(f"La variable {group_var} debe tener exactamente 2 grupos")
            return None
        
        # Separar datos por grupo
        group1 = self.data[self.data[group_var] == groups[0]][variable].dropna()
        group2 = self.data[self.data[group_var] == groups[1]][variable].dropna()
        
        # Prueba de Levene para homogeneidad de varianzas
        levene_stat, levene_p = stats.levene(group1, group2)
        equal_var = levene_p > self.alpha
        
        # Prueba t
        t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=equal_var)
        
        # Tamaño del efecto (d de Cohen)
        cohens_d = (group1.mean() - group2.mean()) / np.sqrt(
            ((len(group1)-1)*group1.std()**2 + (len(group2)-1)*group2.std()**2) / 
            (len(group1) + len(group2) - 2)
        )
        
        result = {
            'variable': variable,
            'group_var': group_var,
            'group1_name': groups[0],
            'group1_n': len(group1),
            'group1_mean': group1.mean(),
            'group1_std': group1.std(),
            'group2_name': groups[1],
            'group2_n': len(group2),
            'group2_mean': group2.mean(),
            'group2_std': group2.std(),
            'levene_statistic': levene_stat,
            'levene_p': levene_p,
            'equal_variances': equal_var,
            't_statistic': t_stat,
            'p_value': p_value,
            'cohens_d': cohens_d,
            'effect_size': self._interpret_cohens_d(cohens_d),
            'significant': p_value < self.alpha,
            'interpretation': self._interpret_test(p_value,
                f"Hay diferencia significativa entre {groups[0]} y {groups[1]}")
        }
        
        logger.info(f"✓ Prueba t independiente: {variable} por {group_var}")
        logger.info(f"  t = {t_stat:.4f}, p = {p_value:.4f}")
        
        return result
    
    def anova_one_way(self, variable: str, group_var: str) -> Dict:
        """
        ANOVA de una vía para comparar múltiples grupos.
        
        H0: Todas las medias de los grupos son iguales
        H1: Al menos una media es diferente
        
        Args:
            variable (str): Variable numérica dependiente
            group_var (str): Variable categórica con grupos
            
        Returns:
            Dict: Resultados de la prueba
        """
        # Obtener grupos
        groups = self.data[group_var].unique()
        group_data = [self.data[self.data[group_var] == g][variable].dropna() 
                     for g in groups]
        
        # ANOVA
        f_stat, p_value = stats.f_oneway(*group_data)
        
        # Eta cuadrado (tamaño del efecto)
        grand_mean = self.data[variable].mean()
        ss_between = sum([len(g) * (g.mean() - grand_mean)**2 for g in group_data])
        ss_total = sum([(x - grand_mean)**2 for g in group_data for x in g])
        eta_squared = ss_between / ss_total if ss_total > 0 else 0
        
        # Estadísticas descriptivas por grupo
        group_stats = {}
        for g in groups:
            g_data = self.data[self.data[group_var] == g][variable].dropna()
            group_stats[g] = {
                'n': len(g_data),
                'mean': g_data.mean(),
                'std': g_data.std()
            }
        
        result = {
            'variable': variable,
            'group_var': group_var,
            'n_groups': len(groups),
            'groups': list(groups),
            'group_statistics': group_stats,
            'f_statistic': f_stat,
            'p_value': p_value,
            'eta_squared': eta_squared,
            'effect_size': self._interpret_eta_squared(eta_squared),
            'significant': p_value < self.alpha,
            'interpretation': self._interpret_test(p_value,
                "Existen diferencias significativas entre los grupos")
        }
        
        # Post-hoc si es significativo
        if p_value < self.alpha:
            result['post_hoc'] = self._tukey_hsd(variable, group_var)
        
        logger.info(f"✓ ANOVA: {variable} por {group_var}")
        logger.info(f"  F = {f_stat:.4f}, p = {p_value:.4f}")
        
        return result
    
    def correlation_test(self, var1: str, var2: str, 
                        method: str = 'pearson') -> Dict:
        """
        Prueba de correlación entre dos variables.
        
        Args:
            var1 (str): Primera variable
            var2 (str): Segunda variable
            method (str): Método ('pearson', 'spearman', 'kendall')
            
        Returns:
            Dict: Resultados de la correlación
        """
        # Eliminar valores faltantes
        df_clean = self.data[[var1, var2]].dropna()
        
        # Calcular correlación
        if method == 'pearson':
            corr, p_value = stats.pearsonr(df_clean[var1], df_clean[var2])
        elif method == 'spearman':
            corr, p_value = stats.spearmanr(df_clean[var1], df_clean[var2])
        elif method == 'kendall':
            corr, p_value = stats.kendalltau(df_clean[var1], df_clean[var2])
        else:
            logger.error(f"Método '{method}' no reconocido")
            return None
        
        result = {
            'var1': var1,
            'var2': var2,
            'method': method,
            'n': len(df_clean),
            'correlation': corr,
            'p_value': p_value,
            'significant': p_value < self.alpha,
            'strength': self._interpret_correlation(corr),
            'interpretation': self._interpret_test(p_value,
                f"Correlación {self._interpret_correlation(corr).lower()} " +
                f"({'positiva' if corr > 0 else 'negativa'}) entre {var1} y {var2}")
        }
        
        logger.info(f"✓ Correlación {method}: {var1} vs {var2}")
        logger.info(f"  r = {corr:.4f}, p = {p_value:.4f}")
        
        return result
    
    def chi_square_test(self, var1: str, var2: str) -> Dict:
        """
        Prueba Chi-cuadrado de independencia para variables categóricas.
        
        H0: Las variables son independientes
        H1: Las variables están relacionadas
        
        Args:
            var1 (str): Primera variable categórica
            var2 (str): Segunda variable categórica
            
        Returns:
            Dict: Resultados de la prueba
        """
        # Crear tabla de contingencia
        contingency_table = pd.crosstab(self.data[var1], self.data[var2])
        
        # Prueba Chi-cuadrado
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        
        # V de Cramer (tamaño del efecto)
        n = contingency_table.sum().sum()
        min_dim = min(contingency_table.shape[0], contingency_table.shape[1]) - 1
        cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else 0
        
        result = {
            'var1': var1,
            'var2': var2,
            'contingency_table': contingency_table,
            'chi_square': chi2,
            'p_value': p_value,
            'degrees_of_freedom': dof,
            'cramers_v': cramers_v,
            'effect_size': self._interpret_cramers_v(cramers_v),
            'significant': p_value < self.alpha,
            'interpretation': self._interpret_test(p_value,
                f"Existe relación significativa entre {var1} y {var2}")
        }
        
        logger.info(f"✓ Chi-cuadrado: {var1} vs {var2}")
        logger.info(f"  χ² = {chi2:.4f}, p = {p_value:.4f}")
        
        return result
    
    def simple_regression(self, dependent_var: str, 
                         independent_var: str) -> Dict:
        """
        Regresión lineal simple.
        
        Args:
            dependent_var (str): Variable dependiente (Y)
            independent_var (str): Variable independiente (X)
            
        Returns:
            Dict: Resultados del modelo de regresión
        """
        # Preparar datos
        df_clean = self.data[[dependent_var, independent_var]].dropna()
        X = df_clean[[independent_var]].values
        y = df_clean[dependent_var].values
        
        # Ajustar modelo
        model = LinearRegression()
        model.fit(X, y)
        
        # Predicciones
        y_pred = model.predict(X)
        
        # R²
        r2 = model.score(X, y)
        
        # Error estándar
        mse = np.mean((y - y_pred)**2)
        rmse = np.sqrt(mse)
        
        # Prueba F para el modelo
        n = len(y)
        k = 1  # número de predictores
        ss_total = np.sum((y - np.mean(y))**2)
        ss_residual = np.sum((y - y_pred)**2)
        ss_regression = ss_total - ss_residual
        
        f_stat = (ss_regression / k) / (ss_residual / (n - k - 1))
        f_pvalue = 1 - stats.f.cdf(f_stat, k, n - k - 1)
        
        result = {
            'dependent_var': dependent_var,
            'independent_var': independent_var,
            'n': n,
            'intercept': model.intercept_,
            'slope': model.coef_[0],
            'r_squared': r2,
            'rmse': rmse,
            'f_statistic': f_stat,
            'f_pvalue': f_pvalue,
            'significant': f_pvalue < self.alpha,
            'equation': f"{dependent_var} = {model.intercept_:.3f} + {model.coef_[0]:.3f}*{independent_var}",
            'interpretation': self._interpret_test(f_pvalue,
                f"{independent_var} predice significativamente {dependent_var}")
        }
        
        logger.info(f"✓ Regresión simple: {dependent_var} ~ {independent_var}")
        logger.info(f"  R² = {r2:.4f}, F = {f_stat:.4f}, p = {f_pvalue:.4f}")
        
        return result
    
    def _tukey_hsd(self, variable: str, group_var: str) -> pd.DataFrame:
        """Prueba post-hoc de Tukey HSD (implementación simplificada)."""
        from itertools import combinations
        
        groups = self.data[group_var].unique()
        comparisons = []
        
        for g1, g2 in combinations(groups, 2):
            data1 = self.data[self.data[group_var] == g1][variable].dropna()
            data2 = self.data[self.data[group_var] == g2][variable].dropna()
            
            t_stat, p_val = stats.ttest_ind(data1, data2)
            
            comparisons.append({
                'Group1': g1,
                'Group2': g2,
                'Mean_Diff': data1.mean() - data2.mean(),
                'p_value': p_val,
                'Significant': p_val < self.alpha
            })
        
        return pd.DataFrame(comparisons)
    
    def _interpret_test(self, p_value: float, message: str) -> str:
        """Interpreta el resultado de una prueba de hipótesis."""
        if p_value < self.alpha:
            return f"Se rechaza H0 (p = {p_value:.4f}): {message}"
        else:
            return f"No se rechaza H0 (p = {p_value:.4f}): No hay evidencia suficiente"
    
    def _interpret_cohens_d(self, d: float) -> str:
        """Interpreta el tamaño del efecto de Cohen."""
        abs_d = abs(d)
        if abs_d < 0.2:
            return "Pequeño"
        elif abs_d < 0.5:
            return "Mediano"
        elif abs_d < 0.8:
            return "Grande"
        else:
            return "Muy grande"
    
    def _interpret_eta_squared(self, eta_sq: float) -> str:
        """Interpreta eta cuadrado."""
        if eta_sq < 0.01:
            return "Pequeño"
        elif eta_sq < 0.06:
            return "Mediano"
        else:
            return "Grande"
    
    def _interpret_correlation(self, r: float) -> str:
        """Interpreta la fuerza de la correlación."""
        abs_r = abs(r)
        if abs_r < 0.1:
            return "Despreciable"
        elif abs_r < 0.3:
            return "Débil"
        elif abs_r < 0.5:
            return "Moderada"
        elif abs_r < 0.7:
            return "Fuerte"
        else:
            return "Muy fuerte"
    
    def _interpret_cramers_v(self, v: float) -> str:
        """Interpreta V de Cramer."""
        if v < 0.1:
            return "Débil"
        elif v < 0.3:
            return "Moderado"
        else:
            return "Fuerte"


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def quick_ttest(data: pd.DataFrame, variable: str, group_var: str) -> Dict:
    """Función rápida para prueba t."""
    analyzer = InferentialAnalyzer(data)
    return analyzer.t_test_independent(variable, group_var)


def quick_correlation(data: pd.DataFrame, var1: str, var2: str) -> Dict:
    """Función rápida para correlación."""
    analyzer = InferentialAnalyzer(data)
    return analyzer.correlation_test(var1, var2)
