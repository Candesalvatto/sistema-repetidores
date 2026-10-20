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
    print("\nLos 5 casos más altos:")
    print(p1.sort_values(ascending=False).head(5))
    print("\nLos 3 casos más bajos:")
    print(p1.sort_values().head(3))
    print("\nPromedio de toda la provincia, año por año:")
    print(df.groupby('ciclo_lectivo')['tasa_sobreedad'].mean().round(2))

    # Pregunta 2: Máximo de repetidores por año o grado
    p2 = df.groupby(['n_nivel', 'n_anio_grado'])['repetidores'].max()
    print("\n2. Máximo de Repetidores por Año/Grado, entre 2021 - 2025:")
    maximo = df['repetidores'].max()
    print(p2)
    print("Dónde ocurrió el máximo de todos:")
    print(df[df['repetidores'] == maximo][['n_departamento', 'ciclo_lectivo', 'n_nivel', 'n_anio_grado', 'repetidores']])

    # Pregunta 3: Tasa mínima de repitencia en el último ciclo lectivo (Filtro 1)
    ultimo_ciclo = df['ciclo_lectivo'].max()
    df_ultimo = df[df['ciclo_lectivo'] == ultimo_ciclo]
    print(f"\n3. Tasa de Repitencia por Departamento en {ultimo_ciclo}:")
    p3 = df_ultimo.groupby('n_departamento')[['repetidores', 'estudiantes']].sum()
    p3['tasa_repitencia'] = (p3['repetidores'] / p3['estudiantes'] * 100).round(2)
    p3 = p3.sort_values('tasa_repitencia')
    print("Las 3 más bajas:")
    print(p3.head(3))
    print("Las 3 más altas:")
    print(p3.tail(3))

    # Pregunta 4: Suma total de repetidores y sobreedad por año y departamento
    print("\n4.Totales de toda la provincia, por año:")
    print(df.groupby('ciclo_lectivo')[['estudiantes', 'repetidores', 'sobreedad']].sum())
    p4 = df_ultimo.groupby('n_departamento')[['repetidores', 'sobreedad']].sum()
    print(f"Los 5 departamentos con más sobreedad en {ultimo_ciclo}:")
    print(p4.sort_values('sobreedad', ascending=False).head(5))

    # Pregunta 5: Filtro por Nivel Secundario y agrupamiento (Filtro 2)
    df_secundario = df[df['n_nivel'] == 'Secundario']
    p5 = df_secundario.groupby(['n_departamento', 'ciclo_lectivo']).agg({
        'repetidores': 'sum',
        'tasa_repitencia': 'mean',
        'tasa_sobreedad': 'mean'
    }).round(2)
    print("\n5. Tasa de repitencia y Tasa de Sobreedad en Secundario en toda la provincia, año por año:")
    print(df_secundario.groupby('ciclo_lectivo')[['tasa_repitencia', 'tasa_sobreedad']].mean().round(2))
    print("Correlación entre repitencia y sobreedad:", round(p5['tasa_repitencia'].corr(p5['tasa_sobreedad']), 2))

else:
    print("No se pudo establecer conexión con la base de datos.")