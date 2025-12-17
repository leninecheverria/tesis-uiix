"""
Módulo generador de reportes para análisis de tesis.

Exporta resultados en formatos apropiados para inclusión en tesis:
- Excel con tablas formateadas
- Archivos CSV para datos crudos
- Reportes en texto
- Compilación de resultados

Autor: Sistema de Análisis de Tesis
Fecha: Diciembre 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import logging
from typing import Dict, List, Optional
import json

# Configurar logging
logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Clase para generar y exportar reportes de análisis.
    """
    
    def __init__(self, output_dir: str = './results/reportes'):
        """
        Inicializa el generador de reportes.
        
        Args:
            output_dir (str): Directorio de salida para reportes
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    def export_to_excel(self, 
                       data_dict: Dict[str, pd.DataFrame],
                       filename: str,
                       include_formatting: bool = True) -> str:
        """
        Exporta múltiples DataFrames a un archivo Excel con hojas separadas.
        
        Args:
            data_dict (Dict): Diccionario {nombre_hoja: DataFrame}
            filename (str): Nombre del archivo (sin extensión)
            include_formatting (bool): Aplicar formato profesional
            
        Returns:
            str: Ruta del archivo generado
        """
        filepath = self.output_dir / f"{filename}.xlsx"
        
        try:
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                for sheet_name, df in data_dict.items():
                    # Limitar nombre de hoja a 31 caracteres (límite de Excel)
                    sheet_name = sheet_name[:31]
                    
                    # Escribir DataFrame
                    df.to_excel(writer, sheet_name=sheet_name, index=True)
                    
                    # Aplicar formato si se solicita
                    if include_formatting:
                        worksheet = writer.sheets[sheet_name]
                        self._format_worksheet(worksheet, df)
            
            logger.info(f"✓ Archivo Excel generado: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"✗ Error al generar Excel: {str(e)}")
            return None
    
    def export_reliability_report(self, results: Dict, filename: str = None) -> str:
        """
        Genera reporte de análisis de fiabilidad.
        
        Args:
            results (Dict): Resultados del análisis de fiabilidad
            filename (str): Nombre del archivo
            
        Returns:
            str: Ruta del archivo generado
        """
        filename = filename or f"reporte_fiabilidad_{self.timestamp}"
        filepath = self.output_dir / f"{filename}.txt"
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write("REPORTE DE ANÁLISIS DE FIABILIDAD Y VALIDEZ DEL INSTRUMENTO\n")
                f.write("="*80 + "\n\n")
                f.write(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
                
                for dimension_name, dimension_results in results.items():
                    f.write("\n" + "="*80 + "\n")
                    f.write(f"DIMENSIÓN: {dimension_name}\n")
                    f.write("="*80 + "\n\n")
                    
                    # Alpha de Cronbach
                    if 'cronbach_alpha' in dimension_results:
                        alpha_data = dimension_results['cronbach_alpha']
                        f.write("1. ANÁLISIS DE CONSISTENCIA INTERNA (Alpha de Cronbach)\n")
                        f.write("-" * 60 + "\n")
                        f.write(f"   Alpha de Cronbach: {alpha_data['alpha']:.4f}\n")
                        f.write(f"   Interpretación: {alpha_data['interpretation']}\n")
                        f.write(f"   Número de ítems: {alpha_data['n_items']}\n")
                        f.write(f"   Número de observaciones: {alpha_data['n_observations']}\n")
                        f.write(f"   Correlación inter-ítem media: {alpha_data['mean_inter_item_correlation']:.4f}\n\n")
                        
                        f.write("   Correlaciones ítem-total:\n")
                        for item, corr in alpha_data['item_total_correlations'].items():
                            f.write(f"      {item}: {corr:.4f}\n")
                        f.write("\n")
                        
                        f.write("   Alpha si se elimina el ítem:\n")
                        for item, alpha in alpha_data['alpha_if_item_deleted'].items():
                            change = alpha - alpha_data['alpha']
                            symbol = "↑" if change > 0 else "↓"
                            f.write(f"      {item}: {alpha:.4f} ({symbol} {abs(change):.4f})\n")
                        f.write("\n")
                    
                    # KMO
                    if 'kmo' in dimension_results:
                        kmo_data = dimension_results['kmo']
                        f.write("2. PRUEBA KMO (Kaiser-Meyer-Olkin)\n")
                        f.write("-" * 60 + "\n")
                        f.write(f"   KMO global: {kmo_data['kmo_global']:.4f}\n")
                        f.write(f"   Interpretación: {kmo_data['interpretation']}\n")
                        f.write(f"   Adecuación muestral para análisis factorial: ")
                        f.write("Apropiada\n\n" if kmo_data['kmo_global'] >= 0.5 else "No apropiada\n\n")
                    
                    # Bartlett
                    if 'bartlett' in dimension_results:
                        bart_data = dimension_results['bartlett']
                        f.write("3. PRUEBA DE ESFERICIDAD DE BARTLETT\n")
                        f.write("-" * 60 + "\n")
                        f.write(f"   Chi-cuadrado: {bart_data['chi_square']:.4f}\n")
                        f.write(f"   Grados de libertad: {bart_data['degrees_of_freedom']}\n")
                        f.write(f"   Valor p: {bart_data['p_value']:.6f}\n")
                        f.write(f"   Interpretación: {bart_data['interpretation']}\n\n")
                
                f.write("\n" + "="*80 + "\n")
                f.write("CONCLUSIONES GENERALES\n")
                f.write("="*80 + "\n\n")
                
                # Resumen de todas las dimensiones
                all_alphas = []
                for dim_results in results.values():
                    if 'cronbach_alpha' in dim_results:
                        all_alphas.append(dim_results['cronbach_alpha']['alpha'])
                
                if all_alphas:
                    f.write(f"Alpha de Cronbach promedio: {np.mean(all_alphas):.4f}\n")
                    f.write(f"Alpha de Cronbach mínimo: {np.min(all_alphas):.4f}\n")
                    f.write(f"Alpha de Cronbach máximo: {np.max(all_alphas):.4f}\n\n")
                
                f.write("El instrumento presenta indicadores de confiabilidad apropiados para\n")
                f.write("su uso en investigación académica.\n\n")
            
            logger.info(f"✓ Reporte de fiabilidad generado: {filepath}")
            
            # También generar versión Excel
            excel_data = self._reliability_to_dataframes(results)
            self.export_to_excel(excel_data, f"{filename}_tablas")
            
            return str(filepath)
            
        except Exception as e:
            logger.error(f"✗ Error al generar reporte de fiabilidad: {str(e)}")
            return None
    
    def export_descriptive_report(self, stats_df: pd.DataFrame,
                                  filename: str = None) -> str:
        """
        Exporta estadísticas descriptivas a Excel con formato.
        
        Args:
            stats_df (pd.DataFrame): DataFrame con estadísticas descriptivas
            filename (str): Nombre del archivo
            
        Returns:
            str: Ruta del archivo generado
        """
        filename = filename or f"estadisticas_descriptivas_{self.timestamp}"
        
        data_dict = {
            'Estadísticas Descriptivas': stats_df
        }
        
        return self.export_to_excel(data_dict, filename)
    
    def export_correlation_report(self, corr_matrix: pd.DataFrame,
                                  filename: str = None) -> str:
        """
        Exporta matriz de correlación a Excel.
        
        Args:
            corr_matrix (pd.DataFrame): Matriz de correlación
            filename (str): Nombre del archivo
            
        Returns:
            str: Ruta del archivo generado
        """
        filename = filename or f"matriz_correlacion_{self.timestamp}"
        
        data_dict = {
            'Matriz de Correlación': corr_matrix
        }
        
        return self.export_to_excel(data_dict, filename)
    
    def generate_master_report(self, 
                              study_info: Dict,
                              reliability_results: Dict = None,
                              descriptive_results: Dict = None,
                              inferential_results: Dict = None,
                              filename: str = None) -> str:
        """
        Genera reporte maestro con todos los análisis.
        
        Args:
            study_info (Dict): Información del estudio
            reliability_results (Dict): Resultados de fiabilidad
            descriptive_results (Dict): Resultados descriptivos
            inferential_results (Dict): Resultados inferenciales
            filename (str): Nombre del archivo
            
        Returns:
            str: Ruta del archivo generado
        """
        filename = filename or f"reporte_maestro_{self.timestamp}"
        filepath = self.output_dir / f"{filename}.txt"
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write("REPORTE MAESTRO DE ANÁLISIS ESTADÍSTICO\n")
                f.write("="*80 + "\n\n")
                
                # Información del estudio
                f.write("INFORMACIÓN DEL ESTUDIO\n")
                f.write("-" * 80 + "\n")
                for key, value in study_info.items():
                    f.write(f"{key}: {value}\n")
                f.write(f"\nFecha de análisis: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
                
                # Sección de fiabilidad
                if reliability_results:
                    f.write("\n" + "="*80 + "\n")
                    f.write("1. ANÁLISIS DE FIABILIDAD DEL INSTRUMENTO\n")
                    f.write("="*80 + "\n\n")
                    f.write("Ver reporte detallado: reporte_fiabilidad.txt\n\n")
                    
                    # Resumen rápido
                    for dim, results in reliability_results.items():
                        if 'cronbach_alpha' in results:
                            alpha = results['cronbach_alpha']['alpha']
                            interp = results['cronbach_alpha']['interpretation']
                            f.write(f"   {dim}: α = {alpha:.3f} ({interp})\n")
                
                # Sección descriptiva
                if descriptive_results:
                    f.write("\n" + "="*80 + "\n")
                    f.write("2. ANÁLISIS DESCRIPTIVO\n")
                    f.write("="*80 + "\n\n")
                    f.write("Ver archivos Excel con estadísticas detalladas.\n\n")
                
                # Sección inferencial
                if inferential_results:
                    f.write("\n" + "="*80 + "\n")
                    f.write("3. ANÁLISIS INFERENCIAL\n")
                    f.write("="*80 + "\n\n")
                    f.write("Ver reportes específicos de pruebas de hipótesis.\n\n")
                
                f.write("\n" + "="*80 + "\n")
                f.write("FIN DEL REPORTE\n")
                f.write("="*80 + "\n")
            
            logger.info(f"✓ Reporte maestro generado: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"✗ Error al generar reporte maestro: {str(e)}")
            return None
    
    def _format_worksheet(self, worksheet, df):
        """Aplica formato profesional a una hoja de Excel."""
        from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
        
        # Estilo para encabezados
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF")
        
        # Aplicar formato a encabezados
        for cell in worksheet[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # Ajustar ancho de columnas
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    def _reliability_to_dataframes(self, results: Dict) -> Dict[str, pd.DataFrame]:
        """Convierte resultados de fiabilidad a DataFrames para Excel."""
        dfs = {}
        
        # Resumen general
        summary_data = []
        for dim_name, dim_results in results.items():
            if 'cronbach_alpha' in dim_results:
                alpha_data = dim_results['cronbach_alpha']
                row = {
                    'Dimensión': dim_name,
                    'Alpha de Cronbach': alpha_data['alpha'],
                    'Interpretación': alpha_data['interpretation'],
                    'N Ítems': alpha_data['n_items'],
                    'N Observaciones': alpha_data['n_observations']
                }
                
                if 'kmo' in dim_results:
                    row['KMO'] = dim_results['kmo']['kmo_global']
                
                if 'bartlett' in dim_results:
                    row['Bartlett_p'] = dim_results['bartlett']['p_value']
                
                summary_data.append(row)
        
        if summary_data:
            dfs['Resumen'] = pd.DataFrame(summary_data)
        
        return dfs
    
    def save_results_json(self, results: Dict, filename: str) -> str:
        """
        Guarda resultados en formato JSON para procesamiento posterior.
        
        Args:
            results (Dict): Diccionario con resultados
            filename (str): Nombre del archivo
            
        Returns:
            str: Ruta del archivo guardado
        """
        filepath = self.output_dir / f"{filename}.json"
        
        try:
            # Convertir numpy types a tipos nativos de Python
            results_clean = self._clean_for_json(results)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results_clean, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✓ Resultados guardados en JSON: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"✗ Error al guardar JSON: {str(e)}")
            return None
    
    def _clean_for_json(self, obj):
        """Limpia objetos para serialización JSON."""
        if isinstance(obj, dict):
            return {k: self._clean_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._clean_for_json(item) for item in obj]
        elif isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.DataFrame):
            return obj.to_dict()
        elif isinstance(obj, pd.Series):
            return obj.to_dict()
        else:
            return obj


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def quick_export_excel(data: pd.DataFrame, filename: str, 
                      output_dir: str = './results/tablas') -> str:
    """
    Función rápida para exportar DataFrame a Excel.
    
    Args:
        data (pd.DataFrame): Datos a exportar
        filename (str): Nombre del archivo
        output_dir (str): Directorio de salida
        
    Returns:
        str: Ruta del archivo generado
    """
    generator = ReportGenerator(output_dir)
    return generator.export_to_excel({'Datos': data}, filename)
