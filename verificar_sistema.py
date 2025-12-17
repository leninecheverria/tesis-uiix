#!/usr/bin/env python3
"""
Script de verificación del sistema.

Verifica que todas las dependencias estén instaladas y que el sistema
esté listo para usar.

Autor: Sistema de Análisis de Tesis
Fecha: Diciembre 2025
"""

import sys
from pathlib import Path

print("="*80)
print("VERIFICACIÓN DEL SISTEMA DE ANÁLISIS")
print("="*80)
print()

# Lista de verificaciones
checks = []

# 1. Verificar Python
print("1. Verificando versión de Python...")
py_version = sys.version_info
if py_version.major >= 3 and py_version.minor >= 8:
    print(f"   ✓ Python {py_version.major}.{py_version.minor}.{py_version.micro}")
    checks.append(True)
else:
    print(f"   ✗ Python {py_version.major}.{py_version.minor} (se requiere >= 3.8)")
    checks.append(False)

# 2. Verificar estructura de directorios
print("\n2. Verificando estructura de directorios...")
required_dirs = ['BD', 'src', 'config', 'results', 'notebooks']
for dir_name in required_dirs:
    dir_path = Path(dir_name)
    if dir_path.exists():
        print(f"   ✓ {dir_name}/")
        checks.append(True)
    else:
        print(f"   ✗ {dir_name}/ no encontrado")
        checks.append(False)

# 3. Verificar archivos principales
print("\n3. Verificando archivos principales...")
required_files = ['main.py', 'explorar_datos.py', 'requirements.txt', 'README.md']
for file_name in required_files:
    file_path = Path(file_name)
    if file_path.exists():
        print(f"   ✓ {file_name}")
        checks.append(True)
    else:
        print(f"   ✗ {file_name} no encontrado")
        checks.append(False)

# 4. Verificar archivos de datos
print("\n4. Verificando archivos de datos...")
bd_dir = Path('BD')
if bd_dir.exists():
    data_files = list(bd_dir.glob('*'))
    if data_files:
        print(f"   ✓ Se encontraron {len(data_files)} archivo(s) en BD/:")
        for f in data_files:
            print(f"     - {f.name}")
        checks.append(True)
    else:
        print("   ⚠ La carpeta BD/ está vacía")
        checks.append(False)
else:
    print("   ✗ Carpeta BD/ no encontrada")
    checks.append(False)

# 5. Verificar dependencias Python
print("\n5. Verificando dependencias Python...")
dependencies = [
    ('pandas', 'Manipulación de datos'),
    ('numpy', 'Cálculos numéricos'),
    ('scipy', 'Estadística científica'),
    ('matplotlib', 'Visualización'),
    ('seaborn', 'Gráficos estadísticos'),
    ('pyreadstat', 'Lectura de archivos SPSS'),
    ('openpyxl', 'Exportación a Excel'),
    ('sklearn', 'Análisis estadístico'),
]

installed_count = 0
for package, description in dependencies:
    try:
        __import__(package)
        print(f"   ✓ {package:15s} - {description}")
        installed_count += 1
        checks.append(True)
    except ImportError:
        print(f"   ✗ {package:15s} - {description} (NO INSTALADO)")
        checks.append(False)

if installed_count == len(dependencies):
    print(f"\n   ✓ Todas las dependencias ({installed_count}/{len(dependencies)}) están instaladas")
else:
    print(f"\n   ⚠ Faltan {len(dependencies) - installed_count} dependencias")
    print("   Ejecuta: pip install -r requirements.txt")

# 6. Verificar módulos del proyecto
print("\n6. Verificando módulos del proyecto...")
sys.path.insert(0, str(Path.cwd() / 'src'))

modules = [
    ('src.data_loader', 'DataLoader'),
    ('src.reliability_analysis', 'ReliabilityAnalyzer'),
    ('src.descriptive_stats', 'DescriptiveAnalyzer'),
    ('src.inferential_stats', 'InferentialAnalyzer'),
    ('src.visualization', 'DataVisualizer'),
    ('src.report_generator', 'ReportGenerator'),
]

for module_name, class_name in modules:
    try:
        module = __import__(module_name, fromlist=[class_name])
        getattr(module, class_name)
        print(f"   ✓ {module_name.replace('src.', '')}")
        checks.append(True)
    except Exception as e:
        print(f"   ✗ {module_name.replace('src.', '')} - Error: {str(e)[:50]}")
        checks.append(False)

# Resumen final
print("\n" + "="*80)
print("RESUMEN DE VERIFICACIÓN")
print("="*80)

passed = sum(checks)
total = len(checks)
percentage = (passed / total * 100) if total > 0 else 0

print(f"\nVerificaciones exitosas: {passed}/{total} ({percentage:.1f}%)")

if percentage == 100:
    print("\n✅ SISTEMA COMPLETAMENTE FUNCIONAL")
    print("\nPróximos pasos:")
    print("  1. python explorar_datos.py    - Explorar tus datos")
    print("  2. Editar main.py               - Definir dimensiones")
    print("  3. python main.py               - Ejecutar análisis completo")
elif percentage >= 80:
    print("\n⚠ SISTEMA CASI LISTO")
    print("\nFaltan algunas dependencias. Ejecuta:")
    print("  pip install -r requirements.txt")
elif percentage >= 50:
    print("\n⚠ SISTEMA PARCIALMENTE FUNCIONAL")
    print("\nInstalación requerida:")
    print("  pip install -r requirements.txt")
else:
    print("\n❌ SISTEMA NO FUNCIONAL")
    print("\nPasos requeridos:")
    print("  1. Verificar que estás en el directorio correcto")
    print("  2. pip install -r requirements.txt")
    print("  3. Verificar que los archivos de datos están en BD/")

print("\n" + "="*80)
print()
