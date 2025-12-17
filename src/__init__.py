"""
Paquete de análisis estadístico para tesis de maestría.

Este paquete proporciona herramientas completas para:
- Carga de datos desde SPSS y Excel
- Análisis de fiabilidad de instrumentos
- Estadística descriptiva e inferencial
- Visualización de datos profesional
- Generación de reportes

Autor: Sistema de Análisis de Tesis
Fecha: Diciembre 2025
"""

__version__ = '1.0.0'
__author__ = 'Sistema de Análisis de Tesis'

# Importar clases principales para acceso directo
from .data_loader import DataLoader
from .reliability_analysis import ReliabilityAnalyzer
from .descriptive_stats import DescriptiveAnalyzer
from .inferential_stats import InferentialAnalyzer
from .visualization import DataVisualizer
from .report_generator import ReportGenerator

__all__ = [
    'DataLoader',
    'ReliabilityAnalyzer',
    'DescriptiveAnalyzer',
    'InferentialAnalyzer',
    'DataVisualizer',
    'ReportGenerator',
]
