#!/usr/bin/env python3
"""
Script de exploración rápida de datos.

Ejecuta este script primero para conocer tus datos antes del análisis completo.
Te ayudará a identificar:
- Nombres de variables
- Tipos de datos
- Valores faltantes
- Distribución de datos

Autor: Sistema de Análisis de Tesis
Fecha: Diciembre 2025
"""

import sys
from pathlib import Path

# Agregar directorios al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))
sys.path.insert(0, str(Path(__file__).parent))

from src.data_loader import DataLoader
from config import config
import pandas as pd


def main():
    """Función principal de exploración."""
    print("="*80)
    print("EXPLORACIÓN RÁPIDA DE DATOS")
    print("="*80)
    print()
    
    # Cargar datos
    loader = DataLoader()
    
    try:
        print("Intentando cargar archivo SPSS...")
        data, metadata = loader.load_spss(str(config.SPSS_FILE))
        print("✓ Archivo SPSS cargado exitosamente\n")
        
    except Exception as e:
        print(f"No se pudo cargar SPSS: {e}")
        print("Intentando Excel...")
        try:
            data = loader.load_excel(str(config.EXCEL_FILE))
            metadata = loader.metadata
            print("✓ Archivo Excel cargado exitosamente\n")
        except Exception as e:
            print(f"✗ Error: {e}")
            return
    
    # Información básica
    print("="*80)
    print("INFORMACIÓN GENERAL")
    print("="*80)
    print(f"Número de observaciones (filas): {len(data)}")
    print(f"Número de variables (columnas): {len(data.columns)}")
    print()
    
    # Tipos de variables
    print("="*80)
    print("TIPOS DE VARIABLES")
    print("="*80)
    numeric_cols = data.select_dtypes(include=['number']).columns
    categorical_cols = data.select_dtypes(exclude=['number']).columns
    
    print(f"Variables numéricas: {len(numeric_cols)}")
    print(f"Variables categóricas/texto: {len(categorical_cols)}")
    print()
    
    # Mostrar todas las variables
    print("="*80)
    print("LISTA COMPLETA DE VARIABLES")
    print("="*80)
    print()
    
    for i, col in enumerate(data.columns, 1):
        # Obtener tipo
        dtype = data[col].dtype
        
        # Obtener etiqueta si existe (SPSS)
        label = ""
        if hasattr(loader, 'variable_labels') and col in loader.variable_labels:
            label = f" - {loader.variable_labels[col]}"
        
        # Contar valores únicos y nulos
        n_unique = data[col].nunique()
        n_null = data[col].isnull().sum()
        pct_null = (n_null / len(data) * 100)
        
        print(f"{i:3d}. {col:30s} | Tipo: {str(dtype):12s} | "
              f"Únicos: {n_unique:4d} | Nulos: {n_null:4d} ({pct_null:5.1f}%){label}")
    
    print()
    
    # Valores faltantes
    print("="*80)
    print("VARIABLES CON VALORES FALTANTES")
    print("="*80)
    missing = data.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    
    if len(missing) > 0:
        print(f"\nSe encontraron {len(missing)} variables con valores faltantes:\n")
        for var, count in missing.items():
            pct = (count / len(data) * 100)
            print(f"  {var:30s}: {count:4d} ({pct:5.1f}%)")
    else:
        print("\n✓ No hay valores faltantes en ninguna variable")
    
    print()
    
    # Variables numéricas - muestra de estadísticas
    print("="*80)
    print("ESTADÍSTICAS BÁSICAS (Primeras 5 variables numéricas)")
    print("="*80)
    print()
    
    if len(numeric_cols) > 0:
        sample_vars = numeric_cols[:5]
        stats = data[sample_vars].describe().T
        
        pd.set_option('display.float_format', '{:.2f}'.format)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        
        print(stats)
        print()
        print(f"(Mostrando solo 5 de {len(numeric_cols)} variables numéricas)")
    else:
        print("No se encontraron variables numéricas")
    
    print()
    
    # Variables categóricas - muestra
    print("="*80)
    print("VALORES ÚNICOS (Primeras 3 variables categóricas)")
    print("="*80)
    print()
    
    if len(categorical_cols) > 0:
        for col in categorical_cols[:3]:
            unique_vals = data[col].value_counts()
            print(f"\n{col}:")
            print(unique_vals.head(10))
            if len(unique_vals) > 10:
                print(f"... ({len(unique_vals) - 10} valores más)")
    else:
        print("No se encontraron variables categóricas")
    
    print()
    
    # Recomendaciones
    print("="*80)
    print("RECOMENDACIONES PARA EL ANÁLISIS")
    print("="*80)
    print()
    
    print("1. DEFINIR DIMENSIONES:")
    print("   Identifica qué variables pertenecen a cada dimensión de tu instrumento")
    print("   y actualiza la variable DIMENSIONES en main.py")
    print()
    
    print("2. VARIABLES PARA ANÁLISIS:")
    print(f"   - Considera usar las {len(numeric_cols)} variables numéricas")
    print("   - Excluye variables ID, timestamp, o similares")
    print()
    
    if len(missing) > 0:
        print("3. VALORES FALTANTES:")
        print("   - Decide cómo manejar los valores faltantes")
        print("   - Opciones: eliminar casos, imputar valores, o analizar por separado")
        print()
    
    print("4. SIGUIENTE PASO:")
    print("   Ejecuta: python main.py")
    print("   para realizar el análisis completo")
    print()
    
    # Exportar resumen
    print("="*80)
    print("EXPORTANDO RESUMEN")
    print("="*80)
    
    summary = loader.get_data_summary()
    output_file = config.TABLES_DIR / "exploracion_datos.xlsx"
    
    try:
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            summary.to_excel(writer, sheet_name='Resumen', index=False)
            
            if len(numeric_cols) > 0:
                data[numeric_cols].describe().T.to_excel(
                    writer, sheet_name='Estadísticas Numéricas'
                )
        
        print(f"\n✓ Resumen exportado a: {output_file}")
        print("  Revisa este archivo para mayor detalle")
        
    except Exception as e:
        print(f"\n⚠ No se pudo exportar: {e}")
    
    print()
    print("="*80)
    print("EXPLORACIÓN COMPLETADA")
    print("="*80)


if __name__ == "__main__":
    main()
