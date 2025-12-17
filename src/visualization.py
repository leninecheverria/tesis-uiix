"""
Módulo de visualización de datos para análisis de tesis.

Genera gráficos profesionales y atractivos para presentación en tesis,
con estilo académico y alta resolución.

Autor: Sistema de Análisis de Tesis
Fecha: Diciembre 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path
import logging
from typing import Dict, List, Optional, Tuple

# Configurar logging
logger = logging.getLogger(__name__)

# Configuración de estilo para gráficos académicos
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("Set2")


class DataVisualizer:
    """
    Clase para crear visualizaciones profesionales de datos.
    """
    
    def __init__(self, output_dir: str = './results/graficos', dpi: int = 300):
        """
        Inicializa el visualizador.
        
        Args:
            output_dir (str): Directorio para guardar gráficos
            dpi (int): Resolución de las imágenes (300 para tesis)
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.dpi = dpi
        
        # Configuración de fuentes para aspecto profesional
        plt.rcParams['font.family'] = 'serif'
        plt.rcParams['font.size'] = 11
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        plt.rcParams['legend.fontsize'] = 10
        plt.rcParams['figure.titlesize'] = 16
    
    def histogram(self, data: pd.Series, 
                  title: str = None,
                  xlabel: str = None,
                  bins: int = 30,
                  show_normal: bool = True,
                  filename: str = None) -> str:
        """
        Crea un histograma con curva de densidad.
        
        Args:
            data (pd.Series): Datos a graficar
            title (str): Título del gráfico
            xlabel (str): Etiqueta del eje X
            bins (int): Número de bins
            show_normal (bool): Mostrar curva normal de referencia
            filename (str): Nombre del archivo a guardar
            
        Returns:
            str: Ruta del archivo guardado
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Histograma
        data_clean = data.dropna()
        n, bins_edges, patches = ax.hist(data_clean, bins=bins, 
                                         density=True, alpha=0.7,
                                         color='steelblue', edgecolor='black')
        
        # Curva de densidad
        density = stats.gaussian_kde(data_clean)
        x_range = np.linspace(data_clean.min(), data_clean.max(), 100)
        ax.plot(x_range, density(x_range), 'r-', linewidth=2, 
               label='Densidad estimada')
        
        # Curva normal de referencia
        if show_normal:
            mu, std = data_clean.mean(), data_clean.std()
            normal_curve = stats.norm.pdf(x_range, mu, std)
            ax.plot(x_range, normal_curve, 'g--', linewidth=2, 
                   label='Distribución normal')
        
        # Estadísticas en el gráfico
        textstr = f'N = {len(data_clean)}\n'
        textstr += f'Media = {data_clean.mean():.2f}\n'
        textstr += f'Mediana = {data_clean.median():.2f}\n'
        textstr += f'D.E. = {data_clean.std():.2f}'
        ax.text(0.02, 0.98, textstr, transform=ax.transAxes,
               verticalalignment='top', bbox=dict(boxstyle='round',
               facecolor='wheat', alpha=0.5))
        
        ax.set_xlabel(xlabel or data.name or 'Valor')
        ax.set_ylabel('Densidad')
        ax.set_title(title or f'Distribución de {data.name}')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Guardar
        filename = filename or f'histogram_{data.name}.png'
        filepath = self.output_dir / filename
        plt.tight_layout()
        plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        logger.info(f"✓ Histograma guardado: {filepath}")
        return str(filepath)
    
    def boxplot(self, data: pd.DataFrame,
                variables: List[str] = None,
                title: str = None,
                ylabel: str = None,
                filename: str = None) -> str:
        """
        Crea diagrama de cajas (boxplot).
        
        Args:
            data (pd.DataFrame): DataFrame con los datos
            variables (List[str]): Variables a graficar
            title (str): Título del gráfico
            ylabel (str): Etiqueta del eje Y
            filename (str): Nombre del archivo
            
        Returns:
            str: Ruta del archivo guardado
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if variables is None:
            variables = data.select_dtypes(include=[np.number]).columns.tolist()
        
        # Crear boxplot
        bp = ax.boxplot([data[var].dropna() for var in variables],
                       labels=variables,
                       patch_artist=True,
                       notch=True,
                       showmeans=True)
        
        # Colorear cajas
        colors = sns.color_palette("Set2", len(variables))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax.set_ylabel(ylabel or 'Valor')
        ax.set_title(title or 'Diagrama de Cajas')
        ax.grid(True, alpha=0.3, axis='y')
        plt.xticks(rotation=45, ha='right')
        
        # Guardar
        filename = filename or 'boxplot.png'
        filepath = self.output_dir / filename
        plt.tight_layout()
        plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        logger.info(f"✓ Boxplot guardado: {filepath}")
        return str(filepath)
    
    def bar_chart(self, data: pd.Series,
                  title: str = None,
                  xlabel: str = None,
                  ylabel: str = 'Frecuencia',
                  horizontal: bool = False,
                  show_percentages: bool = True,
                  filename: str = None) -> str:
        """
        Crea gráfico de barras.
        
        Args:
            data (pd.Series): Datos categóricos
            title (str): Título
            xlabel (str): Etiqueta eje X
            ylabel (str): Etiqueta eje Y
            horizontal (bool): Barras horizontales
            show_percentages (bool): Mostrar porcentajes
            filename (str): Nombre del archivo
            
        Returns:
            str: Ruta del archivo guardado
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Contar frecuencias
        value_counts = data.value_counts()
        percentages = (value_counts / value_counts.sum() * 100)
        
        if horizontal:
            bars = ax.barh(range(len(value_counts)), value_counts.values,
                          color=sns.color_palette("Set2", len(value_counts)))
            ax.set_yticks(range(len(value_counts)))
            ax.set_yticklabels(value_counts.index)
            ax.set_xlabel(ylabel)
            ax.set_ylabel(xlabel or data.name or 'Categoría')
            
            # Agregar valores/porcentajes
            for i, (val, pct) in enumerate(zip(value_counts.values, percentages.values)):
                label = f'{val} ({pct:.1f}%)' if show_percentages else f'{val}'
                ax.text(val, i, f' {label}', va='center', fontweight='bold')
        else:
            bars = ax.bar(range(len(value_counts)), value_counts.values,
                         color=sns.color_palette("Set2", len(value_counts)))
            ax.set_xticks(range(len(value_counts)))
            ax.set_xticklabels(value_counts.index, rotation=45, ha='right')
            ax.set_xlabel(xlabel or data.name or 'Categoría')
            ax.set_ylabel(ylabel)
            
            # Agregar valores/porcentajes
            for i, (val, pct) in enumerate(zip(value_counts.values, percentages.values)):
                label = f'{val}\n({pct:.1f}%)' if show_percentages else f'{val}'
                ax.text(i, val, label, ha='center', va='bottom', fontweight='bold')
        
        ax.set_title(title or f'Frecuencias de {data.name}')
        ax.grid(True, alpha=0.3, axis='y' if not horizontal else 'x')
        
        # Guardar
        filename = filename or f'barplot_{data.name}.png'
        filepath = self.output_dir / filename
        plt.tight_layout()
        plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        logger.info(f"✓ Gráfico de barras guardado: {filepath}")
        return str(filepath)
    
    def correlation_heatmap(self, corr_matrix: pd.DataFrame,
                           title: str = None,
                           annot: bool = True,
                           cmap: str = 'coolwarm',
                           filename: str = None) -> str:
        """
        Crea mapa de calor de correlaciones.
        
        Args:
            corr_matrix (pd.DataFrame): Matriz de correlación
            title (str): Título
            annot (bool): Anotar valores
            cmap (str): Mapa de colores
            filename (str): Nombre del archivo
            
        Returns:
            str: Ruta del archivo guardado
        """
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Crear heatmap
        sns.heatmap(corr_matrix, annot=annot, cmap=cmap, center=0,
                   square=True, linewidths=0.5, cbar_kws={"shrink": 0.8},
                   vmin=-1, vmax=1, fmt='.2f', ax=ax)
        
        ax.set_title(title or 'Matriz de Correlación')
        
        # Guardar
        filename = filename or 'correlation_heatmap.png'
        filepath = self.output_dir / filename
        plt.tight_layout()
        plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        logger.info(f"✓ Mapa de calor guardado: {filepath}")
        return str(filepath)
    
    def scatter_plot(self, x: pd.Series, y: pd.Series,
                    title: str = None,
                    xlabel: str = None,
                    ylabel: str = None,
                    show_regression: bool = True,
                    filename: str = None) -> str:
        """
        Crea diagrama de dispersión.
        
        Args:
            x (pd.Series): Variable X
            y (pd.Series): Variable Y
            title (str): Título
            xlabel (str): Etiqueta eje X
            ylabel (str): Etiqueta eje Y
            show_regression (bool): Mostrar línea de regresión
            filename (str): Nombre del archivo
            
        Returns:
            str: Ruta del archivo guardado
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Limpiar datos
        df = pd.DataFrame({'x': x, 'y': y}).dropna()
        
        # Scatter plot
        ax.scatter(df['x'], df['y'], alpha=0.6, s=50, color='steelblue',
                  edgecolors='black', linewidth=0.5)
        
        # Línea de regresión
        if show_regression and len(df) > 1:
            from scipy import stats
            slope, intercept, r_value, p_value, std_err = stats.linregress(df['x'], df['y'])
            line = slope * df['x'] + intercept
            ax.plot(df['x'], line, 'r-', linewidth=2, 
                   label=f'Regresión: R² = {r_value**2:.3f}')
            ax.legend()
        
        # Calcular correlación
        corr = df['x'].corr(df['y'])
        textstr = f'N = {len(df)}\nCorrelación = {corr:.3f}'
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes,
               verticalalignment='top', bbox=dict(boxstyle='round',
               facecolor='wheat', alpha=0.5))
        
        ax.set_xlabel(xlabel or x.name or 'X')
        ax.set_ylabel(ylabel or y.name or 'Y')
        ax.set_title(title or f'{y.name} vs {x.name}')
        ax.grid(True, alpha=0.3)
        
        # Guardar
        filename = filename or f'scatter_{x.name}_vs_{y.name}.png'
        filepath = self.output_dir / filename
        plt.tight_layout()
        plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        logger.info(f"✓ Scatter plot guardado: {filepath}")
        return str(filepath)
    
    def grouped_bar_chart(self, data: pd.DataFrame,
                         x_var: str, y_var: str, hue_var: str,
                         title: str = None,
                         filename: str = None) -> str:
        """
        Crea gráfico de barras agrupadas.
        
        Args:
            data (pd.DataFrame): DataFrame
            x_var (str): Variable para eje X
            y_var (str): Variable para eje Y
            hue_var (str): Variable para agrupar
            title (str): Título
            filename (str): Nombre del archivo
            
        Returns:
            str: Ruta del archivo guardado
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        sns.barplot(data=data, x=x_var, y=y_var, hue=hue_var, ax=ax,
                   palette="Set2", ci=95)
        
        ax.set_title(title or f'{y_var} por {x_var} y {hue_var}')
        ax.set_xlabel(x_var)
        ax.set_ylabel(y_var)
        ax.legend(title=hue_var)
        ax.grid(True, alpha=0.3, axis='y')
        plt.xticks(rotation=45, ha='right')
        
        # Guardar
        filename = filename or f'grouped_bar_{x_var}_{y_var}_{hue_var}.png'
        filepath = self.output_dir / filename
        plt.tight_layout()
        plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        logger.info(f"✓ Gráfico de barras agrupadas guardado: {filepath}")
        return str(filepath)
    
    def pie_chart(self, data: pd.Series,
                  title: str = None,
                  autopct: str = '%1.1f%%',
                  filename: str = None) -> str:
        """
        Crea gráfico de pastel.
        
        Args:
            data (pd.Series): Datos categóricos
            title (str): Título
            autopct (str): Formato de porcentajes
            filename (str): Nombre del archivo
            
        Returns:
            str: Ruta del archivo guardado
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        value_counts = data.value_counts()
        colors = sns.color_palette("Set2", len(value_counts))
        
        wedges, texts, autotexts = ax.pie(value_counts.values,
                                          labels=value_counts.index,
                                          autopct=autopct,
                                          colors=colors,
                                          startangle=90,
                                          explode=[0.05] * len(value_counts))
        
        # Mejorar legibilidad
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title(title or f'Distribución de {data.name}')
        
        # Guardar
        filename = filename or f'pie_{data.name}.png'
        filepath = self.output_dir / filename
        plt.tight_layout()
        plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        logger.info(f"✓ Gráfico de pastel guardado: {filepath}")
        return str(filepath)


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def quick_histogram(data: pd.Series, output_dir: str = './results/graficos') -> str:
    """Función rápida para crear histograma."""
    viz = DataVisualizer(output_dir)
    return viz.histogram(data)


def quick_barplot(data: pd.Series, output_dir: str = './results/graficos') -> str:
    """Función rápida para crear gráfico de barras."""
    viz = DataVisualizer(output_dir)
    return viz.bar_chart(data)


# Importar stats para funciones
from scipy import stats
