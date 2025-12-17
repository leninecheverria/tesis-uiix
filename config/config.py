"""
Archivo de configuración para el análisis estadístico de la tesis.
Centraliza rutas, parámetros y configuraciones generales del proyecto.

Autor: Análisis de Tesis - Sistema de Gestión
Fecha: Diciembre 2025
"""

import os
from pathlib import Path

# ============================================================================
# RUTAS DEL PROYECTO
# ============================================================================

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Rutas de datos
DATA_DIR = BASE_DIR / "BD"
SPSS_FILE = DATA_DIR / "DatosAnalisisCOMPLETO.sav"
EXCEL_FILE = DATA_DIR / "Encuesta-LMS-CEV (respuestas) - Respuestas de formulario 1.xls"

# Rutas de resultados
RESULTS_DIR = BASE_DIR / "results"
GRAPHICS_DIR = RESULTS_DIR / "graficos"
TABLES_DIR = RESULTS_DIR / "tablas"
REPORTS_DIR = RESULTS_DIR / "reportes"

# Crear directorios si no existen
for directory in [GRAPHICS_DIR, TABLES_DIR, REPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


# ============================================================================
# PARÁMETROS DE ANÁLISIS ESTADÍSTICO
# ============================================================================

# Nivel de significancia
ALPHA = 0.05

# Nivel de confianza
CONFIDENCE_LEVEL = 0.95

# Criterios de confiabilidad (Alpha de Cronbach)
RELIABILITY_THRESHOLDS = {
    'excellent': 0.90,      # Excelente
    'good': 0.80,           # Bueno
    'acceptable': 0.70,     # Aceptable
    'questionable': 0.60,   # Cuestionable
    'poor': 0.50,           # Pobre
}

# Criterio para KMO (Kaiser-Meyer-Olkin)
KMO_THRESHOLDS = {
    'marvelous': 0.90,      # Maravilloso
    'meritorious': 0.80,    # Meritorio
    'middling': 0.70,       # Mediano
    'mediocre': 0.60,       # Mediocre
    'miserable': 0.50,      # Miserable
}


# ============================================================================
# CONFIGURACIÓN DE VISUALIZACIÓN
# ============================================================================

# Estilo de gráficos
PLOT_STYLE = 'seaborn-v0_8-darkgrid'  # Estilo profesional

# Paleta de colores (profesional para tesis)
COLOR_PALETTE = 'Set2'  # Opciones: 'Set2', 'husl', 'deep', 'muted', 'bright', 'dark', 'colorblind'

# Configuración de figuras
FIGURE_CONFIG = {
    'dpi': 300,                    # Alta resolución para tesis
    'figsize': (12, 8),           # Tamaño por defecto
    'format': 'png',              # Formato de salida
    'bbox_inches': 'tight',       # Ajuste de bordes
    'facecolor': 'white',         # Fondo blanco
}

# Fuentes
FONT_CONFIG = {
    'family': 'serif',
    'size': 11,
    'title_size': 14,
    'label_size': 12,
}


# ============================================================================
# CONFIGURACIÓN DE REPORTES
# ============================================================================

# Formato de números en reportes
DECIMAL_PLACES = 3

# Formato de exportación de tablas
TABLE_FORMAT = 'excel'  # Opciones: 'excel', 'csv', 'latex', 'html'


# ============================================================================
# VARIABLES Y DIMENSIONES DEL ESTUDIO
# ============================================================================

# Este diccionario debe ser actualizado según las dimensiones específicas de tu encuesta
# Ejemplo de estructura:
"""
DIMENSIONS = {
    'dimension_1': {
        'nombre': 'Usabilidad',
        'variables': ['P1', 'P2', 'P3', 'P4', 'P5'],
        'descripcion': 'Evaluación de la usabilidad del sistema'
    },
    'dimension_2': {
        'nombre': 'Satisfacción',
        'variables': ['P6', 'P7', 'P8', 'P9'],
        'descripcion': 'Nivel de satisfacción del usuario'
    },
    # ... más dimensiones
}
"""

# Esta será definida después de explorar los datos
DIMENSIONS = {}


# ============================================================================
# INFORMACIÓN DEL ESTUDIO
# ============================================================================

STUDY_INFO = {
    'titulo': 'Análisis de Encuesta - Tesis de Maestría',
    'autor': 'Lenin',
    'universidad': '',  # Completar
    'programa': 'Maestría',
    'año': 2025,
}


# ============================================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================================

LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S',
}


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def get_reliability_interpretation(alpha_value):
    """
    Interpreta el valor del Alpha de Cronbach.
    
    Args:
        alpha_value (float): Valor del Alpha de Cronbach
        
    Returns:
        str: Interpretación del valor
    """
    if alpha_value >= RELIABILITY_THRESHOLDS['excellent']:
        return 'Excelente'
    elif alpha_value >= RELIABILITY_THRESHOLDS['good']:
        return 'Bueno'
    elif alpha_value >= RELIABILITY_THRESHOLDS['acceptable']:
        return 'Aceptable'
    elif alpha_value >= RELIABILITY_THRESHOLDS['questionable']:
        return 'Cuestionable'
    elif alpha_value >= RELIABILITY_THRESHOLDS['poor']:
        return 'Pobre'
    else:
        return 'Inaceptable'


def get_kmo_interpretation(kmo_value):
    """
    Interpreta el valor del KMO (Kaiser-Meyer-Olkin).
    
    Args:
        kmo_value (float): Valor del KMO
        
    Returns:
        str: Interpretación del valor
    """
    if kmo_value >= KMO_THRESHOLDS['marvelous']:
        return 'Maravilloso'
    elif kmo_value >= KMO_THRESHOLDS['meritorious']:
        return 'Meritorio'
    elif kmo_value >= KMO_THRESHOLDS['middling']:
        return 'Mediano'
    elif kmo_value >= KMO_THRESHOLDS['mediocre']:
        return 'Mediocre'
    elif kmo_value >= KMO_THRESHOLDS['miserable']:
        return 'Miserable'
    else:
        return 'Inaceptable'
