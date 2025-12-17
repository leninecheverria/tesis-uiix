# 🎯 ESTRATEGIA DE ANÁLISIS EN DOS NIVELES PARA TU HIPÓTESIS

## 📊 ESTRUCTURA DE TU MUESTRA

```
MUESTRA TOTAL: 140 participantes
├── Todos responden: P1-P5, T1-T5, L1-L5 (n=140)
│   ├── Factor Personal (P)
│   ├── Factor Tecnológico (T)  
│   └── Viabilidad LMS (L)
│
└── Solo asistentes a iglesia responden: I1-I6 (n=54)
    └── Factor Institucional (I)
```

---

## 🎯 ESTRATEGIA RECOMENDADA: ANÁLISIS EN DOS NIVELES

### **NIVEL 1: Análisis General (Población Amplia) - n=140**
**Pregunta de investigación:**  
*"¿Qué factores personales y tecnológicos influyen en la percepción de viabilidad del LMS en la población general interesada en capacitación virtual?"*

**Modelo estadístico:**
```
VIABILIDAD_LMS = β0 + β1(FACTOR_PERSONAL) + β2(FACTOR_TECNOLOGICO) + ε
```

**Participantes:** Todos (140)
- No asisten a iglesia Verbo: 81 (57.9%)
- Miembros que no participan en CEV: 21 (15.0%)
- Estudiantes CEV: 16 (11.4%)
- Ex-estudiantes CEV: 14 (10.0%)
- Miembros interesados en CEV: 8 (5.7%)

---

### **NIVEL 2: Análisis Específico (Contexto Institucional) - n=54**
**Pregunta de investigación:**  
*"¿Cómo influye adicionalmente el factor institucional en la viabilidad del LMS entre los miembros de la iglesia que están familiarizados con el contexto organizacional?"*

**Modelo estadístico:**
```
VIABILIDAD_LMS = β0 + β1(FACTOR_PERSONAL) + β2(FACTOR_TECNOLOGICO) + β3(FACTOR_INSTITUCIONAL) + ε
```

**Participantes:** Solo asistentes a iglesia (54)
- Miembros que no participan en CEV: 21 (38.9%)
- Estudiantes CEV: 16 (29.6%)
- Ex-estudiantes CEV: 14 (25.9%)
- Miembros interesados en CEV: 3 (5.6%)

---

## 📝 CÓMO PRESENTARLO EN TU TESIS

### **Capítulo de Metodología:**

#### Sección: Diseño de la Investigación

> **Análisis en dos niveles**
>
> Considerando la naturaleza de la muestra y las características del instrumento, el análisis se estructuró en dos niveles:
>
> **Nivel 1 - Análisis General (n=140):** Se evaluó la influencia de los factores personales y tecnológicos en la percepción de viabilidad del LMS con la totalidad de participantes. Este nivel incluyó tanto a miembros de la Iglesia Verbo Centro Histórico Quito como a personas externas interesadas en capacitación virtual. El objetivo fue identificar factores universales que inciden en la viabilidad del LMS independientemente del contexto institucional.
>
> **Nivel 2 - Análisis Específico Institucional (n=54):** Se incorporó el factor institucional al análisis, considerando únicamente a los participantes que asisten a la Iglesia Verbo Centro Histórico Quito y que, por tanto, tienen conocimiento directo del contexto organizacional del Programa CEV. Este nivel permitió evaluar el efecto adicional del apoyo institucional sobre la viabilidad percibida del LMS.
>
> Esta estrategia metodológica se fundamenta en Hernández-Sampieri et al. (2014), quienes señalan que cuando existen diferencias en las características de los participantes que afectan la disponibilidad de datos, es válido realizar análisis diferenciados que aprovechen al máximo la información disponible en cada segmento de la muestra.

---

### **Capítulo de Resultados:**

#### Estructura recomendada:

```
4. RESULTADOS

4.1. Caracterización de la Muestra
     4.1.1. Muestra total (n=140)
     4.1.2. Submuestra institucional (n=54)
     4.1.3. Comparación de características demográficas

4.2. Confiabilidad y Validez del Instrumento
     4.2.1. Factor Personal (n=140)
     4.2.2. Factor Tecnológico (n=140)
     4.2.3. Factor Institucional (n=54)
     4.2.4. Viabilidad del LMS (n=140)

4.3. Análisis Descriptivo de Variables
     4.3.1. Estadísticos descriptivos por factor
     4.3.2. Niveles de cada factor (bajo, medio, alto)

4.4. Análisis de Viabilidad - Nivel General (n=140)
     4.4.1. Correlaciones entre factores personales, tecnológicos y viabilidad
     4.4.2. Regresión múltiple: Modelo con 2 predictores
     4.4.3. Análisis por grupos demográficos

4.5. Análisis de Viabilidad - Nivel Institucional (n=54)
     4.5.1. Correlaciones incluyendo factor institucional
     4.5.2. Regresión múltiple: Modelo con 3 predictores
     4.5.3. Comparación de modelos (Nivel 1 vs Nivel 2)

4.6. Prueba de Hipótesis
     4.6.1. Hipótesis general
     4.6.2. Hipótesis específicas por factor
```

---

## 💻 CÓDIGO ACTUALIZADO PARA main.py

### Agregar esta función después de `crear_variables_acumuladas()`:

```python
def analisis_dos_niveles(data, dimensiones):
    """
    Realiza análisis en dos niveles según disponibilidad de datos.
    
    NIVEL 1 (n=140): Factores Personal + Tecnológico → Viabilidad
    NIVEL 2 (n=54): Factores Personal + Tecnológico + Institucional → Viabilidad
    
    Args:
        data (DataFrame): Datos con variables acumuladas
        dimensiones (dict): Diccionario con dimensiones
    
    Returns:
        dict: Resultados de ambos niveles de análisis
    """
    logger.info("\n" + "="*80)
    logger.info("ANÁLISIS EN DOS NIVELES SEGÚN HIPÓTESIS")
    logger.info("="*80)
    
    results = {
        'nivel1_general': {},
        'nivel2_institucional': {}
    }
    
    # ========================================================================
    # NIVEL 1: ANÁLISIS GENERAL (n=140)
    # Factores Personal + Tecnológico
    # ========================================================================
    
    logger.info("\n" + "─"*80)
    logger.info("NIVEL 1: ANÁLISIS GENERAL (Población Amplia)")
    logger.info("─"*80)
    logger.info("Muestra: Todos los participantes (n=140)")
    logger.info("Factores: Personal + Tecnológico → Viabilidad LMS")
    logger.info("─"*80)
    
    # Dimensiones para Nivel 1 (excluye Factor Institucional)
    dimensiones_nivel1 = {
        k: v for k, v in dimensiones.items() 
        if k != 'Factor_Institucional'
    }
    
    # Análisis de confiabilidad y validez - Nivel 1
    logger.info("\n📊 1.1. CONFIABILIDAD Y VALIDEZ (Nivel General)")
    analyzer_n1 = ReliabilityAnalyzer(data)
    results['nivel1_general']['confiabilidad'] = analyzer_n1.comprehensive_reliability_validity(
        dimensiones_nivel1,
        include_validity=True,
        criterion_variable='VIABILIDAD_LMS'
    )
    
    # Estadísticas descriptivas - Nivel 1
    logger.info("\n📊 1.2. ESTADÍSTICAS DESCRIPTIVAS (Nivel General)")
    desc_analyzer_n1 = DescriptiveAnalyzer(data)
    
    variables_n1 = ['FACTOR_PERSONAL', 'FACTOR_TECNOLOGICO', 'VIABILIDAD_LMS']
    results['nivel1_general']['descriptivos'] = {}
    
    for var in variables_n1:
        if var in data.columns:
            stats = desc_analyzer_n1.basic_statistics(data[var])
            results['nivel1_general']['descriptivos'][var] = stats
            logger.info(f"\n{var}:")
            logger.info(f"  N = {stats['count']:.0f}")
            logger.info(f"  Media = {stats['mean']:.3f}")
            logger.info(f"  DE = {stats['std']:.3f}")
            logger.info(f"  Min-Max = {stats['min']:.2f} - {stats['max']:.2f}")
    
    # Correlaciones - Nivel 1
    logger.info("\n📊 1.3. CORRELACIONES (Nivel General)")
    from scipy import stats as sp_stats
    
    r_personal = data['FACTOR_PERSONAL'].corr(data['VIABILIDAD_LMS'])
    r_tecnologico = data['FACTOR_TECNOLOGICO'].corr(data['VIABILIDAD_LMS'])
    
    # Test de significancia
    n1 = len(data.dropna(subset=['FACTOR_PERSONAL', 'VIABILIDAD_LMS']))
    t_personal = r_personal * np.sqrt((n1-2)/(1-r_personal**2))
    p_personal = 2 * (1 - sp_stats.t.cdf(abs(t_personal), n1-2))
    
    n2 = len(data.dropna(subset=['FACTOR_TECNOLOGICO', 'VIABILIDAD_LMS']))
    t_tecnologico = r_tecnologico * np.sqrt((n2-2)/(1-r_tecnologico**2))
    p_tecnologico = 2 * (1 - sp_stats.t.cdf(abs(t_tecnologico), n2-2))
    
    logger.info(f"\nFACTOR_PERSONAL ↔ VIABILIDAD_LMS:")
    logger.info(f"  r = {r_personal:.3f}, p = {p_personal:.4f} {'***' if p_personal < 0.001 else '**' if p_personal < 0.01 else '*' if p_personal < 0.05 else 'ns'}")
    
    logger.info(f"\nFACTOR_TECNOLOGICO ↔ VIABILIDAD_LMS:")
    logger.info(f"  r = {r_tecnologico:.3f}, p = {p_tecnologico:.4f} {'***' if p_tecnologico < 0.001 else '**' if p_tecnologico < 0.01 else '*' if p_tecnologico < 0.05 else 'ns'}")
    
    results['nivel1_general']['correlaciones'] = {
        'personal_viabilidad': {'r': r_personal, 'p': p_personal, 'n': n1},
        'tecnologico_viabilidad': {'r': r_tecnologico, 'p': p_tecnologico, 'n': n2}
    }
    
    # Regresión múltiple - Nivel 1
    logger.info("\n📊 1.4. REGRESIÓN MÚLTIPLE (Nivel General)")
    logger.info("Modelo: VIABILIDAD_LMS ~ FACTOR_PERSONAL + FACTOR_TECNOLOGICO")
    
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score
    
    # Preparar datos para regresión
    data_reg_n1 = data[['FACTOR_PERSONAL', 'FACTOR_TECNOLOGICO', 'VIABILIDAD_LMS']].dropna()
    X_n1 = data_reg_n1[['FACTOR_PERSONAL', 'FACTOR_TECNOLOGICO']]
    y_n1 = data_reg_n1['VIABILIDAD_LMS']
    
    # Ajustar modelo
    model_n1 = LinearRegression()
    model_n1.fit(X_n1, y_n1)
    y_pred_n1 = model_n1.predict(X_n1)
    r2_n1 = r2_score(y_n1, y_pred_n1)
    
    logger.info(f"\nResultados del modelo:")
    logger.info(f"  R² = {r2_n1:.3f} ({r2_n1*100:.1f}% de varianza explicada)")
    logger.info(f"  β0 (Intercepto) = {model_n1.intercept_:.3f}")
    logger.info(f"  β1 (Factor Personal) = {model_n1.coef_[0]:.3f}")
    logger.info(f"  β2 (Factor Tecnológico) = {model_n1.coef_[1]:.3f}")
    logger.info(f"  N = {len(data_reg_n1)}")
    
    results['nivel1_general']['regresion'] = {
        'r2': r2_n1,
        'intercepto': model_n1.intercept_,
        'coef_personal': model_n1.coef_[0],
        'coef_tecnologico': model_n1.coef_[1],
        'n': len(data_reg_n1)
    }
    
    # ========================================================================
    # NIVEL 2: ANÁLISIS INSTITUCIONAL (n=54)
    # Factores Personal + Tecnológico + Institucional
    # ========================================================================
    
    logger.info("\n\n" + "─"*80)
    logger.info("NIVEL 2: ANÁLISIS INSTITUCIONAL (Contexto Específico)")
    logger.info("─"*80)
    logger.info("Muestra: Solo asistentes a iglesia (n=54)")
    logger.info("Factores: Personal + Tecnológico + Institucional → Viabilidad LMS")
    logger.info("─"*80)
    
    # Filtrar solo asistentes a iglesia (tienen datos de Factor Institucional)
    data_iglesia = data[data['FACTOR_INSTITUCIONAL'].notna()].copy()
    n_iglesia = len(data_iglesia)
    
    logger.info(f"\n📌 Casos con Factor Institucional: {n_iglesia}")
    
    # Análisis de confiabilidad y validez - Nivel 2
    logger.info("\n📊 2.1. CONFIABILIDAD Y VALIDEZ (Nivel Institucional)")
    analyzer_n2 = ReliabilityAnalyzer(data_iglesia)
    results['nivel2_institucional']['confiabilidad'] = analyzer_n2.comprehensive_reliability_validity(
        dimensiones,  # Todas las dimensiones, incluyendo Factor Institucional
        include_validity=True,
        criterion_variable='VIABILIDAD_LMS'
    )
    
    # Estadísticas descriptivas - Nivel 2
    logger.info("\n📊 2.2. ESTADÍSTICAS DESCRIPTIVAS (Nivel Institucional)")
    desc_analyzer_n2 = DescriptiveAnalyzer(data_iglesia)
    
    variables_n2 = ['FACTOR_PERSONAL', 'FACTOR_TECNOLOGICO', 'FACTOR_INSTITUCIONAL', 'VIABILIDAD_LMS']
    results['nivel2_institucional']['descriptivos'] = {}
    
    for var in variables_n2:
        if var in data_iglesia.columns:
            stats = desc_analyzer_n2.basic_statistics(data_iglesia[var])
            results['nivel2_institucional']['descriptivos'][var] = stats
            logger.info(f"\n{var}:")
            logger.info(f"  N = {stats['count']:.0f}")
            logger.info(f"  Media = {stats['mean']:.3f}")
            logger.info(f"  DE = {stats['std']:.3f}")
    
    # Correlaciones - Nivel 2
    logger.info("\n📊 2.3. CORRELACIONES (Nivel Institucional)")
    
    r_personal_2 = data_iglesia['FACTOR_PERSONAL'].corr(data_iglesia['VIABILIDAD_LMS'])
    r_tecnologico_2 = data_iglesia['FACTOR_TECNOLOGICO'].corr(data_iglesia['VIABILIDAD_LMS'])
    r_institucional = data_iglesia['FACTOR_INSTITUCIONAL'].corr(data_iglesia['VIABILIDAD_LMS'])
    
    logger.info(f"\nFACTOR_PERSONAL ↔ VIABILIDAD_LMS: r = {r_personal_2:.3f}")
    logger.info(f"FACTOR_TECNOLOGICO ↔ VIABILIDAD_LMS: r = {r_tecnologico_2:.3f}")
    logger.info(f"FACTOR_INSTITUCIONAL ↔ VIABILIDAD_LMS: r = {r_institucional:.3f}")
    
    results['nivel2_institucional']['correlaciones'] = {
        'personal_viabilidad': r_personal_2,
        'tecnologico_viabilidad': r_tecnologico_2,
        'institucional_viabilidad': r_institucional
    }
    
    # Regresión múltiple - Nivel 2
    logger.info("\n📊 2.4. REGRESIÓN MÚLTIPLE (Nivel Institucional)")
    logger.info("Modelo: VIABILIDAD_LMS ~ FACTOR_PERSONAL + FACTOR_TECNOLOGICO + FACTOR_INSTITUCIONAL")
    
    data_reg_n2 = data_iglesia[['FACTOR_PERSONAL', 'FACTOR_TECNOLOGICO', 
                                 'FACTOR_INSTITUCIONAL', 'VIABILIDAD_LMS']].dropna()
    X_n2 = data_reg_n2[['FACTOR_PERSONAL', 'FACTOR_TECNOLOGICO', 'FACTOR_INSTITUCIONAL']]
    y_n2 = data_reg_n2['VIABILIDAD_LMS']
    
    model_n2 = LinearRegression()
    model_n2.fit(X_n2, y_n2)
    y_pred_n2 = model_n2.predict(X_n2)
    r2_n2 = r2_score(y_n2, y_pred_n2)
    
    logger.info(f"\nResultados del modelo:")
    logger.info(f"  R² = {r2_n2:.3f} ({r2_n2*100:.1f}% de varianza explicada)")
    logger.info(f"  β0 (Intercepto) = {model_n2.intercept_:.3f}")
    logger.info(f"  β1 (Factor Personal) = {model_n2.coef_[0]:.3f}")
    logger.info(f"  β2 (Factor Tecnológico) = {model_n2.coef_[1]:.3f}")
    logger.info(f"  β3 (Factor Institucional) = {model_n2.coef_[2]:.3f}")
    logger.info(f"  N = {len(data_reg_n2)}")
    
    results['nivel2_institucional']['regresion'] = {
        'r2': r2_n2,
        'intercepto': model_n2.intercept_,
        'coef_personal': model_n2.coef_[0],
        'coef_tecnologico': model_n2.coef_[1],
        'coef_institucional': model_n2.coef_[2],
        'n': len(data_reg_n2)
    }
    
    # ========================================================================
    # COMPARACIÓN DE MODELOS
    # ========================================================================
    
    logger.info("\n\n" + "="*80)
    logger.info("COMPARACIÓN DE MODELOS")
    logger.info("="*80)
    
    logger.info(f"\nModelo Nivel 1 (n={len(data_reg_n1)}): R² = {r2_n1:.3f}")
    logger.info(f"Modelo Nivel 2 (n={len(data_reg_n2)}): R² = {r2_n2:.3f}")
    logger.info(f"\nIncremento en R² al agregar Factor Institucional: {r2_n2-r2_n1:.3f}")
    logger.info(f"({(r2_n2-r2_n1)*100:.1f}% adicional de varianza explicada)")
    
    results['comparacion'] = {
        'delta_r2': r2_n2 - r2_n1,
        'mejora_porcentual': (r2_n2 - r2_n1) * 100
    }
    
    logger.info("\n" + "="*80)
    logger.info("✓ ANÁLISIS EN DOS NIVELES COMPLETADO")
    logger.info("="*80)
    
    return results
```

---

## 📊 MODIFICACIÓN EN LA FUNCIÓN main()

Reemplazar la sección de análisis con:

```python
def main():
    """Función principal que ejecuta todo el análisis."""
    
    try:
        # 1. Cargar datos
        loader, data = cargar_datos()
        
        # 2. Crear variables acumuladas
        data = crear_variables_acumuladas(data)
        
        # 3. Explorar datos
        summary, numeric_vars = explorar_datos(loader)
        
        # 4. ANÁLISIS EN DOS NIVELES (NUEVO)
        resultados_dos_niveles = analisis_dos_niveles(data, DIMENSIONES)
        
        # 5. Análisis descriptivo general
        descriptive_results = analisis_descriptivo(data, numeric_vars)
        
        # 6. Visualizaciones
        generar_visualizaciones(data, numeric_vars, 
                               descriptive_results['correlation_matrix'])
        
        # 7. Exportar resultados
        logger.info("\n📁 Exportando resultados finales...")
        
        # Guardar resultados en Excel
        reporter = ReportGenerator(config.REPORTS_DIR)
        reporter.export_to_excel(
            resultados_dos_niveles,
            'analisis_dos_niveles'
        )
        
        logger.info("✓ Análisis completo finalizado exitosamente")
        
    except Exception as e:
        logger.error(f"Error en el análisis: {str(e)}")
        raise
```

---

## 📋 TABLAS PARA TU TESIS

### Tabla 1: Comparación de Muestras

| Característica | Nivel 1 (General) | Nivel 2 (Institucional) |
|----------------|-------------------|-------------------------|
| **Tamaño muestral** | n = 140 | n = 54 |
| **Factores analizados** | Personal, Tecnológico | Personal, Tecnológico, Institucional |
| **Variables independientes** | 2 | 3 |
| **Pregunta de investigación** | ¿Qué factores universales inciden en la viabilidad? | ¿Cómo influye adicionalmente el contexto institucional? |

### Tabla 2: Resultados de Regresión Múltiple

| Predictor | Nivel 1 (n=140) | Nivel 2 (n=54) |
|-----------|-----------------|----------------|
|           | β | p | β | p |
| Factor Personal | β1 | p1 | β1' | p1' |
| Factor Tecnológico | β2 | p2 | β2' | p2' |
| Factor Institucional | - | - | β3 | p3 |
| **R²** | **R²₁** | - | **R²₂** | - |
| **R² ajustado** | **R²ₐⱼ₁** | - | **R²ₐⱼ₂** | - |

---

## ✅ VENTAJAS DE ESTA ESTRATEGIA

1. ✅ **Aprovecha todos los datos disponibles** (140 casos para análisis general)
2. ✅ **Responde a ambas preguntas de investigación** (universal + institucional)
3. ✅ **Metodológicamente sólido** (Hernández-Sampieri apoya análisis diferenciados)
4. ✅ **Transparente** (claramente reportas n en cada nivel)
5. ✅ **Comparable** (puedes ver el efecto incremental del factor institucional)
6. ✅ **Realista** (reconoce las limitaciones de tus datos)

---

## 🚀 PRÓXIMOS PASOS

¿Quieres que:
1. ✅ **Implemente el código** completo en `main.py`?
2. ✅ **Cree las visualizaciones** específicas para los dos niveles?
3. ✅ **Prepare las tablas formateadas** para tu tesis?

¡Dime y lo hago! 😊
