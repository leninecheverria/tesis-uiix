#!/usr/bin/env python3
"""
Script principal para análisis estadístico de encuesta de tesis.

Este script orquesta todo el proceso de análisis:
1. Carga de datos
2. Análisis de fiabilidad del instrumento
3. Análisis descriptivo
4. Análisis inferencial
5. Generación de visualizaciones
6. Exportación de resultados

Autor: Sistema de Análisis de Tesis
Fecha: Diciembre 2025
"""

import sys
import logging
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))
sys.path.insert(0, str(Path(__file__).parent))

# Importar módulos del proyecto
from src.data_loader import DataLoader
from src.reliability_analysis import ReliabilityAnalyzer
from src.descriptive_stats import DescriptiveAnalyzer
from src.inferential_stats import InferentialAnalyzer
from src.visualization import DataVisualizer
from src.report_generator import ReportGenerator
from src.pdf_generator import (generate_validity_reliability_report, 
                               generate_descriptive_report,
                               generate_inferential_report,
                               generate_visualizations_report,
                               generate_results_export_report)

# Importar configuración
from config import config


# ============================================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analisis.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ============================================================================
# CONFIGURACIÓN DE DIMENSIONES E ÍTEMS
# ============================================================================

# IMPORTANTE: Debes actualizar este diccionario con las dimensiones reales
# de tu encuesta después de explorar los datos.
# Ejemplo:
"""
DIMENSIONES = {
    'Usabilidad': {
        'items': ['P1', 'P2', 'P3', 'P4', 'P5'],
        'descripcion': 'Evaluación de la usabilidad del sistema'
    },
    'Satisfaccion': {
        'items': ['T1', 'T2', 'T3', 'T4', 'T5'],
        'descripcion': 'Nivel de satisfacción del usuario'
    },
    'Funcionalidad': {
        'items': ['L1', 'L2', 'L3', 'L4', 'L5'],
        'descripcion': 'Funcionalidades del sistema'
    }
    'Institucionalidad': {
        'items': ['I1', 'I2', 'I3', 'I4', 'I5', 'I6'],
        'descripcion': 'Identificación de la Institución'
    }
}
"""

# Dimensiones según la hipótesis de investigación:
# "Los factores personales, tecnológicos e institucionales inciden en la 
# viabilidad de implementar un LMS"
DIMENSIONES = {
    'Factor_Personal': {
        'items': ['P1', 'P2', 'P3', 'P4', 'P5'],
        'descripcion': 'Autogestión y disposición personal para aprendizaje virtual'
    },
    'Factor_Tecnologico': {
        'items': ['T1', 'T2', 'T3', 'T4', 'T5'],
        'descripcion': 'Infraestructura tecnológica y competencias digitales'
    },
    'Factor_Institucional': {
        'items': ['I1', 'I2', 'I3', 'I4', 'I5', 'I6'],
        'descripcion': 'Apoyo y capacidad institucional (solo asistentes a iglesia)'
    },
    'Viabilidad_LMS': {
        'items': ['L1', 'L2', 'L3', 'L4', 'L5'],
        'descripcion': 'Percepción de viabilidad del LMS (Variable dependiente)'
    }
}


# ============================================================================
# FUNCIONES PRINCIPALES
# ============================================================================

def crear_variables_acumuladas(data):
    """
    Crea variables acumuladas para probar la hipótesis de investigación.
    
    Hipótesis: Los factores personales, tecnológicos e institucionales
    inciden en la viabilidad de implementar un LMS.
    
    Args:
        data (DataFrame): Datos con variables originales
        
    Returns:
        DataFrame: Datos con variables acumuladas agregadas
    """
    import numpy as np
    
    logger.info("\n" + "="*80)
    logger.info("CREACIÓN DE VARIABLES ACUMULADAS PARA HIPÓTESIS")
    logger.info("="*80)
    
    # ============================================
    # VARIABLES INDEPENDIENTES (Factores)
    # ============================================
    
    # Factor Personal (Autogestión y Disposición)
    if all(col in data.columns for col in ['P1', 'P2', 'P3', 'P4', 'P5']):
        data['FACTOR_PERSONAL'] = data[['P1', 'P2', 'P3', 'P4', 'P5']].mean(axis=1)
        logger.info("✓ FACTOR_PERSONAL creado (P1-P5)")
    
    # Factor Tecnológico (Infraestructura y Competencias)
    if all(col in data.columns for col in ['T1', 'T2', 'T3', 'T4', 'T5']):
        data['FACTOR_TECNOLOGICO'] = data[['T1', 'T2', 'T3', 'T4', 'T5']].mean(axis=1)
        logger.info("✓ FACTOR_TECNOLOGICO creado (T1-T5)")
    
    # Factor Institucional (Apoyo Institucional)
    # Solo disponible para asistentes a la iglesia
    if all(col in data.columns for col in ['I1', 'I2', 'I3', 'I4', 'I5', 'I6']):
        data['FACTOR_INSTITUCIONAL'] = data[['I1', 'I2', 'I3', 'I4', 'I5', 'I6']].mean(axis=1)
        n_validos = data['FACTOR_INSTITUCIONAL'].notna().sum()
        logger.info(f"✓ FACTOR_INSTITUCIONAL creado (I1-I6) - {n_validos} casos válidos")
    
    # ============================================
    # VARIABLE DEPENDIENTE (Viabilidad)
    # ============================================
    
    if all(col in data.columns for col in ['L1', 'L2', 'L3', 'L4', 'L5']):
        # Invertir L5 (pregunta negativa sobre riesgos)
        data['L5_invertida'] = 6 - data['L5']  # Escala 1-5 invertida
        logger.info("✓ L5_invertida creada (L5 invertida para análisis)")
        
        # Viabilidad del LMS (Percepción de viabilidad)
        data['VIABILIDAD_LMS'] = data[['L1', 'L2', 'L3', 'L4', 'L5_invertida']].mean(axis=1)
        logger.info("✓ VIABILIDAD_LMS creada (L1-L4 + L5_invertida)")
    
    # ============================================
    # RESUMEN
    # ============================================
    logger.info("\n" + "-"*80)
    logger.info("RESUMEN DE VARIABLES ACUMULADAS:")
    logger.info("-"*80)
    
    variables_creadas = [
        ('FACTOR_PERSONAL', 'Variable Independiente 1'),
        ('FACTOR_TECNOLOGICO', 'Variable Independiente 2'),
        ('FACTOR_INSTITUCIONAL', 'Variable Independiente 3'),
        ('VIABILIDAD_LMS', 'Variable Dependiente')
    ]
    
    for var_name, tipo in variables_creadas:
        if var_name in data.columns:
            n_valid = data[var_name].notna().sum()
            mean_val = data[var_name].mean()
            std_val = data[var_name].std()
            logger.info(f"  {var_name:25s} | {tipo:30s} | n={n_valid:3d} | M={mean_val:.2f} | DE={std_val:.2f}")
    
    logger.info("="*80 + "\n")
    
    return data


def cargar_datos():
    """
    Carga los datos desde archivo SPSS o Excel.
    
    Returns:
        tuple: (DataLoader, DataFrame)
    """
    logger.info("="*80)
    logger.info("PASO 1: CARGA DE DATOS")
    logger.info("="*80)
    
    loader = DataLoader()
    
    # Intentar cargar archivo SPSS primero (recomendado)
    try:
        logger.info(f"\nCargando archivo SPSS: {config.SPSS_FILE}")
        data, metadata = loader.load_spss(str(config.SPSS_FILE))
        
        logger.info("\n✓ Datos cargados exitosamente desde SPSS")
        logger.info(f"  - Variables: {metadata['n_variables']}")
        logger.info(f"  - Observaciones: {metadata['n_observations']}")
        
        # Mostrar primeras variables
        logger.info("\n  Primeras 10 variables:")
        for i, var in enumerate(metadata['variable_names'][:10], 1):
            label = metadata['variable_labels'].get(var, 'Sin etiqueta')
            logger.info(f"    {i}. {var}: {label}")
        
        return loader, data
        
    except Exception as e:
        logger.warning(f"No se pudo cargar archivo SPSS: {str(e)}")
        logger.info("Intentando cargar archivo Excel...")
        
        try:
            data = loader.load_excel(str(config.EXCEL_FILE))
            logger.info("\n✓ Datos cargados exitosamente desde Excel")
            logger.info(f"  - Variables: {len(data.columns)}")
            logger.info(f"  - Observaciones: {len(data)}")
            
            return loader, data
            
        except Exception as e:
            logger.error(f"✗ Error al cargar datos: {str(e)}")
            sys.exit(1)


def explorar_datos(loader):
    """
    Explora y muestra resumen de los datos.
    
    Args:
        loader (DataLoader): Cargador de datos con información
    """
    logger.info("\n" + "="*80)
    logger.info("PASO 2: EXPLORACIÓN INICIAL DE DATOS")
    logger.info("="*80)
    
    # Resumen de datos
    summary = loader.get_data_summary()
    logger.info(f"\n✓ Resumen generado con {len(summary)} variables")
    
    # Exportar resumen
    output_path = config.TABLES_DIR / "resumen_datos.xlsx"
    loader.export_to_excel(str(output_path))
    logger.info(f"✓ Resumen exportado a: {output_path}")
    
    # Mostrar variables numéricas
    numeric_cols = loader.filter_numeric_columns(exclude_patterns=['ID', 'Marca'])
    logger.info(f"\n✓ Variables numéricas encontradas: {len(numeric_cols)}")
    logger.info(f"  {', '.join(numeric_cols[:20])}" + 
               (f" ... (+{len(numeric_cols)-20} más)" if len(numeric_cols) > 20 else ""))
    
    return summary, numeric_cols


def analizar_fiabilidad_validez(data, dimensiones, include_validity=True, 
                                criterion_variable=None):
    """
    Realiza análisis de confiabilidad y validez del instrumento.
    
    Basado en la metodología de Hernández-Sampieri et al. (2014).
    
    Args:
        data (DataFrame): Datos a analizar
        dimensiones (dict): Diccionario con dimensiones e ítems
        include_validity (bool): Si True, incluye análisis de validez
        criterion_variable (str): Variable criterio para validez de criterio
        
    Returns:
        dict: Resultados del análisis de confiabilidad y validez
    """
    if not dimensiones:
        logger.warning("\n⚠ No se definieron dimensiones. Saltando análisis.")
        logger.warning("  Por favor, actualiza la variable DIMENSIONES en main.py")
        return None
    
    logger.info("\n" + "="*80)
    logger.info("PASO 3: ANÁLISIS DE CONFIABILIDAD Y VALIDEZ DEL INSTRUMENTO")
    logger.info("Metodología: Hernández-Sampieri et al. (2014)")
    logger.info("="*80)
    
    # Convertir formato de dimensiones
    dims_for_analysis = {
        name: info['items'] 
        for name, info in dimensiones.items()
    }
    
    # Realizar análisis
    analyzer = ReliabilityAnalyzer(data)
    results = analyzer.comprehensive_reliability_validity(
        dims_for_analysis,
        include_validity=include_validity,
        criterion_variable=criterion_variable
    )
    
    # Generar reporte
    reporter = ReportGenerator(config.REPORTS_DIR)
    reporter.export_reliability_report(results, "reporte_confiabilidad_validez")
    
    logger.info("\n✓ Análisis de confiabilidad y validez completado")
    
    return results


def analizar_fiabilidad(data, dimensiones):
    """
    Realiza análisis de confiabilidad (método legacy).
    
    Nota: Se recomienda usar analizar_fiabilidad_validez() para análisis completo.
    
    Args:
        data (DataFrame): Datos a analizar
        dimensiones (dict): Diccionario con dimensiones e ítems
        
    Returns:
        dict: Resultados del análisis de confiabilidad
    """
    return analizar_fiabilidad_validez(data, dimensiones, include_validity=False)


def analisis_dos_niveles(data, dimensiones):
    """
    Realiza análisis en dos niveles según disponibilidad de datos.
    
    NIVEL 1 (n=140): Factores Personal + Tecnológico → Viabilidad
    NIVEL 2 (n=54): Factores Personal + Tecnológico + Institucional → Viabilidad
    
    Args:
        data (DataFrame): Datos con variables acumuladas
        dimensiones (dict): Diccionario con dimensiones
    
    Returns:
        dict: Resultados de ambos niveles de análisis
    """
    import numpy as np
    from scipy import stats as sp_stats
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score
    
    logger.info("\n" + "="*80)
    logger.info("ANÁLISIS EN DOS NIVELES SEGÚN HIPÓTESIS")
    logger.info("="*80)
    
    results = {
        'nivel1_general': {},
        'nivel2_institucional': {},
        'comparacion': {}
    }
    
    # ========================================================================
    # NIVEL 1: ANÁLISIS GENERAL (n=140)
    # ========================================================================
    
    logger.info("\n" + "─"*80)
    logger.info("NIVEL 1: ANÁLISIS GENERAL (Población Amplia)")
    logger.info("─"*80)
    logger.info("Muestra: Todos los participantes (n=140)")
    logger.info("Factores: Personal + Tecnológico → Viabilidad LMS\n")
    
    # Dimensiones para Nivel 1 (excluye Factor Institucional)
    # Extraer solo los ítems de cada dimensión
    dimensiones_nivel1 = {
        k: v['items'] if isinstance(v, dict) else v
        for k, v in dimensiones.items() 
        if k != 'Factor_Institucional'
    }
    
    # Confiabilidad Nivel 1
    logger.info("📊 1.1. CONFIABILIDAD Y VALIDEZ")
    analyzer_n1 = ReliabilityAnalyzer(data)
    results['nivel1_general']['confiabilidad'] = analyzer_n1.comprehensive_reliability_validity(
        dimensiones_nivel1,
        include_validity=True,
        criterion_variable='VIABILIDAD_LMS'
    )
    
    # Descriptivos Nivel 1
    logger.info("\n📊 1.2. ESTADÍSTICAS DESCRIPTIVAS")
    variables_n1 = ['FACTOR_PERSONAL', 'FACTOR_TECNOLOGICO', 'VIABILIDAD_LMS']
    results['nivel1_general']['descriptivos'] = {}
    
    for var in variables_n1:
        if var in data.columns:
            n = data[var].notna().sum()
            mean = data[var].mean()
            std = data[var].std()
            results['nivel1_general']['descriptivos'][var] = {
                'n': n, 'mean': mean, 'std': std
            }
            logger.info(f"  {var}: N={n}, M={mean:.3f}, DE={std:.3f}")
    
    # Correlaciones Nivel 1
    logger.info("\n📊 1.3. CORRELACIONES")
    r_personal = data['FACTOR_PERSONAL'].corr(data['VIABILIDAD_LMS'])
    r_tecnologico = data['FACTOR_TECNOLOGICO'].corr(data['VIABILIDAD_LMS'])
    
    n1 = len(data.dropna(subset=['FACTOR_PERSONAL', 'VIABILIDAD_LMS']))
    t_personal = r_personal * np.sqrt((n1-2)/(1-r_personal**2))
    p_personal = 2 * (1 - sp_stats.t.cdf(abs(t_personal), n1-2))
    
    n2 = len(data.dropna(subset=['FACTOR_TECNOLOGICO', 'VIABILIDAD_LMS']))
    t_tecnologico = r_tecnologico * np.sqrt((n2-2)/(1-r_tecnologico**2))
    p_tecnologico = 2 * (1 - sp_stats.t.cdf(abs(t_tecnologico), n2-2))
    
    sig_personal = '***' if p_personal < 0.001 else '**' if p_personal < 0.01 else '*' if p_personal < 0.05 else 'ns'
    sig_tecnologico = '***' if p_tecnologico < 0.001 else '**' if p_tecnologico < 0.01 else '*' if p_tecnologico < 0.05 else 'ns'
    
    logger.info(f"  Personal ↔ Viabilidad: r={r_personal:.3f}, p={p_personal:.4f} {sig_personal}")
    logger.info(f"  Tecnológico ↔ Viabilidad: r={r_tecnologico:.3f}, p={p_tecnologico:.4f} {sig_tecnologico}")
    
    results['nivel1_general']['correlaciones'] = {
        'personal': {'r': r_personal, 'p': p_personal, 'n': n1},
        'tecnologico': {'r': r_tecnologico, 'p': p_tecnologico, 'n': n2}
    }
    
    # Regresión Nivel 1
    logger.info("\n📊 1.4. REGRESIÓN MÚLTIPLE")
    logger.info("  Modelo: VIABILIDAD = β0 + β1(Personal) + β2(Tecnológico)")
    
    data_reg_n1 = data[['FACTOR_PERSONAL', 'FACTOR_TECNOLOGICO', 'VIABILIDAD_LMS']].dropna()
    X_n1 = data_reg_n1[['FACTOR_PERSONAL', 'FACTOR_TECNOLOGICO']]
    y_n1 = data_reg_n1['VIABILIDAD_LMS']
    
    model_n1 = LinearRegression()
    model_n1.fit(X_n1, y_n1)
    y_pred_n1 = model_n1.predict(X_n1)
    r2_n1 = r2_score(y_n1, y_pred_n1)
    
    logger.info(f"\n  Resultados:")
    logger.info(f"    R² = {r2_n1:.3f} ({r2_n1*100:.1f}% varianza explicada)")
    logger.info(f"    β0 = {model_n1.intercept_:.3f}")
    logger.info(f"    β1 (Personal) = {model_n1.coef_[0]:.3f}")
    logger.info(f"    β2 (Tecnológico) = {model_n1.coef_[1]:.3f}")
    logger.info(f"    N = {len(data_reg_n1)}")
    
    results['nivel1_general']['regresion'] = {
        'r2': r2_n1,
        'intercepto': model_n1.intercept_,
        'coef_personal': model_n1.coef_[0],
        'coef_tecnologico': model_n1.coef_[1],
        'n': len(data_reg_n1)
    }
    
    # ========================================================================
    # NIVEL 2: ANÁLISIS INSTITUCIONAL (n=54)
    # ========================================================================
    
    logger.info("\n\n" + "─"*80)
    logger.info("NIVEL 2: ANÁLISIS INSTITUCIONAL (Contexto Específico)")
    logger.info("─"*80)
    logger.info("Muestra: Solo asistentes a iglesia (n=54)")
    logger.info("Factores: Personal + Tecnológico + Institucional → Viabilidad\n")
    
    # Filtrar datos
    data_iglesia = data[data['FACTOR_INSTITUCIONAL'].notna()].copy()
    n_iglesia = len(data_iglesia)
    logger.info(f"📌 Casos con Factor Institucional: {n_iglesia}")
    
    # Confiabilidad Nivel 2
    # Extraer solo los ítems de cada dimensión
    dimensiones_nivel2 = {
        k: v['items'] if isinstance(v, dict) else v
        for k, v in dimensiones.items()
    }
    
    logger.info("\n📊 2.1. CONFIABILIDAD Y VALIDEZ")
    analyzer_n2 = ReliabilityAnalyzer(data_iglesia)
    results['nivel2_institucional']['confiabilidad'] = analyzer_n2.comprehensive_reliability_validity(
        dimensiones_nivel2,
        include_validity=True,
        criterion_variable='VIABILIDAD_LMS'
    )
    
    # Descriptivos Nivel 2
    logger.info("\n📊 2.2. ESTADÍSTICAS DESCRIPTIVAS")
    variables_n2 = ['FACTOR_PERSONAL', 'FACTOR_TECNOLOGICO', 'FACTOR_INSTITUCIONAL', 'VIABILIDAD_LMS']
    results['nivel2_institucional']['descriptivos'] = {}
    
    for var in variables_n2:
        n = data_iglesia[var].notna().sum()
        mean = data_iglesia[var].mean()
        std = data_iglesia[var].std()
        results['nivel2_institucional']['descriptivos'][var] = {
            'n': n, 'mean': mean, 'std': std
        }
        logger.info(f"  {var}: N={n}, M={mean:.3f}, DE={std:.3f}")
    
    # Correlaciones Nivel 2
    logger.info("\n📊 2.3. CORRELACIONES")
    r_personal_2 = data_iglesia['FACTOR_PERSONAL'].corr(data_iglesia['VIABILIDAD_LMS'])
    r_tecnologico_2 = data_iglesia['FACTOR_TECNOLOGICO'].corr(data_iglesia['VIABILIDAD_LMS'])
    r_institucional = data_iglesia['FACTOR_INSTITUCIONAL'].corr(data_iglesia['VIABILIDAD_LMS'])
    
    logger.info(f"  Personal ↔ Viabilidad: r={r_personal_2:.3f}")
    logger.info(f"  Tecnológico ↔ Viabilidad: r={r_tecnologico_2:.3f}")
    logger.info(f"  Institucional ↔ Viabilidad: r={r_institucional:.3f}")
    
    results['nivel2_institucional']['correlaciones'] = {
        'personal': r_personal_2,
        'tecnologico': r_tecnologico_2,
        'institucional': r_institucional
    }
    
    # Regresión Nivel 2
    logger.info("\n📊 2.4. REGRESIÓN MÚLTIPLE")
    logger.info("  Modelo: VIABILIDAD = β0 + β1(Personal) + β2(Tecnológico) + β3(Institucional)")
    
    data_reg_n2 = data_iglesia[['FACTOR_PERSONAL', 'FACTOR_TECNOLOGICO', 
                                 'FACTOR_INSTITUCIONAL', 'VIABILIDAD_LMS']].dropna()
    X_n2 = data_reg_n2[['FACTOR_PERSONAL', 'FACTOR_TECNOLOGICO', 'FACTOR_INSTITUCIONAL']]
    y_n2 = data_reg_n2['VIABILIDAD_LMS']
    
    model_n2 = LinearRegression()
    model_n2.fit(X_n2, y_n2)
    y_pred_n2 = model_n2.predict(X_n2)
    r2_n2 = r2_score(y_n2, y_pred_n2)
    
    logger.info(f"\n  Resultados:")
    logger.info(f"    R² = {r2_n2:.3f} ({r2_n2*100:.1f}% varianza explicada)")
    logger.info(f"    β0 = {model_n2.intercept_:.3f}")
    logger.info(f"    β1 (Personal) = {model_n2.coef_[0]:.3f}")
    logger.info(f"    β2 (Tecnológico) = {model_n2.coef_[1]:.3f}")
    logger.info(f"    β3 (Institucional) = {model_n2.coef_[2]:.3f}")
    logger.info(f"    N = {len(data_reg_n2)}")
    
    results['nivel2_institucional']['regresion'] = {
        'r2': r2_n2,
        'intercepto': model_n2.intercept_,
        'coef_personal': model_n2.coef_[0],
        'coef_tecnologico': model_n2.coef_[1],
        'coef_institucional': model_n2.coef_[2],
        'n': len(data_reg_n2)
    }
    
    # ========================================================================
    # COMPARACIÓN
    # ========================================================================
    
    logger.info("\n\n" + "="*80)
    logger.info("COMPARACIÓN DE MODELOS")
    logger.info("="*80)
    logger.info(f"\nNivel 1 (n={len(data_reg_n1)}): R² = {r2_n1:.3f}")
    logger.info(f"Nivel 2 (n={len(data_reg_n2)}): R² = {r2_n2:.3f}")
    logger.info(f"\n💡 Incremento en R²: +{r2_n2-r2_n1:.3f} ({(r2_n2-r2_n1)*100:.1f}% adicional)")
    
    results['comparacion'] = {
        'delta_r2': r2_n2 - r2_n1,
        'mejora_porcentual': (r2_n2 - r2_n1) * 100
    }
    
    logger.info("\n" + "="*80)
    logger.info("✓ ANÁLISIS EN DOS NIVELES COMPLETADO")
    logger.info("="*80)
    
    return results


def analisis_descriptivo(data, variables):
    """
    Realiza análisis estadístico descriptivo.
    
    Args:
        data (DataFrame): Datos a analizar
        variables (list): Lista de variables numéricas
        
    Returns:
        dict: Resultados del análisis descriptivo
    """
    logger.info("\n" + "="*80)
    logger.info("PASO 4: ANÁLISIS ESTADÍSTICO DESCRIPTIVO")
    logger.info("="*80)
    
    analyzer = DescriptiveAnalyzer(data)
    
    # Estadísticas básicas
    logger.info("\n4.1. Calculando estadísticas básicas...")
    stats_basic = analyzer.basic_statistics(variables)
    
    # Matriz de correlación
    logger.info("4.2. Calculando matriz de correlación...")
    corr_matrix = analyzer.correlation_matrix(variables)
    
    # Pruebas de normalidad
    logger.info("4.3. Realizando pruebas de normalidad...")
    normality = analyzer.normality_tests(variables)
    
    # Exportar resultados
    reporter = ReportGenerator(config.TABLES_DIR)
    reporter.export_descriptive_report(stats_basic, "estadisticas_descriptivas")
    reporter.export_correlation_report(corr_matrix, "matriz_correlacion")
    
    results = {
        'basic_statistics': stats_basic,
        'correlation_matrix': corr_matrix,
        'normality_tests': normality
    }
    
    logger.info("\n✓ Análisis descriptivo completado")
    
    return results


def generar_visualizaciones(data, variables, corr_matrix):
    """
    Genera visualizaciones profesionales.
    
    Args:
        data (DataFrame): Datos a visualizar
        variables (list): Lista de variables
        corr_matrix (DataFrame): Matriz de correlación
    """
    logger.info("\n" + "="*80)
    logger.info("PASO 5: GENERACIÓN DE VISUALIZACIONES")
    logger.info("="*80)
    
    visualizer = DataVisualizer(config.GRAPHICS_DIR, dpi=300)
    
    # Histogramas de las primeras variables
    logger.info("\n5.1. Generando histogramas...")
    for var in variables[:5]:  # Primeras 5 variables
        try:
            visualizer.histogram(data[var], 
                               title=f'Distribución de {var}',
                               filename=f'hist_{var}.png')
        except Exception as e:
            logger.warning(f"  No se pudo generar histograma para {var}: {str(e)}")
    
    # Boxplot comparativo
    logger.info("5.2. Generando boxplots...")
    try:
        visualizer.boxplot(data, variables=variables[:10],
                          title='Comparación de Variables',
                          filename='boxplot_comparacion.png')
    except Exception as e:
        logger.warning(f"  Error en boxplot: {str(e)}")
    
    # Mapa de calor de correlaciones
    logger.info("5.3. Generando mapa de calor de correlaciones...")
    try:
        visualizer.correlation_heatmap(corr_matrix,
                                      title='Matriz de Correlación',
                                      filename='heatmap_correlacion.png')
    except Exception as e:
        logger.warning(f"  Error en heatmap: {str(e)}")
    
    logger.info("\n✓ Visualizaciones generadas")


def generar_reporte_maestro(reliability_results, descriptive_results):
    """
    Genera reporte maestro con todos los resultados.
    
    Args:
        reliability_results (dict): Resultados de fiabilidad
        descriptive_results (dict): Resultados descriptivos
    """
    logger.info("\n" + "="*80)
    logger.info("PASO 6: GENERACIÓN DE REPORTE MAESTRO")
    logger.info("="*80)
    
    reporter = ReportGenerator(config.REPORTS_DIR)
    
    study_info = {
        'Título': config.STUDY_INFO['titulo'],
        'Autor': config.STUDY_INFO['autor'],
        'Programa': config.STUDY_INFO['programa'],
        'Año': config.STUDY_INFO['año'],
    }
    
    reporter.generate_master_report(
        study_info=study_info,
        reliability_results=reliability_results,
        descriptive_results=descriptive_results,
        filename='reporte_maestro'
    )
    
    logger.info("\n✓ Reporte maestro generado")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """
    Función principal que ejecuta todo el análisis.
    """
    logger.info("\n" + "="*80)
    logger.info("SISTEMA DE ANÁLISIS ESTADÍSTICO PARA TESIS DE MAESTRÍA")
    logger.info("Metodología: Hernández-Sampieri et al. (2014)")
    logger.info("="*80)
    logger.info(f"Inicio del análisis: {config.STUDY_INFO['año']}\n")
    
    try:
        # 1. Cargar datos
        loader, data = cargar_datos()
        
        # 2. Crear variables acumuladas según hipótesis
        data = crear_variables_acumuladas(data)
        
        # 3. Explorar datos
        summary, numeric_vars = explorar_datos(loader)
        
        # 4. ANÁLISIS EN DOS NIVELES (Principal)
        logger.info("\n" + "🎯"*40)
        logger.info("ANÁLISIS PRINCIPAL: Prueba de Hipótesis en Dos Niveles")
        logger.info("🎯"*40)
        resultados_dos_niveles = analisis_dos_niveles(data, DIMENSIONES)
        
        # 5. Análisis descriptivo general
        descriptive_results = analisis_descriptivo(data, numeric_vars)
        
        # 6. Generar visualizaciones
        generar_visualizaciones(data, numeric_vars, 
                               descriptive_results['correlation_matrix'])
        
        # 7. Exportar resultados de análisis de dos niveles
        logger.info("\n📁 Exportando resultados del análisis en dos niveles...")
        reporter = ReportGenerator(config.REPORTS_DIR)
        
        # Guardar resultados en archivo de texto
        with open(config.REPORTS_DIR / 'analisis_dos_niveles.txt', 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("RESULTADOS DEL ANÁLISIS EN DOS NIVELES\n")
            f.write("="*80 + "\n\n")
            
            f.write("NIVEL 1: Análisis General (n=140)\n")
            f.write("-"*80 + "\n")
            if 'regresion' in resultados_dos_niveles['nivel1_general']:
                reg = resultados_dos_niveles['nivel1_general']['regresion']
                f.write(f"R² = {reg['r2']:.3f}\n")
                f.write(f"β₀ (Intercepto) = {reg['intercepto']:.3f}\n")
                f.write(f"β₁ (Factor Personal) = {reg['coef_personal']:.3f}\n")
                f.write(f"β₂ (Factor Tecnológico) = {reg['coef_tecnologico']:.3f}\n")
                f.write(f"N = {reg['n']}\n\n")
            
            f.write("NIVEL 2: Análisis Institucional (n=54)\n")
            f.write("-"*80 + "\n")
            if 'regresion' in resultados_dos_niveles['nivel2_institucional']:
                reg = resultados_dos_niveles['nivel2_institucional']['regresion']
                f.write(f"R² = {reg['r2']:.3f}\n")
                f.write(f"β₀ (Intercepto) = {reg['intercepto']:.3f}\n")
                f.write(f"β₁ (Factor Personal) = {reg['coef_personal']:.3f}\n")
                f.write(f"β₂ (Factor Tecnológico) = {reg['coef_tecnologico']:.3f}\n")
                f.write(f"β₃ (Factor Institucional) = {reg['coef_institucional']:.3f}\n")
                f.write(f"N = {reg['n']}\n")
        
        logger.info("✓ Resultados exportados a: analisis_dos_niveles.txt")
        
        # 8. Generar reportes PDF de validez y confiabilidad
        logger.info("\n📄 Generando reportes PDF de validez y confiabilidad...")
        
        # PDF Nivel 1
        pdf_path_n1 = config.REPORTS_DIR / 'validez_confiabilidad_nivel1.pdf'
        generate_validity_reliability_report(
            resultados_dos_niveles['nivel1_general'],
            str(pdf_path_n1),
            nivel="Nivel 1 - Análisis General (n=140)"
        )
        logger.info(f"✓ PDF Nivel 1 generado: {pdf_path_n1}")
        
        # PDF Nivel 2
        pdf_path_n2 = config.REPORTS_DIR / 'validez_confiabilidad_nivel2.pdf'
        generate_validity_reliability_report(
            resultados_dos_niveles['nivel2_institucional'],
            str(pdf_path_n2),
            nivel="Nivel 2 - Análisis Institucional (n=54)"
        )
        logger.info(f"✓ PDF Nivel 2 generado: {pdf_path_n2}")
        
        # PDF Análisis Descriptivo
        pdf_path_desc = config.REPORTS_DIR / 'analisis_descriptivo.pdf'
        generate_descriptive_report(
            descriptive_results,
            data,
            str(pdf_path_desc)
        )
        logger.info(f"✓ PDF Análisis Descriptivo generado: {pdf_path_desc}")
        
        # PDF Análisis Inferencial
        pdf_path_inf = config.REPORTS_DIR / 'analisis_inferencial.pdf'
        generate_inferential_report(
            resultados_dos_niveles,
            str(pdf_path_inf)
        )
        logger.info(f"✓ PDF Análisis Inferencial generado: {pdf_path_inf}")
        
        # PDF Visualizaciones
        pdf_path_viz = config.REPORTS_DIR / 'visualizaciones.pdf'
        generate_visualizations_report(
            str(config.GRAPHICS_DIR),
            str(pdf_path_viz)
        )
        logger.info(f"✓ PDF Visualizaciones generado: {pdf_path_viz}")
        
        # PDF Resumen Ejecutivo (Exportación de Resultados)
        pdf_path_resumen = config.REPORTS_DIR / 'resumen_ejecutivo.pdf'
        generate_results_export_report(
            resultados_dos_niveles,
            descriptive_results,
            str(pdf_path_resumen)
        )
        logger.info(f"✓ PDF Resumen Ejecutivo generado: {pdf_path_resumen}")
        
        # Resumen final
        logger.info("\n" + "="*80)
        logger.info("ANÁLISIS COMPLETADO EXITOSAMENTE")
        logger.info("="*80)
        logger.info("\nResultados guardados en:")
        logger.info(f"  - Gráficos: {config.GRAPHICS_DIR}")
        logger.info(f"  - Tablas: {config.TABLES_DIR}")
        logger.info(f"  - Reportes: {config.REPORTS_DIR}")
        logger.info(f"  - PDFs de Validez y Confiabilidad: {config.REPORTS_DIR}")
        logger.info("\n¡Revisa los archivos generados para incluir en tu tesis!")
        
    except Exception as e:
        logger.error(f"\n✗ Error durante el análisis: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
