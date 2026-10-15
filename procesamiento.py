import pandas as pd
import numpy as np
from config.database import obtener_conexion, cerrar_conexion

# 1. CARGA DE DATOS DESDE LA VISTA A PANDAS
conexion = obtener_conexion()

if conexion:
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM vista_matricula_completa"
    cursor.execute(query)
    datos = cursor.fetchall()
    cerrar_conexion(conexion, cursor)

    # Convertimos la lista de diccionarios a un DataFrame de Pandas
    df = pd.DataFrame(datos)

    # CONVERSIÓN DE DECIMAL A FLOAT (Solución al TypeError)
    df['tasa_repitencia'] = df['tasa_repitencia'].astype(float)
    df['tasa_sobreedad'] = df['tasa_sobreedad'].astype(float)

    print("--- VISTA PREVIA DE LOS DATOS ---")
    print(df.head())

    # 2. ESTADISTICAS DESCRIPTIVAS (describe)
    print("\n--- ESTADISTICAS DESCRIPTIVAS ---")
    cols_num = ['estudiantes', 'repetidores', 'sobreedad', 'tasa_repitencia', 'tasa_sobreedad']
    print(df[cols_num].describe().round(2))

    # 3. OPERACION CON NUMPY
    mediana_sobreedad = np.median(df['tasa_sobreedad'])
    desviacion_sobreedad = np.std(df['tasa_sobreedad'])
    print(f"\nMediana de la Tasa de Sobreedad: {mediana_sobreedad:.2f}%")
    print(f"Desviación Estándar de la Tasa de Sobreedad: {desviacion_sobreedad:.2f}%")

    # 4. RESPUESTAS A LAS 5 PREGUNTAS DE ANALISIS

    # Pregunta 1: Promedio de tasa de sobreedad por departamento y ciclo lectivo
    p1 = df.groupby(['n_departamento', 'ciclo_lectivo'])['tasa_sobreedad'].mean().round(2)
    print("\n1. Promedio de Tasa de Sobreedad por Departamento y Año:")
    print(p1.head())

    # Pregunta 2: Máximo de repetidores por año o grado
    p2 = df.groupby('n_anio_grado')['repetidores'].max()
    print("\n2. Máximo de Repetidores por Año/Grado:")
    print(p2)

    # Pregunta 3: Tasa mínima de repitencia en el último ciclo lectivo (Filtro 1)
    ultimo_ciclo = df['ciclo_lectivo'].max()
    df_ultimo = df[df['ciclo_lectivo'] == ultimo_ciclo]
    p3 = df_ultimo.groupby('n_departamento')['tasa_repitencia'].min().round(2)
    print(f"\n3. Tasa Mínima de Repitencia por Departamento en {ultimo_ciclo}:")
    print(p3.head())

    # Pregunta 4: Suma total de repetidores y sobreedad por año y departamento
    p4 = df.groupby(['ciclo_lectivo', 'n_departamento'])[['repetidores', 'sobreedad']].sum()
    print("\n4. Suma Total de Repetidores y Sobreedad por Año y Departamento:")
    print(p4.head())

    # Pregunta 5: Filtro por Nivel Secundario y agrupamiento (Filtro 2)
    df_secundario = df[df['n_nivel'] == 'Secundario']
    p5 = df_secundario.groupby(['n_departamento', 'ciclo_lectivo']).agg({
        'repetidores': 'sum',
        'tasa_sobreedad': 'mean'
    }).round(2)
    print("\n5. Repetidores y Promedio de Tasa de Sobreedad en Secundario:")
    print(p5.head())

else:
    print("No se pudo establecer conexión con la base de datos.")