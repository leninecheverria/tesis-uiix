# Guía de Inicio Rápido

## 🚀 Primeros Pasos

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Explorar tus datos

```bash
python explorar_datos.py
```

Este script te mostrará:
- Todas tus variables
- Tipos de datos
- Valores faltantes
- Estadísticas básicas

📄 **Resultado**: Archivo `results/tablas/exploracion_datos.xlsx`

### 3. Configurar dimensiones

Abre `main.py` y define tus dimensiones:

```python
DIMENSIONES = {
    'Dimension1': {
        'items': ['P1', 'P2', 'P3'],  # ← Tus variables
        'descripcion': 'Descripción de la dimensión'
    },
    # ... más dimensiones
}
```

### 4. Ejecutar análisis completo

```bash
python main.py
```

### 5. Revisar resultados

Los resultados estarán en:

- **Gráficos**: `results/graficos/` → Para tu tesis
- **Tablas**: `results/tablas/` → Para insertar en documentos
- **Reportes**: `results/reportes/` → Para interpretar resultados

## 📊 Análisis Básicos por Módulo

### Solo estadística descriptiva

```python
python -c "
from src.data_loader import DataLoader
from src.descriptive_stats import DescriptiveAnalyzer

loader = DataLoader()
data, _ = loader.load_spss('BD/DatosAnalisisCOMPLETO.sav')

analyzer = DescriptiveAnalyzer(data)
stats = analyzer.basic_statistics()
print(stats)
"
```

### Solo fiabilidad

```python
python -c "
from src.data_loader import DataLoader
from src.reliability_analysis import ReliabilityAnalyzer

loader = DataLoader()
data, _ = loader.load_spss('BD/DatosAnalisisCOMPLETO.sav')

analyzer = ReliabilityAnalyzer(data)
items = ['P1', 'P2', 'P3', 'P4', 'P5']  # Tus ítems
result = analyzer.cronbach_alpha(items)

print(f\"Alpha de Cronbach: {result['alpha']:.4f}\")
print(f\"Interpretación: {result['interpretation']}\")
"
```

### Solo gráficos

```python
python -c "
from src.data_loader import DataLoader
from src.visualization import DataVisualizer

loader = DataLoader()
data, _ = loader.load_spss('BD/DatosAnalisisCOMPLETO.sav')

viz = DataVisualizer()
viz.histogram(data['variable_nombre'])
viz.bar_chart(data['categoria'])
"
```

## 🔧 Solución de Problemas Comunes

### Error: Module not found

```bash
pip install -r requirements.txt
```

### Error: File not found

Verifica que tus archivos están en `BD/`:
```bash
ls -la BD/
```

### No veo resultados

Verifica la carpeta `results/`:
```bash
ls -R results/
```

## 📱 Contacto y Ayuda

- Revisa `README.md` para documentación completa
- Consulta `analisis.log` para ver errores detallados
- Los comentarios en cada módulo explican cómo usarlos

## ✅ Checklist para tu Tesis

- [ ] Exploré mis datos con `explorar_datos.py`
- [ ] Definí las dimensiones en `main.py`
- [ ] Ejecuté el análisis completo con `main.py`
- [ ] Revisé el reporte de fiabilidad
- [ ] Seleccioné los gráficos para mi tesis
- [ ] Exporté las tablas necesarias
- [ ] Interpreté los resultados con mi asesor

¡Buena suerte! 🎓
