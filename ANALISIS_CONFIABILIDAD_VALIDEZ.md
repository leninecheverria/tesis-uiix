# Análisis de Confiabilidad y Validez del Instrumento

## 📚 Referencia Metodológica

Este sistema implementa la metodología de:

**Hernández-Sampieri, R., Fernández-Collado, C., & Baptista-Lucio, P. (2014).** *Metodología de la investigación* (6a ed.). McGraw-Hill Education.

Específicamente el Capítulo 9: "Recolección de datos cuantitativos" - Sección sobre **Confiabilidad y Validez**.

---

## 🎯 ¿Qué incluye el análisis?

### 1. ANÁLISIS DE CONFIABILIDAD

#### 1.1 Alpha de Cronbach
- **Qué mide**: Consistencia interna del instrumento
- **Interpretación** (Hernández-Sampieri, 2014):
  - α ≥ 0.90: **Elevada** (Excelente)
  - α ≥ 0.80: **Muy alta** (Buena)
  - α ≥ 0.70: **Alta** (Aceptable para tesis)
  - α ≥ 0.60: **Moderada** (Cuestionable)
  - α < 0.60: **Baja** (Inaceptable)

#### 1.2 Confiabilidad por Dos Mitades (Split-Half)
- **Qué mide**: Equivalencia entre dos mitades del instrumento
- **Método**: Divide ítems en dos grupos, correlaciona y aplica corrección Spearman-Brown
- **Interpretación**: Misma escala que Alpha de Cronbach

#### 1.3 Prueba KMO (Kaiser-Meyer-Olkin)
- **Qué mide**: Adecuación de la muestra para análisis factorial
- **Interpretación**:
  - KMO ≥ 0.90: Maravilloso
  - KMO ≥ 0.80: Meritorio
  - KMO ≥ 0.70: Mediano (aceptable)
  - KMO ≥ 0.60: Mediocre
  - KMO < 0.50: Inaceptable

#### 1.4 Prueba de Bartlett
- **Qué mide**: Si las variables están suficientemente correlacionadas
- **Interpretación**: p < 0.05 indica que SÍ es adecuado hacer análisis factorial

---

### 2. ANÁLISIS DE VALIDEZ

#### 2.1 Validez de Contenido
- **Qué mide**: Si el instrumento cubre adecuadamente el dominio de contenido
- **Método**: Índice de Validez de Contenido (IVC) basado en juicio de expertos
- **Cómo usarlo**: 
  - Necesitas una tabla donde expertos califiquen cada ítem (ej: 1-4)
  - El sistema calcula el IVC automáticamente
- **Interpretación**:
  - IVC ≥ 0.80: Excelente
  - IVC ≥ 0.70: Buena
  - IVC ≥ 0.60: Aceptable
  - IVC < 0.60: Insuficiente

**Ejemplo de uso:**
```python
# Crear DataFrame con calificaciones de jueces
# Filas = ítems, Columnas = jueces, Valores = calificación (1-4)
judges_ratings = pd.DataFrame({
    'Juez1': [4, 4, 3, 4, 3],
    'Juez2': [4, 3, 4, 4, 4],
    'Juez3': [3, 4, 4, 3, 4],
    'Juez4': [4, 4, 4, 4, 3],
    'Juez5': [4, 3, 4, 4, 4]
}, index=['Item1', 'Item2', 'Item3', 'Item4', 'Item5'])

# Calcular IVC
analyzer = ReliabilityAnalyzer(data)
ivc_result = analyzer.content_validity_index(judges_ratings)
```

#### 2.2 Validez de Constructo (Análisis Factorial)
- **Qué mide**: Si el instrumento mide el constructo teórico propuesto
- **Método**: Análisis Factorial Exploratorio
- **Interpreta**:
  - Número de factores extraídos
  - Cargas factoriales (> 0.40 son significativas)
  - Varianza explicada (> 60% es buena)
- **Uso automático**: El sistema lo hace por cada dimensión

#### 2.3 Validez Convergente
- **Qué mide**: Si ítems del mismo constructo correlacionan entre sí
- **Método**: Correlación promedio entre ítems de la misma dimensión
- **Interpretación**:
  - r ≥ 0.50: Excelente
  - r ≥ 0.30: Buena
  - r ≥ 0.20: Aceptable
  - r < 0.20: Insuficiente
- **Uso automático**: El sistema lo calcula para cada dimensión

#### 2.4 Validez Discriminante
- **Qué mide**: Si dimensiones diferentes están suficientemente diferenciadas
- **Método**: Correlación entre puntajes de diferentes dimensiones
- **Interpretación** (debe ser BAJA):
  - |r| < 0.30: Excelente discriminación
  - |r| < 0.50: Buena discriminación
  - |r| ≥ 0.70: Insuficiente (dimensiones muy similares)
- **Uso automático**: El sistema compara las dos primeras dimensiones

#### 2.5 Validez de Criterio
- **Qué mide**: Si el instrumento se relaciona con un criterio externo conocido
- **Método**: Correlación con variable criterio
- **Necesitas**: Una variable criterio (ej: calificaciones, rendimiento previo)
- **Interpretación**:
  - r ≥ 0.50 y p < 0.01: Excelente
  - r ≥ 0.30 y p < 0.05: Buena
  - p ≥ 0.05: No significativa

**Ejemplo de uso:**
```python
# Especificar variable criterio al ejecutar
results = analyzer.comprehensive_reliability_validity(
    dimensions,
    include_validity=True,
    criterion_variable='Promedio_General'  # Tu variable criterio
)
```

---

## 🚀 Cómo ejecutar el análisis completo

### Opción 1: Confiabilidad + Validez (RECOMENDADO)

```python
from src.reliability_analysis import ReliabilityAnalyzer

# Cargar datos
data = pd.read_spss('tu_archivo.sav')

# Definir dimensiones
dimensiones = {
    'Usabilidad': ['P1', 'P2', 'P3', 'P4', 'P5'],
    'Satisfaccion': ['P6', 'P7', 'P8', 'P9', 'P10'],
    'Funcionalidad': ['P11', 'P12', 'P13', 'P14']
}

# Crear analizador
analyzer = ReliabilityAnalyzer(data)

# Análisis COMPLETO
results = analyzer.comprehensive_reliability_validity(
    dimensions=dimensiones,
    include_validity=True,  # Incluir análisis de validez
    criterion_variable=None  # Opcional: especifica una variable criterio
)
```

### Opción 2: Solo Confiabilidad

```python
# Si solo quieres confiabilidad (sin validez)
results = analyzer.comprehensive_reliability_validity(
    dimensions=dimensiones,
    include_validity=False
)

# O usar el método legacy
results = analyzer.comprehensive_reliability(dimensiones)
```

---

## 📊 Interpretando los Resultados

### Estructura del diccionario de resultados:

```python
{
    'general': {  # Análisis del instrumento completo
        'cronbach_alpha': {...},
        'split_half': {...},
        'kmo': {...},
        'bartlett': {...}
    },
    'by_dimension': {  # Análisis por cada dimensión
        'Usabilidad': {
            'cronbach_alpha': {...},
            'split_half': {...},
            'kmo': {...},
            'bartlett': {...}
        },
        'Satisfaccion': {...},
        ...
    },
    'validity': {  # Análisis de validez
        'Usabilidad_factorial': {...},  # Análisis factorial por dimensión
        'Satisfaccion_factorial': {...},
        'Usabilidad_convergent': {...},  # Validez convergente por dimensión
        'Satisfaccion_convergent': {...},
        'discriminant': {...},  # Validez discriminante entre dimensiones
        'criterion': {...}  # Validez de criterio (si se especificó)
    }
}
```

### Accediendo a resultados específicos:

```python
# Alpha de Cronbach general
alpha_general = results['general']['cronbach_alpha']['alpha']
print(f"Alpha general: {alpha_general:.3f}")

# Alpha por dimensión
alpha_usabilidad = results['by_dimension']['Usabilidad']['cronbach_alpha']['alpha']
print(f"Alpha Usabilidad: {alpha_usabilidad:.3f}")

# Validez convergente
conv_usabilidad = results['validity']['Usabilidad_convergent']['mean_correlation']
print(f"Correlación promedio Usabilidad: {conv_usabilidad:.3f}")
```

---

## 📝 Redactando los Resultados para la Tesis

### Ejemplo de Sección de Metodología:

> **Confiabilidad y validez del instrumento**
>
> Para garantizar la calidad psicométrica del instrumento, se evaluó su confiabilidad mediante el coeficiente Alpha de Cronbach y el método de dos mitades con corrección de Spearman-Brown (Hernández-Sampieri et al., 2014). El Alpha de Cronbach general del instrumento fue α = 0.89, considerado muy alto. El método de dos mitades confirmó estos resultados con un coeficiente de 0.87.
>
> Por dimensiones, se obtuvieron los siguientes valores: Usabilidad (α = 0.87, muy alta), Satisfacción (α = 0.91, elevada) y Funcionalidad (α = 0.84, muy alta). Todos los valores superan el mínimo recomendado de 0.70 (Hernández-Sampieri et al., 2014).
>
> La validez de constructo fue evaluada mediante Análisis Factorial Exploratorio. La prueba de Kaiser-Meyer-Olkin (KMO = 0.82) indicó una adecuación muestral meritoria, y la prueba de esfericidad de Bartlett fue significativa (χ² = 234.56, gl = 45, p < 0.001), confirmando la pertinencia del análisis.
>
> La validez convergente mostró correlaciones promedio de r = 0.54, indicando que los ítems de cada dimensión miden consistentemente el mismo constructo. La validez discriminante entre dimensiones fue adecuada (r = 0.42), indicando que miden constructos relacionados pero diferenciados.

### Tabla resumen para la tesis:

| Dimensión | N Ítems | α Cronbach | Dos Mitades | KMO | Validez Convergente | Interpretación |
|-----------|---------|------------|-------------|-----|---------------------|----------------|
| Usabilidad | 5 | 0.87 | 0.85 | 0.81 | r = 0.52 | Muy alta |
| Satisfacción | 7 | 0.91 | 0.90 | 0.84 | r = 0.58 | Elevada |
| Funcionalidad | 4 | 0.84 | 0.82 | 0.79 | r = 0.49 | Muy alta |
| **TOTAL** | **16** | **0.89** | **0.87** | **0.82** | **r = 0.53** | **Muy alta** |

---

## ⚠️ Notas Importantes

1. **Validez de contenido**: Necesitas datos de jueces expertos. Si no los tienes, puedes omitir esta prueba y justificarlo en tu tesis diciendo que los ítems fueron tomados de un instrumento validado previamente.

2. **Variable criterio**: Para validez de criterio necesitas una variable externa (ej: calificaciones, test previo). Si no la tienes, omite esta prueba.

3. **Tamaño muestral**: 
   - Mínimo 50 casos para análisis básico
   - Ideal: 5-10 casos por ítem para análisis factorial
   - Con menos casos, algunos análisis pueden no ser válidos

4. **Interpretaciones**: Todos los criterios de interpretación están basados en Hernández-Sampieri et al. (2014).

---

## 🔍 Verificando que todo funciona

Ejecuta el script de verificación:

```bash
python verificar_sistema.py
```

Si hay algún error con las nuevas funciones, reporta el mensaje de error.

---

## 📧 ¿Necesitas ayuda?

Si tienes dudas sobre:
- Cómo definir tus dimensiones
- Qué análisis aplicar según tu caso
- Cómo interpretar resultados específicos
- Cómo redactar los resultados en tu tesis

Pregunta específicamente sobre tu situación.
