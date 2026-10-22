from models.matricula import Matricula
import subprocess
import sys
from pathlib import Path

def mostrar_menu():
    print("\n" + "="*45)
    print("      SISTEMA DE GESTIÓN DE MATRÍCULAS")
    print("="*45)
    print("1. Alta de matrícula")
    print("2. Baja de matrícula")
    print("3. Modificación de matrícula")
    print("4. Buscar por departamento")
    print("5. Buscar por ciclo lectivo")
    print("6. Consultar vista completa")
    print("7. Ejecutar análisis de datos")
    print("0. Salir")
    print("="*45)

def ejecutar_menu():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            print("\n--- ALTA DE MATRÍCULA ---")
            try:
                id_mat = int(input("ID matrícula: "))
                estudiantes = int(input("Cantidad de estudiantes: "))
                repetidores = int(input("Cantidad de repetidores: "))
                sobreedad = int(input("Cantidad con sobreedad: "))
                n_anio_grado = int(input("Año/grado: "))
                id_departamento = int(input("ID departamento: "))
                id_ciclo = int(input("ID ciclo: "))
                id_nivel = int(input("ID nivel: "))

                nueva_mat = Matricula(
                    id_matricula=id_mat,
                    estudiantes=estudiantes,
                    repetidores=repetidores,
                    sobreedad=sobreedad,
                    n_anio_grado=n_anio_grado,
                    id_departamento=id_departamento,
                    id_ciclo=id_ciclo,
                    id_nivel=id_nivel,
                )

                id_creado = nueva_mat.guardar_matricula()
                if id_creado:

                    # Asignamos el ID generado a la instancia para usar su _str_
                    nueva_mat.id_matricula = id_creado
                    print(f"\n[ÉXITO] Matrícula registrada con ID: {id_creado}")
                    print("-" * 70)
                    print(nueva_mat)
                    print("-" * 70)
                
                    print("VERIFICACIÓN EN BASE DE DATOS (CONSULTA POSTERIOR):")

                    # Consulta posterior para comprobar la persistencia
                    registro_creado = Matricula.obtener_matricula_por_id(id_creado)
                    if registro_creado:
                        print(f"ID: {registro_creado['id_matricula']} | "
                            f"Depto ID: {registro_creado['id_departamento']} | "
                            f"Estudiantes: {registro_creado['estudiantes']} | "
                            f"Repetidores: {registro_creado['repetidores']} | "
                            f"Sobreedad: {registro_creado['sobreedad']}")
                        print("-" * 80)
                    else:
                        print("No se pudo obtener la confirmación del registro.")
                    print("-" * 60)

                else:
                    print("❌ No se pudo registrar la matrícula.")
            except ValueError as e:
                print(f"⚠️ Error de entrada/validación: {e}")

        elif opcion == "2":
            print("\n--- BAJA DE MATRÍCULA ---")
            try:
                id_mat_a_eliminar = int(input("Ingrese el ID de la matrícula a eliminar: "))
                
                if Matricula.eliminar_matricula(id_mat_a_eliminar):  # o eliminar_matricula()
                    print(f"\n[ÉXITO] Matrícula ID {id_mat_a_eliminar} eliminada correctamente.")
                    print("-" * 60)
                    print("VERIFICACIÓN EN BASE DE DATOS (CONSULTA POSTERIOR):")
                    
                    # Búsqueda posterior: Debe retornar None
                    registro_borrado = Matricula.obtener_matricula_por_id(id_mat_a_eliminar)
                    print(f"Búsqueda por ID {id_mat_a_eliminar}: {registro_borrado}")
                    print("Confirmación: El registro ya NO existe en la base de datos.")
                    print("-" * 60)
                else:
                    print(f"\n[ERROR] No se encontró o no se pudo eliminar la matrícula ID {id_mat_a_eliminar}.")

            except ValueError as e:
                print(f"⚠️ Error de entrada: {e}")

        elif opcion == "3":
            print("\n--- MODIFICACIÓN DE MATRÍCULA ---")

            try:
                id_a_modificar = int(input("Ingrese el ID de la matrícula que desea modificar: "))
            except ValueError:
                print("\n[ERROR] El ID debe ser un número entero.")
                return

            # 1. Obtenemos los datos actuales de la base de datos
            registro_actual = Matricula.obtener_matricula_por_id(id_a_modificar)

            if not registro_actual:
                print(f"\n[ERROR] No se encontró ninguna matrícula con el ID {id_a_modificar}.")
            else:
                print(f"\nRegistro encontrado (Presione Enter para MANTENER el valor actual):")
                print("-" * 60)

                # 2. Función auxiliar interna para procesar las entradas opcionales
                def pedir_campo(prompt, valor_actual, es_entero=True):
                    entrada = input(f"{prompt} [Actual: {valor_actual}]: ").strip()
                    if entrada == "":
                        return valor_actual  # Mantiene el valor previo si presionó Enter
                    return int(entrada) if es_entero else entrada

                try:
                    # Solicitamos solo lo que el usuario quiera cambiar
                    nuevo_id_dept = pedir_campo("ID Departamento", registro_actual['id_departamento'])
                    nuevo_id_ciclo = pedir_campo("ID Ciclo Lectivo", registro_actual['id_ciclo'])
                    nuevo_id_nivel = pedir_campo("ID Nivel Educativo", registro_actual['id_nivel'])
                    nuevo_anio = pedir_campo("Año / Grado", registro_actual['n_anio_grado'])
                    nuevos_estudiantes = pedir_campo("Cantidad Estudiantes", registro_actual['estudiantes'])
                    nuevos_repetidores = pedir_campo("Cantidad Repetidores", registro_actual['repetidores'])
                    nueva_sobreedad = pedir_campo("Cantidad Sobreedad", registro_actual['sobreedad'])

                    # 3. Creamos el objeto con los valores actualizados/mantenidos
                    matricula_editada = Matricula(
                        id_matricula=id_a_modificar,
                        id_departamento=nuevo_id_dept,
                        id_ciclo=nuevo_id_ciclo,
                        id_nivel=nuevo_id_nivel,
                        n_anio_grado=nuevo_anio,
                        estudiantes=nuevos_estudiantes,
                        repetidores=nuevos_repetidores,
                        sobreedad=nueva_sobreedad
                    )

                    # 4. Guardamos los cambios
                    if matricula_editada.modificar_matricula(): # o modificar_matricula() según tu nombre de método
                        print(f"\n[ÉXITO] Matrícula ID {id_a_modificar} actualizada correctamente.")
                        print("-" * 60)
                        print("VERIFICACIÓN EN BASE DE DATOS (ESTADO ACTUALIZADO):")
                        
                        # Consulta posterior para la evidencia académica
                        registro_confirmado = Matricula.obtener_matricula_por_id(id_a_modificar)
                        if registro_confirmado:
                            print(f"ID: {registro_confirmado['id_matricula']} | "
                                f"Dept ID: {registro_confirmado['id_departamento']} | "
                                f"Estudiantes: {registro_confirmado['estudiantes']} | "
                                f"Repetidores: {registro_confirmado['repetidores']} | "
                                f"Sobreedad: {registro_confirmado['sobreedad']}")
                        print("-" * 60)
                    else:
                        print(f"\n[ERROR] No se pudo modificar el registro ID {id_a_modificar}.")

                except ValueError:
                    print("\n[ERROR] Ingrese valores numéricos válidos para los campos.")

        elif opcion == "4":
            print("\n--- BÚSQUEDA POR DEPARTAMENTO ---")
    
            try:
                id_depto = int(input("Ingrese el ID del Departamento a consultar: "))
            except ValueError:
                print("\n[ERROR] El ID del departamento debe ser un número entero.")
                return

            # Consultamos a través de la vista
            resultados = Matricula.buscar_por_departamento(id_depto)

            if resultados:
                print("\n" + "=" * 120)
                print(f"RESULTADOS PARA EL DEPARTAMENTO ID: {id_depto}".center(120))
                print("=" * 120)

                # 1. ENCABEZADOS DE COLUMNA (Mismo formato que la Opción 6)
                encabezado = (
                    f"{'ID':<6} "
                    f"{'DEPARTAMENTO':<18} "
                    f"{'CICLO':<8} "
                    f"{'NIVEL':<18} "
                    f"{'AÑO/GRADO':<10} "
                    f"{'ESTUDIANTES':<12} "
                    f"{'REPETIDORES':<12} "
                    f"{'SOBREEDAD':<10} "
                    f"{'% REPIT.':<10} "
                    f"{'% SOBRE.':<10}"
                )
                print(encabezado)
                print("-" * len(encabezado))

                # 2. BUCLE PARA FILAS DE DATOS
                for registro in resultados:
                    dept = registro.get('n_departamento') or registro.get('departamento') or 'N/A'
                    nivel = registro.get('n_nivel') or registro.get('nivel_educativo') or 'N/A'
                    tasa_rep = registro.get('tasa_repitencia', 0.0)
                    tasa_sob = registro.get('tasa_sobreedad', 0.0)

                    fila = (
                        f"{registro['id_matricula']:<6} "
                        f"{dept:<18} "
                        f"{registro['ciclo_lectivo']:<8} "
                        f"{nivel:<18} "
                        f"{registro['n_anio_grado']:<10} "
                        f"{registro['estudiantes']:<12} "
                        f"{registro['repetidores']:<12} "
                        f"{registro['sobreedad']:<10} "
                        f"{tasa_rep:<10.2f} "
                        f"{tasa_sob:<10.2f}"
                    )
                    print(fila)

                print("=" * 120 + "\n")
            else:
                print(f"\n[INFORMACIÓN] No se encontraron registros de matrícula para el departamento ID {id_depto}.")

        elif opcion == "5":
            print("\n--- BÚSQUEDA POR CICLO LECTIVO ---")
            
            try:
                id_ciclo = int(input("Ingrese el ID del Ciclo Lectivo a consultar: "))
            except ValueError:
                print("\n[ERROR] El ID del ciclo debe ser un número entero.")
                return
            
            # Consultamos a través de la vista
            resultados = Matricula.buscar_por_ciclo(id_ciclo)
            
            if resultados:
                print("\n" + "=" * 120)
                print(f"RESULTADOS PARA EL CICLO ID: {id_ciclo}".center(120))
                print("=" * 120)
            
                # 1. ENCABEZADOS DE COLUMNA (Mismo formato que la Opción 6)
                encabezado = (
                    f"{'ID':<6} "
                    f"{'DEPARTAMENTO':<18} "
                    f"{'CICLO':<8} "
                    f"{'NIVEL':<18} "
                    f"{'AÑO/GRADO':<10} "
                    f"{'ESTUDIANTES':<12} "
                    f"{'REPETIDORES':<12} "
                    f"{'SOBREEDAD':<10} "
                    f"{'% REPIT.':<10} "
                    f"{'% SOBRE.':<10}"
                )
                print(encabezado)
                print("-" * len(encabezado))
            
                # 2. BUCLE PARA FILAS DE DATOS
                for registro in resultados:
                    dept = registro.get('n_departamento') or registro.get('departamento') or 'N/A'
                    nivel = registro.get('n_nivel') or registro.get('nivel_educativo') or 'N/A'
                    anio_grado = registro.get('anio_grado') or 'N/A'
                    tasa_rep = registro.get('tasa_repitencia', 0.0)
                    tasa_sob = registro.get('tasa_sobreedad', 0.0)
            
                    fila = (
                        f"{registro['id_matricula']:<6} "
                        f"{dept:<18} "
                        f"{registro['ciclo_lectivo']:<8} "
                        f"{nivel:<18} "
                        f"{anio_grado:<10} "
                        f"{registro['estudiantes']:<12} "
                        f"{registro['repetidores']:<12} "
                        f"{registro['sobreedad']:<10} "
                        f"{tasa_rep:<10.2f} "
                        f"{tasa_sob:<10.2f}"
                    )
                    print(fila)
            
                print("=" * 120 + "\n")
            else:
                print(f"\n[INFORMACIÓN] No se encontraron registros para el ciclo ID {id_ciclo}.")

        elif opcion == "6":
            print("\n--- CONSULTA DE VISTA COMPLETA ---")

            resultados = Matricula.obtener_vista_matricula()

            # Mostrar solamente los primeros 30 registros
            resultados = resultados[:30]

            if resultados:
                print("\n" + "=" * 120)

                encabezado = (
                    f"{'ID':<8}"
                    f"{'DEPARTAMENTO':<20}"
                    f"{'CICLO':<10}"
                    f"{'NIVEL':<18}"
                    f"{'AÑO/GRADO':<12}"
                    f"{'ESTUDIANTES':<14}"
                    f"{'REPETIDORES':<14}"
                    f"{'SOBREEDAD':<12}"
                    f"{'% REPIT.':<12}"
                    f"{'% SOBRE.':<12}"
                )

                print(encabezado)
                print("-" * 120)

                for registro in resultados:
                    print(
                        f"{registro['id_matricula']:<8}"
                        f"{registro['n_departamento']:<20}"
                        f"{registro['ciclo_lectivo']:<10}"
                        f"{registro['n_nivel']:<18}"
                        f"{registro['n_anio_grado']:<12}"
                        f"{registro['estudiantes']:<14}"
                        f"{registro['repetidores']:<14}"
                        f"{registro['sobreedad']:<12}"
                        f"{registro['tasa_repitencia']:<12.2f}"
                        f"{registro['tasa_sobreedad']:<12.2f}"
                    )

                print("=" * 120)
                print(f"Registros mostrados: {len(resultados)} de hasta 30")

            else:
                print("La vista no contiene registros.")
        
        elif opcion == "7":
            print("\n--- ANÁLISIS DE DATOS ---")
            print("Ejecutando procesamiento.py...\n")

            ruta_proyecto = Path(__file__).resolve().parent.parent
            ruta_procesamiento = ruta_proyecto / "procesamiento.py"

            if ruta_procesamiento.exists():
                subprocess.run(
                    [sys.executable, str(ruta_procesamiento)],
                    cwd=str(ruta_proyecto)
                )
                input("\nPresiona Enter para volver al menú...")
            else:
                print("No se encontró el archivo procesamiento.py.")

        elif opcion == "0":
            print("\nSaliendo del sistema. ¡Hasta luego!")
            break