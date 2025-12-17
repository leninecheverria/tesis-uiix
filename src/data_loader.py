"""
Módulo de carga de datos para análisis de tesis.

Este módulo proporciona funciones para cargar y preprocesar datos
desde archivos SPSS (.sav) y Excel (.xls/.xlsx).

Autor: Sistema de Análisis de Tesis
Fecha: Diciembre 2025
"""

import pandas as pd
import numpy as np
import pyreadstat
import logging
from pathlib import Path
from typing import Tuple, Dict, Optional, List

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataLoader:
    """
    Clase para cargar y gestionar datos de la encuesta.
    
    Atributos:
        data (pd.DataFrame): DataFrame con los datos cargados
        metadata (dict): Metadatos del archivo (etiquetas, tipos, etc.)
        source_file (Path): Ruta del archivo fuente
    """
    
    def __init__(self):
        """Inicializa el cargador de datos."""
        self.data = None
        self.metadata = None
        self.source_file = None
        self.variable_labels = {}
        self.value_labels = {}
        
    def load_spss(self, file_path: str) -> Tuple[pd.DataFrame, Dict]:
        """
        Carga un archivo SPSS (.sav) y extrae sus metadatos.
        
        Args:
            file_path (str): Ruta al archivo .sav
            
        Returns:
            Tuple[pd.DataFrame, Dict]: DataFrame con los datos y diccionario con metadatos
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            Exception: Si hay error al leer el archivo
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                raise FileNotFoundError(f"El archivo no existe: {file_path}")
            
            logger.info(f"Cargando archivo SPSS: {file_path}")
            
            # Leer archivo SPSS con metadatos
            df, meta = pyreadstat.read_sav(
                str(file_path),
                apply_value_formats=False,  # Mantener valores numéricos
                formats_as_ordered_category=False
            )
            
            # Guardar datos y metadatos
            self.data = df
            self.source_file = file_path
            self.variable_labels = meta.column_names_to_labels
            self.value_labels = meta.variable_value_labels
            
            # Crear diccionario de metadatos estructurado
            self.metadata = {
                'n_variables': len(df.columns),
                'n_observations': len(df),
                'variable_names': list(df.columns),
                'variable_labels': meta.column_names_to_labels,
                'value_labels': meta.variable_value_labels,
                'variable_types': df.dtypes.to_dict(),
                'missing_values': df.isnull().sum().to_dict(),
                'file_encoding': meta.file_encoding,
                'creation_date': getattr(meta, 'creation_date', None),
            }
            
            logger.info(f"✓ Archivo cargado exitosamente")
            logger.info(f"  - Variables: {self.metadata['n_variables']}")
            logger.info(f"  - Observaciones: {self.metadata['n_observations']}")
            
            return self.data, self.metadata
            
        except FileNotFoundError as e:
            logger.error(f"✗ {str(e)}")
            raise
        except Exception as e:
            logger.error(f"✗ Error al cargar archivo SPSS: {str(e)}")
            raise
    
    def load_excel(self, file_path: str, sheet_name: int = 0) -> pd.DataFrame:
        """
        Carga un archivo Excel (.xls o .xlsx).
        
        Args:
            file_path (str): Ruta al archivo Excel
            sheet_name (int): Número de hoja a cargar (por defecto 0)
            
        Returns:
            pd.DataFrame: DataFrame con los datos
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            Exception: Si hay error al leer el archivo
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                raise FileNotFoundError(f"El archivo no existe: {file_path}")
            
            logger.info(f"Cargando archivo Excel: {file_path}")
            
            # Leer archivo Excel
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Guardar datos
            self.data = df
            self.source_file = file_path
            
            # Crear metadatos básicos
            self.metadata = {
                'n_variables': len(df.columns),
                'n_observations': len(df),
                'variable_names': list(df.columns),
                'variable_types': df.dtypes.to_dict(),
                'missing_values': df.isnull().sum().to_dict(),
            }
            
            logger.info(f"✓ Archivo cargado exitosamente")
            logger.info(f"  - Variables: {self.metadata['n_variables']}")
            logger.info(f"  - Observaciones: {self.metadata['n_observations']}")
            
            return self.data
            
        except FileNotFoundError as e:
            logger.error(f"✗ {str(e)}")
            raise
        except Exception as e:
            logger.error(f"✗ Error al cargar archivo Excel: {str(e)}")
            raise
    
    def get_data_summary(self) -> pd.DataFrame:
        """
        Genera un resumen descriptivo de los datos cargados.
        
        Returns:
            pd.DataFrame: Resumen con estadísticas descriptivas
        """
        if self.data is None:
            logger.warning("No hay datos cargados")
            return None
        
        summary = pd.DataFrame({
            'Variable': self.data.columns,
            'Tipo': self.data.dtypes.values,
            'No Nulos': self.data.count().values,
            'Nulos': self.data.isnull().sum().values,
            '% Nulos': (self.data.isnull().sum() / len(self.data) * 100).round(2).values,
            'Únicos': [self.data[col].nunique() for col in self.data.columns],
        })
        
        # Agregar etiquetas si existen (de SPSS)
        if self.variable_labels:
            summary['Etiqueta'] = summary['Variable'].map(self.variable_labels)
        
        return summary
    
    def get_variable_info(self, variable: str) -> Dict:
        """
        Obtiene información detallada de una variable específica.
        
        Args:
            variable (str): Nombre de la variable
            
        Returns:
            Dict: Diccionario con información de la variable
        """
        if self.data is None or variable not in self.data.columns:
            logger.warning(f"Variable '{variable}' no encontrada")
            return None
        
        info = {
            'nombre': variable,
            'tipo': str(self.data[variable].dtype),
            'n_validos': self.data[variable].count(),
            'n_nulos': self.data[variable].isnull().sum(),
            'n_unicos': self.data[variable].nunique(),
        }
        
        # Agregar etiqueta si existe
        if variable in self.variable_labels:
            info['etiqueta'] = self.variable_labels[variable]
        
        # Agregar etiquetas de valores si existen
        if variable in self.value_labels:
            info['etiquetas_valores'] = self.value_labels[variable]
        
        # Estadísticas para variables numéricas
        if pd.api.types.is_numeric_dtype(self.data[variable]):
            info['estadisticas'] = {
                'media': self.data[variable].mean(),
                'mediana': self.data[variable].median(),
                'std': self.data[variable].std(),
                'min': self.data[variable].min(),
                'max': self.data[variable].max(),
            }
        
        # Frecuencias para variables categóricas o con pocos valores únicos
        if info['n_unicos'] <= 20:
            info['frecuencias'] = self.data[variable].value_counts().to_dict()
        
        return info
    
    def filter_numeric_columns(self, exclude_patterns: Optional[List[str]] = None) -> List[str]:
        """
        Filtra y retorna las columnas numéricas, excluyendo patrones específicos.
        
        Args:
            exclude_patterns (List[str]): Lista de patrones a excluir (ej: ['ID', 'Timestamp'])
            
        Returns:
            List[str]: Lista de nombres de columnas numéricas
        """
        if self.data is None:
            return []
        
        # Obtener columnas numéricas
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        # Excluir patrones si se especifican
        if exclude_patterns:
            numeric_cols = [
                col for col in numeric_cols 
                if not any(pattern.lower() in col.lower() for pattern in exclude_patterns)
            ]
        
        return numeric_cols
    
    def clean_data(self, 
                   drop_na_threshold: float = 0.5,
                   drop_duplicates: bool = True) -> pd.DataFrame:
        """
        Limpia los datos según criterios especificados.
        
        Args:
            drop_na_threshold (float): Umbral de valores nulos (0-1) para eliminar columnas
            drop_duplicates (bool): Si se deben eliminar filas duplicadas
            
        Returns:
            pd.DataFrame: DataFrame limpio
        """
        if self.data is None:
            logger.warning("No hay datos para limpiar")
            return None
        
        logger.info("Iniciando limpieza de datos...")
        df_clean = self.data.copy()
        
        # Eliminar columnas con muchos valores nulos
        null_ratio = df_clean.isnull().sum() / len(df_clean)
        cols_to_drop = null_ratio[null_ratio > drop_na_threshold].index.tolist()
        
        if cols_to_drop:
            logger.info(f"Eliminando {len(cols_to_drop)} columnas con >{drop_na_threshold*100}% nulos: {cols_to_drop}")
            df_clean = df_clean.drop(columns=cols_to_drop)
        
        # Eliminar filas duplicadas
        if drop_duplicates:
            n_duplicates = df_clean.duplicated().sum()
            if n_duplicates > 0:
                logger.info(f"Eliminando {n_duplicates} filas duplicadas")
                df_clean = df_clean.drop_duplicates()
        
        logger.info(f"✓ Limpieza completada. Shape final: {df_clean.shape}")
        
        return df_clean
    
    def export_to_excel(self, output_path: str, include_summary: bool = True):
        """
        Exporta los datos a un archivo Excel.
        
        Args:
            output_path (str): Ruta del archivo de salida
            include_summary (bool): Si se debe incluir una hoja con resumen
        """
        if self.data is None:
            logger.warning("No hay datos para exportar")
            return
        
        try:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                # Exportar datos
                self.data.to_excel(writer, sheet_name='Datos', index=False)
                
                # Exportar resumen si se solicita
                if include_summary:
                    summary = self.get_data_summary()
                    summary.to_excel(writer, sheet_name='Resumen', index=False)
                
            logger.info(f"✓ Datos exportados a: {output_path}")
            
        except Exception as e:
            logger.error(f"✗ Error al exportar datos: {str(e)}")
            raise


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def quick_load_spss(file_path: str) -> Tuple[pd.DataFrame, Dict]:
    """
    Función rápida para cargar un archivo SPSS.
    
    Args:
        file_path (str): Ruta al archivo .sav
        
    Returns:
        Tuple[pd.DataFrame, Dict]: Datos y metadatos
    """
    loader = DataLoader()
    return loader.load_spss(file_path)


def quick_load_excel(file_path: str) -> pd.DataFrame:
    """
    Función rápida para cargar un archivo Excel.
    
    Args:
        file_path (str): Ruta al archivo Excel
        
    Returns:
        pd.DataFrame: Datos cargados
    """
    loader = DataLoader()
    return loader.load_excel(file_path)


def compare_datasets(df1: pd.DataFrame, df2: pd.DataFrame) -> Dict:
    """
    Compara dos datasets y retorna las diferencias.
    
    Args:
        df1 (pd.DataFrame): Primer dataset
        df2 (pd.DataFrame): Segundo dataset
        
    Returns:
        Dict: Diccionario con las diferencias encontradas
    """
    comparison = {
        'shape_df1': df1.shape,
        'shape_df2': df2.shape,
        'columns_only_df1': list(set(df1.columns) - set(df2.columns)),
        'columns_only_df2': list(set(df2.columns) - set(df1.columns)),
        'common_columns': list(set(df1.columns) & set(df2.columns)),
    }
    
    return comparison
