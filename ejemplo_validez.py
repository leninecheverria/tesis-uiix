#!/usr/bin/env python3
"""
Ejemplo de uso del análisis de confiabilidad y validez.

Este script demuestra cómo usar las nuevas funcionalidades de validez
implementadas según Hernández-Sampieri et al. (2014).

Autor: Sistema de Análisis de Tesis
Fecha: Diciembre 2024
"""

import sys
from pathlib import Path
import pandas as pd

# Agregar directorios al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))
sys.path.insert(0, str(Path(__file__).parent))

from src.data_loader import DataLoader
from src.reliability_analysis import ReliabilityAnalyzer
from config import config


def ejemplo_confiabilidad_basica():
    """
    Ejemplo 1: Análisis de confiabilidad básico (solo Alpha, KMO, Bartlett)
    """
    print("=" * 80)
    print("EJEMPLO 1: ANÁLISIS DE CONFIABILIDAD BÁSICO")
    print("=" * 80)
    
    # Cargar datos
    loader = DataLoader()
    try:
        data, metadata = loader.load_spss(str(config.SPSS_FILE))
    except:
        print("⚠ No se pudo cargar el archivo SPSS")
        return
    
    # Definir dimensiones de ejemplo (DEBES CAMBIAR ESTO CON TUS DATOS REALES)
    dimensiones = {
        'Dimension1': ['P1', 'P2', 'P3', 'P4'],  # Cambia por tus columnas reales
        'Dimension2': ['P5', 'P6', 'P7', 'P8']   # Cambia por tus columnas reales
    }
    
    # Crear analizador
    analyzer = ReliabilityAnalyzer(data)
    
    # Análisis solo de confiabilidad
    results = analyzer.comprehensive_reliability_validity(
        dimensiones,
        include_validity=False  # Solo confiabilidad
    )
    
    # Mostrar resultados
    print("\n📊 RESULTADOS:")
    print(f"Alpha de Cronbach general: {results['general']['cronbach_alpha']['alpha']:.3f}")
    print(f"Interpretación: {results['general']['cronbach_alpha']['interpretation']}")
    
    print("\nPor dimensión:")
    for dim_name, dim_results in results['by_dimension'].items():
        alpha = dim_results['cronbach_alpha']['alpha']
        interp = dim_results['cronbach_alpha']['interpretation']
        print(f"  {dim_name}: α = {alpha:.3f} ({interp})")


def ejemplo_confiabilidad_validez_completo():
    """
    Ejemplo 2: Análisis COMPLETO de confiabilidad y validez
    """
    print("\n\n")
    print("=" * 80)
    print("EJEMPLO 2: ANÁLISIS COMPLETO (CONFIABILIDAD + VALIDEZ)")
    print("Metodología: Hernández-Sampieri et al. (2014)")
    print("=" * 80)
    
    # Cargar datos
    loader = DataLoader()
    try:
        data, metadata = loader.load_spss(str(config.SPSS_FILE))
    except:
        print("⚠ No se pudo cargar el archivo SPSS")
        return
    
    # Definir dimensiones
    dimensiones = {
        'Dimension1': ['P1', 'P2', 'P3', 'P4'],
        'Dimension2': ['P5', 'P6', 'P7', 'P8']
    }
    
    # Crear analizador
    analyzer = ReliabilityAnalyzer(data)
    
    # Análisis COMPLETO
    results = analyzer.comprehensive_reliability_validity(
        dimensiones,
        include_validity=True,      # Incluir validez
        criterion_variable=None     # Cambia si tienes variable criterio
    )
    
    # Mostrar resultados de CONFIABILIDAD
    print("\n📊 CONFIABILIDAD:")
    print(f"Alpha de Cronbach: {results['general']['cronbach_alpha']['alpha']:.3f}")
    print(f"Dos mitades: {results['general']['split_half']['spearman_brown_coefficient']:.3f}")
    print(f"KMO: {results['general']['kmo']['kmo_global']:.3f}")
    
    # Mostrar resultados de VALIDEZ
    print("\n✅ VALIDEZ:")
    
    # Validez convergente
    for dim_name in dimensiones.keys():
        if f'{dim_name}_convergent' in results['validity']:
            conv = results['validity'][f'{dim_name}_convergent']
            print(f"\nValidez Convergente - {dim_name}:")
            print(f"  Correlación promedio: r = {conv['mean_correlation']:.3f}")
            print(f"  Interpretación: {conv['interpretation']}")
    
    # Validez discriminante
    if 'discriminant' in results['validity']:
        disc = results['validity']['discriminant']
        print(f"\nValidez Discriminante:")
        print(f"  Correlación entre dimensiones: r = {disc['correlation_between_dimensions']:.3f}")
        print(f"  Interpretación: {disc['interpretation']}")


def ejemplo_validez_contenido():
    """
    Ejemplo 3: Validez de Contenido con juicio de expertos
    """
    print("\n\n")
    print("=" * 80)
    print("EJEMPLO 3: VALIDEZ DE CONTENIDO (Juicio de Expertos)")
    print("=" * 80)
    
    # Cargar datos
    loader = DataLoader()
    try:
        data, metadata = loader.load_spss(str(config.SPSS_FILE))
    except:
        print("⚠ No se pudo cargar el archivo SPSS")
        return
    
    # EJEMPLO: Datos de juicio de expertos
    # En la realidad, estos datos vendrían de tus jueces
    # Valores 1-4 donde 3-4 = relevante
    judges_ratings = pd.DataFrame({
        'Juez1': [4, 4, 3, 4, 3],
        'Juez2': [4, 3, 4, 4, 4],
        'Juez3': [3, 4, 4, 3, 4],
        'Juez4': [4, 4, 4, 4, 3],
        'Juez5': [4, 3, 4, 4, 4]
    }, index=['Item1', 'Item2', 'Item3', 'Item4', 'Item5'])
    
    print("\n📋 Calificaciones de expertos:")
    print(judges_ratings)
    
    # Calcular IVC
    analyzer = ReliabilityAnalyzer(data)
    ivc_result = analyzer.content_validity_index(judges_ratings)
    
    if ivc_result:
        print(f"\n📊 RESULTADOS:")
        print(f"IVC Total: {ivc_result['ivc_total']:.3f}")
        print(f"Interpretación: {ivc_result['interpretation']}")
        print(f"Número de jueces: {ivc_result['n_judges']}")
        print(f"Número de ítems: {ivc_result['n_items']}")
        
        print("\nIVC por ítem:")
        for item, ivc in ivc_result['ivc_by_item'].items():
            print(f"  {item}: {ivc:.3f}")


def ejemplo_validez_criterio():
    """
    Ejemplo 4: Validez de Criterio
    """
    print("\n\n")
    print("=" * 80)
    print("EJEMPLO 4: VALIDEZ DE CRITERIO")
    print("=" * 80)
    
    # Cargar datos
    loader = DataLoader()
    try:
        data, metadata = loader.load_spss(str(config.SPSS_FILE))
    except:
        print("⚠ No se pudo cargar el archivo SPSS")
        return
    
    # Mostrar columnas disponibles
    print("\n📋 Columnas disponibles en tus datos:")
    print(list(data.columns)[:20], "...")
    
    print("\n⚠ NOTA: Para usar validez de criterio necesitas:")
    print("  1. Una variable criterio externa (ej: 'Promedio_Calificaciones')")
    print("  2. Que esa variable esté en tus datos")
    print("\nEjemplo de uso:")
    print("""
    items_instrumento = ['P1', 'P2', 'P3', 'P4', 'P5']
    variable_criterio = 'Promedio_Calificaciones'
    
    analyzer = ReliabilityAnalyzer(data)
    result = analyzer.criterion_validity(items_instrumento, variable_criterio)
    
    print(f"Correlación con criterio: r = {result['correlation_with_criterion']:.3f}")
    print(f"Significancia: p = {result['p_value']:.4f}")
    print(f"Interpretación: {result['interpretation']}")
    """)


def ejemplo_todos_los_metodos():
    """
    Ejemplo 5: Demostración de todos los métodos individuales
    """
    print("\n\n")
    print("=" * 80)
    print("EJEMPLO 5: TODOS LOS MÉTODOS DISPONIBLES")
    print("=" * 80)
    
    # Cargar datos
    loader = DataLoader()
    try:
        data, metadata = loader.load_spss(str(config.SPSS_FILE))
    except:
        print("⚠ No se pudo cargar el archivo SPSS")
        return
    
    analyzer = ReliabilityAnalyzer(data)
    items_ejemplo = ['P1', 'P2', 'P3', 'P4', 'P5']  # Cambia por tus ítems reales
    
    print("\n📚 MÉTODOS DE CONFIABILIDAD:")
    print("  1. cronbach_alpha(items)")
    print("  2. split_half_reliability(items)")
    print("  3. kmo_test(items)")
    print("  4. bartlett_test(items)")
    
    print("\n✅ MÉTODOS DE VALIDEZ:")
    print("  5. content_validity_index(judges_ratings)")
    print("  6. construct_validity_factorial(items, n_factors)")
    print("  7. convergent_validity(items_dimension)")
    print("  8. discriminant_validity(dimension1_items, dimension2_items)")
    print("  9. criterion_validity(predictor_items, criterion_var)")
    
    print("\n🎯 MÉTODO PRINCIPAL:")
    print("  10. comprehensive_reliability_validity(dimensions, include_validity, criterion_variable)")
    
    print("\n💡 RECOMENDACIÓN:")
    print("  Usa comprehensive_reliability_validity() para análisis completo automático")
    print("  O usa métodos individuales para análisis específicos")


def main():
    """
    Función principal que ejecuta todos los ejemplos.
    """
    print("\n" + "=" * 80)
    print("EJEMPLOS DE USO: ANÁLISIS DE CONFIABILIDAD Y VALIDEZ")
    print("Metodología: Hernández-Sampieri et al. (2014)")
    print("=" * 80)
    
    print("\n⚠️  IMPORTANTE:")
    print("Estos son EJEMPLOS. Debes ajustarlos con:")
    print("  1. Tus columnas reales de datos")
    print("  2. Tus dimensiones específicas")
    print("  3. Tu variable criterio (si la tienes)")
    
    print("\n📝 Para ejecutar cada ejemplo:")
    print("  - Descomenta la función que quieras probar")
    print("  - Ajusta las columnas con tus datos reales")
    print("  - Ejecuta: python ejemplo_validez.py")
    
    # DESCOMENTA EL EJEMPLO QUE QUIERAS EJECUTAR:
    
    # ejemplo_confiabilidad_basica()
    # ejemplo_confiabilidad_validez_completo()
    # ejemplo_validez_contenido()
    # ejemplo_validez_criterio()
    ejemplo_todos_los_metodos()
    
    print("\n" + "=" * 80)
    print("✅ EJEMPLOS COMPLETADOS")
    print("=" * 80)
    print("\nPróximos pasos:")
    print("  1. Explora tus datos: python explorar_datos.py")
    print("  2. Define tus DIMENSIONES en main.py")
    print("  3. Ejecuta análisis completo: python main.py")
    print("\n📖 Consulta ANALISIS_CONFIABILIDAD_VALIDEZ.md para más detalles")


if __name__ == "__main__":
    main()
