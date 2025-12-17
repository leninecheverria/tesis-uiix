# 🎯 CONFIGURACIÓN DE VARIABLES PARA TU HIPÓTESIS

## 📋 Tu Hipótesis:

**"Los factores personales, tecnológicos e institucionales inciden en la viabilidad de implementar un Sistema de Gestión de Aprendizaje (LMS) en el Programa de Capacitación CEV de la Iglesia Cristiana 'Verbo Centro Histórico Quito'"**

---

## 🔬 MAPEO DE VARIABLES A FACTORES

Según tu hipótesis, tienes **3 factores (variables independientes)** que inciden en **1 variable dependiente**:

### ✅ VARIABLES INDEPENDIENTES (Factores que inciden):

#### 1️⃣ **FACTOR PERSONAL** (Autogestión y Disposición Personal)
**Variables del cuestionario:**
- **P1**: Disciplina para cumplir con actividades de aprendizaje virtual
- **P2**: Disponibilidad de tiempo para capacitaciones en línea
- **P3**: Apoyo familiar o del entorno cercano
- **P4**: Motivación para aprender temas espirituales virtuales
- **P5**: Capacidad de organizar propio ritmo de estudio

**Variable acumulada existente:** ✅ Ya tienes `Autogestion_Personal` pero usa fórmula mixta

**Variable acumulada recomendada:** 
```
FACTOR_PERSONAL = (P1 + P2 + P3 + P4 + P5) / 5
```

---

#### 2️⃣ **FACTOR TECNOLÓGICO** (Infraestructura y Competencias Tecnológicas)
**Variables del cuestionario:**
- **T1**: Acceso a dispositivo tecnológico (computadora, tableta, celular)
- **T2**: Conexión estable a internet
- **T3**: Habilidad utilizando plataformas virtuales
- **T4**: Experiencia previa en cursos virtuales
- **T5**: Percepción de que la tecnología facilita crecimiento espiritual

**Variable acumulada existente:** ✅ Ya tienes `Infraestructura_Entorno` pero usa fórmula mixta

**Variable acumulada recomendada:**
```
FACTOR_TECNOLOGICO = (T1 + T2 + T3 + T4 + T5) / 5
```

---

#### 3️⃣ **FACTOR INSTITUCIONAL** (Apoyo y Capacidad Institucional)
**Variables del cuestionario:**
- **I1**: La iglesia promueve uso de tecnología en enseñanza
- **I2**: La iglesia cuenta con recursos humanos y técnicos para LMS
- **I3**: Líderes/maestros dispuestos a capacitarse en LMS
- **I4**: El Programa CEV tiene organización para incorporar LMS
- **I5**: El liderazgo apoyaría implementación de LMS
- **I6**: Miembros aceptarían modalidad virtual como complemento

**Variable acumulada existente:** ✅ Ya tienes `Apoyo_Institucional`

**Variable acumulada recomendada:**
```
FACTOR_INSTITUCIONAL = (I1 + I2 + I3 + I4 + I5 + I6) / 6
```

⚠️ **PROBLEMA**: 61.4% datos faltantes (solo 54 de 140 casos respondieron)

---

### 🎯 VARIABLE DEPENDIENTE (Viabilidad del LMS):

#### **VIABILIDAD_LMS** (Percepción de Viabilidad)
**Variables del cuestionario:**
- **L1**: LMS mejoraría organización del programa
- **L2**: LMS facilitaría acceso a materiales
- **L3**: LMS permitiría ampliar alcance a más personas
- **L4**: LMS fortalece proceso de enseñanza-aprendizaje
- **L5**: Percepción de riesgos/dificultades (⚠️ INVERTIDA)

**Variable acumulada recomendada:**
```
VIABILIDAD_LMS = (L1 + L2 + L3 + L4 + (6 - L5)) / 5
```
**Nota:** L5 debe invertirse porque pregunta por riesgos (más riesgo = menos viabilidad)

---

## 📊 MODELO DE ANÁLISIS PARA TU HIPÓTESIS

### Estructura del modelo:

```
FACTORES (Variables Independientes):          RESULTADO (Variable Dependiente):
┌─────────────────────────┐
│  FACTOR_PERSONAL        │ ──┐
│  (P1, P2, P3, P4, P5)   │   │
└─────────────────────────┘   │
                              │
┌─────────────────────────┐   │
│  FACTOR_TECNOLOGICO     │ ──┤──────────>  VIABILIDAD_LMS
│  (T1, T2, T3, T4, T5)   │   │             (L1, L2, L3, L4, L5*)
└─────────────────────────┘   │
                              │
┌─────────────────────────┐   │
│  FACTOR_INSTITUCIONAL   │ ──┘
│  (I1, I2, I3, I4, I5, I6)│
└─────────────────────────┘
```

---

## 🔍 ANÁLISIS ESTADÍSTICOS RECOMENDADOS

### 1. **Análisis de Confiabilidad** (Capítulo de Metodología)
Evaluar consistencia interna de cada factor:
- Alpha de Cronbach para cada factor
- Dos mitades (Split-Half)
- Validez de constructo (análisis factorial)

**Pregunta de investigación:** ¿Los instrumentos miden consistentemente cada factor?

---

### 2. **Análisis Descriptivo** (Capítulo de Resultados)
Características de cada factor:
- Media, desviación estándar
- Nivel de cada factor (bajo, medio, alto)
- Distribución de respuestas

**Pregunta de investigación:** ¿Cuál es el nivel actual de cada factor?

---

### 3. **Análisis de Correlación** (Capítulo de Resultados)
Correlación de Pearson entre factores y viabilidad:
- FACTOR_PERSONAL ↔ VIABILIDAD_LMS
- FACTOR_TECNOLOGICO ↔ VIABILIDAD_LMS
- FACTOR_INSTITUCIONAL ↔ VIABILIDAD_LMS

**Pregunta de investigación:** ¿Qué factores se relacionan más con la viabilidad?

---

### 4. **Regresión Múltiple** (Prueba de Hipótesis)
Modelo predictivo:
```
VIABILIDAD_LMS = β0 + β1(FACTOR_PERSONAL) + β2(FACTOR_TECNOLOGICO) + β3(FACTOR_INSTITUCIONAL) + ε
```

**Pregunta de investigación:** ¿Los 3 factores predicen significativamente la viabilidad?

**Hipótesis estadísticas:**
- **H0**: Los factores NO predicen significativamente la viabilidad
- **H1**: Al menos un factor predice significativamente la viabilidad

---

### 5. **Análisis por Grupos** (Análisis Complementario)
Comparar grupos usando variables demográficas:
- Viabilidad según **tipo de participación** (estudiante CEV vs no estudiante)
- Viabilidad según **edad**
- Viabilidad según **nivel educativo**
- Viabilidad según **asiste/no asiste a la iglesia**

**Pregunta de investigación:** ¿Existen diferencias en la percepción de viabilidad entre grupos?

---

## ⚠️ PROBLEMA CRÍTICO: Factor Institucional

### El problema:
- **61.4% de datos faltantes** en I1-I6 (86 de 140 casos)
- Solo respondieron personas que **asisten a la iglesia específica** (54 casos)

### Soluciones propuestas:

#### **OPCIÓN A: Análisis en dos fases** (RECOMENDADO)

**Fase 1 - Muestra general (n=140):**
```
VIABILIDAD_LMS = β0 + β1(FACTOR_PERSONAL) + β2(FACTOR_TECNOLOGICO) + ε
```
Analiza solo factores Personal y Tecnológico con todos los participantes.

**Fase 2 - Submuestra de asistentes a iglesia (n=54):**
```
VIABILIDAD_LMS = β0 + β1(FACTOR_PERSONAL) + β2(FACTOR_TECNOLOGICO) + β3(FACTOR_INSTITUCIONAL) + ε
```
Analiza los 3 factores solo con quienes respondieron preguntas institucionales.

**Redacción para tesis:**
> "Debido a que las preguntas sobre factor institucional solo aplicaban a asistentes de la Iglesia Verbo Centro Histórico Quito, el análisis se realizó en dos fases: (1) evaluación de factores personales y tecnológicos con la muestra completa (n=140), y (2) evaluación del modelo completo incluyendo factor institucional con la submuestra de asistentes (n=54)."

---

#### **OPCIÓN B: Reformular hipótesis** (Alternativa)

**Hipótesis ajustada:**
> "Los factores personales y tecnológicos inciden en la viabilidad de implementar un LMS en el Programa CEV, considerando el factor institucional como moderador entre asistentes a la iglesia."

Analiza:
1. Modelo con 2 factores (Personal + Tecnológico) - n=140
2. Factor Institucional como análisis descriptivo separado - n=54

---

#### **OPCIÓN C: Imputación** (NO RECOMENDADO)

Con 61% faltantes, la imputación no es metodológicamente válida.

---

## 💻 CÓDIGO PARA CREAR VARIABLES ACUMULADAS

### Script Python para agregar a `main.py`:

```python
def crear_variables_acumuladas(data):
    """
    Crea variables acumuladas para probar la hipótesis.
    
    Hipótesis: Los factores personales, tecnológicos e institucionales
    inciden en la viabilidad de implementar un LMS.
    """
    import numpy as np
    
    # ============================================
    # VARIABLES INDEPENDIENTES (Factores)
    # ============================================
    
    # Factor Personal (Autogestión y Disposición)
    data['FACTOR_PERSONAL'] = data[['P1', 'P2', 'P3', 'P4', 'P5']].mean(axis=1)
    
    # Factor Tecnológico (Infraestructura y Competencias)
    data['FACTOR_TECNOLOGICO'] = data[['T1', 'T2', 'T3', 'T4', 'T5']].mean(axis=1)
    
    # Factor Institucional (Apoyo Institucional)
    # Solo disponible para asistentes a la iglesia (n=54)
    data['FACTOR_INSTITUCIONAL'] = data[['I1', 'I2', 'I3', 'I4', 'I5', 'I6']].mean(axis=1)
    
    # ============================================
    # VARIABLE DEPENDIENTE (Viabilidad)
    # ============================================
    
    # Invertir L5 (pregunta negativa sobre riesgos)
    data['L5_invertida'] = 6 - data['L5']  # Escala 1-5 invertida
    
    # Viabilidad del LMS (Percepción de viabilidad)
    data['VIABILIDAD_LMS'] = data[['L1', 'L2', 'L3', 'L4', 'L5_invertida']].mean(axis=1)
    
    # ============================================
    # VARIABLES DE CONTROL (Demográficas)
    # ============================================
    
    # Ya existen: Edad_R, Genero_R, Estudio_R, Iglesia_R
    
    print("✓ Variables acumuladas creadas:")
    print(f"  - FACTOR_PERSONAL: {data['FACTOR_PERSONAL'].notna().sum()} casos válidos")
    print(f"  - FACTOR_TECNOLOGICO: {data['FACTOR_TECNOLOGICO'].notna().sum()} casos válidos")
    print(f"  - FACTOR_INSTITUCIONAL: {data['FACTOR_INSTITUCIONAL'].notna().sum()} casos válidos")
    print(f"  - VIABILIDAD_LMS: {data['VIABILIDAD_LMS'].notna().sum()} casos válidos")
    
    return data
```

---

## 📋 CONFIGURACIÓN PARA `main.py`

### Opción 1: Dimensiones por factor (para análisis de confiabilidad)

```python
DIMENSIONES = {
    'Factor_Personal': {
        'items': ['P1', 'P2', 'P3', 'P4', 'P5'],
        'descripcion': 'Autogestión y disposición personal para aprendizaje virtual'
    },
    'Factor_Tecnologico': {
        'items': ['T1', 'T2', 'T3', 'T4', 'T5'],
        'descripcion': 'Infraestructura tecnológica y competencias digitales'
    },
    'Factor_Institucional': {
        'items': ['I1', 'I2', 'I3', 'I4', 'I5', 'I6'],
        'descripcion': 'Apoyo y capacidad institucional (solo asistentes, n=54)'
    },
    'Viabilidad_LMS': {
        'items': ['L1', 'L2', 'L3', 'L4', 'L5'],
        'descripcion': 'Percepción de viabilidad del LMS (Variable dependiente)'
    }
}
```

---

## 📊 TABLA RESUMEN PARA TU TESIS

| Factor | Variables | N Ítems | Variable Acumulada | Casos Válidos |
|--------|-----------|---------|-------------------|---------------|
| **Personal** | P1-P5 | 5 | FACTOR_PERSONAL | 140 (100%) |
| **Tecnológico** | T1-T5 | 5 | FACTOR_TECNOLOGICO | 140 (100%) |
| **Institucional** | I1-I6 | 6 | FACTOR_INSTITUCIONAL | 54 (38.6%) |
| **Viabilidad (VD)** | L1-L5 | 5 | VIABILIDAD_LMS | 140 (100%) |

---

## 🎯 RESUMEN EJECUTIVO

### Para probar tu hipótesis necesitas:

1. ✅ **Crear 4 variables acumuladas:**
   - `FACTOR_PERSONAL` (P1-P5)
   - `FACTOR_TECNOLOGICO` (T1-T5)
   - `FACTOR_INSTITUCIONAL` (I1-I6) ⚠️ solo 54 casos
   - `VIABILIDAD_LMS` (L1-L5, con L5 invertida)

2. ✅ **Análisis de confiabilidad** para cada factor

3. ✅ **Análisis descriptivo** de cada factor

4. ✅ **Correlaciones** entre factores y viabilidad

5. ✅ **Regresión múltiple** para probar hipótesis:
   - Modelo 1: Personal + Tecnológico (n=140)
   - Modelo 2: Personal + Tecnológico + Institucional (n=54)

6. ✅ **Comparaciones por grupos** (análisis complementario)

---

## 🚀 Próximos Pasos

1. **Agrega la función `crear_variables_acumuladas()` a tu `main.py`**
2. **Actualiza DIMENSIONES con los 4 factores**
3. **Ejecuta el análisis**
4. **Interpreta resultados para probar tu hipótesis**

---

¿Quieres que te ayude a:
- ✅ Modificar el archivo `main.py` con estas configuraciones?
- ✅ Crear el código para la regresión múltiple?
- ✅ Preparar las tablas para presentar en tu tesis?

¡Dime qué necesitas! 😊
