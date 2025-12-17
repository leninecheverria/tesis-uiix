# Sistema de Análisis Estadístico para Tesis de Maestría

Sistema completo y profesional para análisis estadístico de encuestas aplicadas en investigaciones de tesis de maestría. Incluye análisis de **confiabilidad y validez**, estadística descriptiva e inferencial, y generación automática de gráficos y reportes de alta calidad.

## 📚 Metodología

Este sistema implementa la metodología de investigación cuantitativa de:

**Hernández-Sampieri, R., Fernández-Collado, C., & Baptista-Lucio, P. (2014).** *Metodología de la investigación* (6a ed.). McGraw-Hill Education.

Específicamente para la **Ruta Cuantitativa** (Capítulo 9: Recolección de datos cuantitativos).

## 📋 Tabla de Contenidos

- [Características](#características)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Uso Rápido](#uso-rápido)
- [Guía Detallada](#guía-detallada)
- [Análisis Disponibles](#análisis-disponibles)
- [Interpretación de Resultados](#interpretación-de-resultados)
- [Preguntas Frecuentes](#preguntas-frecuentes)

## ✨ Características

### 🔬 Análisis de Confiabilidad
- **Alpha de Cronbach**: Medida de consistencia interna (por dimensión y global)
- **Confiabilidad por dos mitades**: Método Split-Half con corrección Spearman-Brown
- **KMO (Kaiser-Meyer-Olkin)**: Adecuación muestral para análisis factorial
- **Prueba de Bartlett**: Esfericidad de la matriz de correlación

### ✅ Análisis de Validez
- **Validez de Contenido**: Índice de Validez de Contenido (IVC) basado en juicio de expertos
- **Validez de Constructo**: Análisis Factorial Exploratorio
- **Validez Convergente**: Correlaciones inter-ítems dentro de cada dimensión
- **Validez Discriminante**: Diferenciación entre dimensiones distintas
- **Validez de Criterio**: Correlación con variable criterio externa (predictiva/concurrente)

### 📊 Estadística Descriptiva
- Medidas de tendencia central (media, mediana, moda)
- Medidas de dispersión (desviación estándar, varianza, rango)
- Medidas de forma (asimetría, curtosis)
- Tablas de frecuencias
- Matrices de correlación
- Pruebas de normalidad (Shapiro-Wilk, Kolmogorov-Smirnov)
- Detección de valores atípicos

### 🔍 Estadística Inferencial
- Prueba t de Student (una muestra e independiente)
- ANOVA de una vía con post-hoc (Tukey HSD)
- Pruebas de correlación (Pearson, Spearman, Kendall)
- Chi-cuadrado para variables categóricas
- Regresión lineal simple
- Cálculo de tamaños del efecto

### 📈 Visualizaciones Profesionales
- Histogramas con curvas de densidad
- Diagramas de caja (boxplots)
- Gráficos de barras (simples y agrupados)
- Gráficos de dispersión con regresión
- Mapas de calor de correlaciones
- Gráficos de pastel
- Alta resolución (300 DPI) para publicación

### 📄 Reportes Automatizados
- Reportes en formato Excel con formato profesional
- Reportes en texto plano
- Exportación de gráficos en PNG de alta calidad
- Reporte maestro consolidado

## 📁 Estructura del Proyecto

```
Datos/
├── BD/                          # Base de datos (tus archivos)
│   ├── DatosAnalisisCOMPLETO.sav
│   └── Encuesta-LMS-CEV (respuestas) - Respuestas de formulario 1.xls
├── src/                         # Código fuente
│   ├── __init__.py
│   ├── data_loader.py          # Carga de datos SPSS/Excel
│   ├── reliability_analysis.py  # Análisis de fiabilidad
│   ├── descriptive_stats.py    # Estadística descriptiva
│   ├── inferential_stats.py    # Estadística inferencial
│   ├── visualization.py        # Generación de gráficos
│   └── report_generator.py     # Exportación de resultados
├── config/                      # Configuración
│   └── config.py               # Parámetros del proyecto
├── results/                     # Resultados generados
│   ├── graficos/               # Gráficos en PNG
│   ├── tablas/                 # Tablas en Excel
│   └── reportes/               # Reportes consolidados
├── notebooks/                   # Jupyter notebooks (opcional)
├── main.py                      # Script principal
├── requirements.txt             # Dependencias Python
└── README.md                    # Esta documentación
```

## 🚀 Instalación

### Paso 1: Instalar Python

Asegúrate de tener Python 3.8 o superior instalado:

```bash
python --version
```

### Paso 2: Crear entorno virtual (recomendado)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

Las principales librerías que se instalarán:
- `pandas`: Manipulación de datos
- `numpy`: Cálculos numéricos
- `scipy`: Estadística científica
- `matplotlib` y `seaborn`: Visualización
- `pyreadstat`: Lectura de archivos SPSS
- `openpyxl`: Exportación a Excel
- `scikit-learn`: Análisis estadístico adicional

## 🎯 Uso Rápido

### Opción 1: Ejecutar análisis completo

```bash
python main.py
```

Este comando ejecutará automáticamente:
1. Carga de datos
2. Exploración inicial
3. Análisis de fiabilidad (si defines dimensiones)
4. Análisis descriptivo completo
5. Generación de visualizaciones
6. Exportación de todos los resultados

### Opción 2: Uso desde Python interactivo

```python
from src.data_loader import DataLoader
from src.descriptive_stats import DescriptiveAnalyzer
from src.visualization import DataVisualizer

# Cargar datos
loader = DataLoader()
data, metadata = loader.load_spss('BD/DatosAnalisisCOMPLETO.sav')

# Análisis descriptivo
analyzer = DescriptiveAnalyzer(data)
stats = analyzer.basic_statistics()

# Visualización
viz = DataVisualizer()
viz.histogram(data['variable_nombre'])
```

## 📖 Guía Detallada

### 1. Preparar tus datos

Tus datos pueden estar en dos formatos:
- **SPSS (.sav)**: Recomendado, mantiene etiquetas y metadatos
- **Excel (.xls/.xlsx)**: Alternativa si no tienes SPSS

Los archivos deben estar en la carpeta `BD/`.

### 2. Configurar dimensiones (IMPORTANTE)

Antes de ejecutar el análisis completo, debes definir las dimensiones de tu encuesta en `main.py`:

```python
DIMENSIONES = {
    'Usabilidad': {
        'items': ['P1', 'P2', 'P3', 'P4', 'P5'],
        'descripcion': 'Evaluación de la usabilidad del sistema'
    },
    'Satisfaccion': {
        'items': ['P6', 'P7', 'P8', 'P9', 'P10'],
        'descripcion': 'Nivel de satisfacción del usuario'
    },
    # ... más dimensiones según tu instrumento
}
```

**¿Cómo identificar tus dimensiones?**

1. Ejecuta primero el análisis para ver las variables:
```bash
python main.py
```

2. Revisa el archivo `results/tablas/resumen_datos.xlsx` para ver todas tus variables

3. Identifica qué ítems pertenecen a cada dimensión según tu marco teórico

4. Actualiza `DIMENSIONES` en `main.py` con tus ítems específicos

### 3. Ejecutar análisis

```bash
python main.py
```

El sistema generará automáticamente:

#### En `results/graficos/`:
- Histogramas de distribución
- Boxplots comparativos
- Mapas de calor de correlaciones
- Gráficos de barras
- Y más...

#### En `results/tablas/`:
- `resumen_datos.xlsx`: Resumen de todas las variables
- `estadisticas_descriptivas.xlsx`: Estadísticas completas
- `matriz_correlacion.xlsx`: Correlaciones entre variables

#### En `results/reportes/`:
- `reporte_fiabilidad.txt`: Análisis de fiabilidad detallado
- `reporte_maestro.txt`: Resumen ejecutivo de todo el análisis
- Versiones en Excel de los reportes

## 🔬 Análisis Disponibles

### Análisis de Fiabilidad

```python
from src.reliability_analysis import ReliabilityAnalyzer

analyzer = ReliabilityAnalyzer(data)

# Alpha de Cronbach para una dimensión
items = ['P1', 'P2', 'P3', 'P4', 'P5']
result = analyzer.cronbach_alpha(items)
print(f"Alpha de Cronbach: {result['alpha']:.3f}")
print(f"Interpretación: {result['interpretation']}")

# KMO y Bartlett
kmo = analyzer.kmo_test(items)
bartlett = analyzer.bartlett_test(items)
```

### Estadística Descriptiva

```python
from src.descriptive_stats import DescriptiveAnalyzer

analyzer = DescriptiveAnalyzer(data)

# Estadísticas básicas
stats = analyzer.basic_statistics(['variable1', 'variable2'])

# Tabla de frecuencias
freq = analyzer.frequency_table('variable_categorica')

# Matriz de correlación
corr = analyzer.correlation_matrix(['var1', 'var2', 'var3'])

# Pruebas de normalidad
normality = analyzer.normality_tests(['var1', 'var2'])
```

### Estadística Inferencial

```python
from src.inferential_stats import InferentialAnalyzer

analyzer = InferentialAnalyzer(data, alpha=0.05)

# Prueba t independiente
result = analyzer.t_test_independent('puntaje', 'grupo')

# ANOVA
result = analyzer.anova_one_way('puntaje', 'categoria')

# Correlación
result = analyzer.correlation_test('var1', 'var2', method='pearson')

# Chi-cuadrado
result = analyzer.chi_square_test('categoria1', 'categoria2')

# Regresión lineal
result = analyzer.simple_regression('dependiente', 'independiente')
```

### Visualizaciones

```python
from src.visualization import DataVisualizer

viz = DataVisualizer(output_dir='./results/graficos', dpi=300)

# Histograma
viz.histogram(data['variable'], title='Mi Histograma')

# Boxplot
viz.boxplot(data, variables=['var1', 'var2', 'var3'])

# Gráfico de barras
viz.bar_chart(data['categoria'], show_percentages=True)

# Mapa de calor de correlaciones
viz.correlation_heatmap(corr_matrix)

# Scatter plot con regresión
viz.scatter_plot(data['x'], data['y'], show_regression=True)
```

## 📊 Interpretación de Resultados

### Alpha de Cronbach (Fiabilidad)

| Valor α | Interpretación |
|---------|----------------|
| ≥ 0.90  | Excelente      |
| ≥ 0.80  | Bueno          |
| ≥ 0.70  | Aceptable      |
| ≥ 0.60  | Cuestionable   |
| ≥ 0.50  | Pobre          |
| < 0.50  | Inaceptable    |

**Para tesis:** Se recomienda α ≥ 0.70 como mínimo aceptable.

### KMO (Kaiser-Meyer-Olkin)

| Valor KMO | Interpretación | Análisis Factorial |
|-----------|----------------|-------------------|
| ≥ 0.90    | Maravilloso    | Excelente         |
| ≥ 0.80    | Meritorio      | Muy bueno         |
| ≥ 0.70    | Mediano        | Aceptable         |
| ≥ 0.60    | Mediocre       | Regular           |
| ≥ 0.50    | Miserable      | Apenas aceptable  |
| < 0.50    | Inaceptable    | No recomendado    |

### Prueba de Bartlett

- **p < 0.05**: Las variables están correlacionadas (apropiado para análisis factorial)
- **p ≥ 0.05**: Las variables NO están suficientemente correlacionadas

### Correlación de Pearson

| Valor |r| | Interpretación |
|---------|----------------|
| 0.00-0.10 | Despreciable |
| 0.10-0.30 | Débil        |
| 0.30-0.50 | Moderada     |
| 0.50-0.70 | Fuerte       |
| 0.70-1.00 | Muy fuerte   |

### Tamaño del Efecto (d de Cohen)

| Valor |d| | Interpretación |
|---------|----------------|
| < 0.20  | Pequeño        |
| 0.20-0.50 | Mediano      |
| 0.50-0.80 | Grande       |
| > 0.80  | Muy grande     |

### Valor p (Significancia estadística)

- **p < 0.05**: Resultado estadísticamente significativo (rechazar H0)
- **p < 0.01**: Altamente significativo
- **p < 0.001**: Muy altamente significativo
- **p ≥ 0.05**: No significativo (no rechazar H0)

## ❓ Preguntas Frecuentes

### ¿Qué archivo debo usar: SPSS (.sav) o Excel?

**Recomendación:** Usa el archivo SPSS (.sav) porque:
- Mantiene las etiquetas de variables y valores
- Conserva los tipos de datos correctos
- Ya incluye las transformaciones que hiciste en PSPP

### ¿Qué análisis debo incluir en mi tesis?

Para una tesis de maestría, generalmente necesitas:

1. **Análisis de Fiabilidad** (Capítulo de Metodología):
   - Alpha de Cronbach por dimensión
   - KMO y Bartlett (si aplica análisis factorial)
   
2. **Análisis Descriptivo** (Capítulo de Resultados):
   - Características de la muestra
   - Estadísticas descriptivas de variables clave
   - Distribución de respuestas
   
3. **Análisis Inferencial** (Capítulo de Resultados):
   - Pruebas de hipótesis según tus objetivos
   - Correlaciones entre variables
   - Comparaciones entre grupos (si aplica)

4. **Gráficos** (A lo largo de la tesis):
   - Mínimo 3-5 gráficos profesionales
   - Deben ilustrar los hallazgos principales

### ¿Cómo cito estos análisis en mi tesis?

Ejemplos de redacción:

**Fiabilidad:**
> "Se calculó el coeficiente Alpha de Cronbach para evaluar la consistencia interna del instrumento. La dimensión de Usabilidad obtuvo un α = 0.87, considerado bueno según George y Mallery (2003)."

**Prueba KMO:**
> "La prueba de Kaiser-Meyer-Olkin (KMO = 0.82) indica una adecuación muestral meritoria para el análisis factorial (Kaiser, 1974)."

**Bartlett:**
> "La prueba de esfericidad de Bartlett resultó significativa (χ² = 234.56, gl = 45, p < 0.001), indicando que las variables están lo suficientemente correlacionadas para realizar análisis factorial."

### ¿Qué hago si mi Alpha de Cronbach es bajo (< 0.70)?

1. **Revisa el análisis "Alpha si se elimina el ítem"**: 
   - Si eliminar un ítem aumenta significativamente α, considera excluirlo
   
2. **Verifica las correlaciones ítem-total**:
   - Ítems con correlación < 0.30 son problemáticos
   
3. **Considera**:
   - ¿El ítem mide lo mismo que los demás?
   - ¿Está redactado de forma inversa?
   - ¿Los encuestados lo entendieron correctamente?

4. **Documenta** tus decisiones en la tesis

### ¿Cómo interpreto un mapa de calor de correlaciones?

- **Colores cálidos (rojos)**: Correlación positiva fuerte
- **Colores fríos (azules)**: Correlación negativa fuerte
- **Colores blancos**: Sin correlación
- **Diagonal**: Siempre 1.00 (variable consigo misma)

### ¿Qué resolución debo usar para los gráficos?

El sistema genera automáticamente gráficos a **300 DPI**, que es el estándar para:
- Publicaciones académicas
- Impresión de tesis
- Revistas científicas

No necesitas modificar esto.

### Error: "No se ha podido resolver la importación"

Esto es normal antes de instalar las dependencias. Ejecuta:

```bash
pip install -r requirements.txt
```

### ¿Puedo modificar los colores de los gráficos?

Sí, edita `src/visualization.py` y cambia:

```python
sns.set_palette("Set2")  # Cambia a "husl", "deep", "muted", etc.
```

### ¿Cómo agrego más pruebas estadísticas?

Los módulos son extensibles. Por ejemplo, para agregar una prueba Mann-Whitney:

```python
# En src/inferential_stats.py
def mann_whitney_test(self, variable: str, group_var: str) -> Dict:
    from scipy.stats import mannwhitneyu
    
    groups = self.data[group_var].unique()
    group1 = self.data[self.data[group_var] == groups[0]][variable].dropna()
    group2 = self.data[self.data[group_var] == groups[1]][variable].dropna()
    
    statistic, p_value = mannwhitneyu(group1, group2)
    
    # ... resto del código
```

## 📚 Referencias Metodológicas

- **Alpha de Cronbach**: Cronbach, L. J. (1951). Coefficient alpha and the internal structure of tests.
- **KMO**: Kaiser, H. F. (1974). An index of factorial simplicity.
- **Bartlett**: Bartlett, M. S. (1954). A note on the multiplying factors for various chi square approximations.
- **d de Cohen**: Cohen, J. (1988). Statistical power analysis for the behavioral sciences.

## 🆘 Soporte

Si encuentras problemas:

1. **Revisa el archivo de log**: `analisis.log`
2. **Verifica que instalaste todas las dependencias**
3. **Asegúrate de que tus archivos de datos están en `BD/`**
4. **Revisa que definiste correctamente las DIMENSIONES**

## 📝 Notas Finales

- **Respalda tus datos** antes de realizar modificaciones
- **Documenta cualquier transformación** que hagas a los datos
- **Revisa siempre los resultados** antes de incluirlos en tu tesis
- **Consulta con tu asesor** sobre qué análisis son apropiados para tu investigación

## 🎓 Para tu Tesis

Este sistema te proporcionará:

✅ Tablas con formato profesional listas para insertar  
✅ Gráficos de alta calidad (300 DPI)  
✅ Análisis estadísticos rigurosos  
✅ Reportes interpretativos  
✅ Respaldo metodológico sólido  

**¡Buena suerte con tu tesis de maestría!** 🎉
