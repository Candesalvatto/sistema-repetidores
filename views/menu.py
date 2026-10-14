from models.matricula import Matricula

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
                    id_nivel=id_nivel
                )

                id_creado = nueva_mat.guardar_matricula()
                if id_creado:
                    print("\n✅ Matrícula registrada correctamente.")
                    # CONSULTA POSTERIOR DE CONFIRMACIÓN REAL
                    print("🔍 Confirmación desde la base de datos:")
                    reg = Matricula.obtener_matricula_por_id(id_creado)
                    print(reg)
                else:
                    print("❌ No se pudo registrar la matrícula.")

            except ValueError as e:
                print(f"⚠️ Error de entrada/validación: {e}")

        elif opcion == "2":
            print("\n--- BAJA DE MATRÍCULA ---")
            try:
                id_mat = int(input("Ingrese el ID de la matrícula a eliminar: "))
                
                eliminado = Matricula.eliminar_matricula(id_mat)
                if eliminado:
                    print("\n✅ Matrícula eliminada correctamente.")
                    # CONSULTA POSTERIOR DE CONFIRMACIÓN (Verificar que devuelve None/vacío)
                    print("🔍 Confirmación de ausencia en la base de datos:")
                    reg = Matricula.obtener_matricula_por_id(id_mat)
                    if reg is None:
                        print(f"✔️ Confirmado: El registro con ID {id_mat} ya no existe en la base de datos.")
                    else:
                        print("⚠️ El registro aún parece existir.")
                else:
                    print(f"⚠️ No se encontró ninguna matrícula con ID {id_mat} para eliminar.")

            except ValueError as e:
                print(f"⚠️ Error de entrada: {e}")

        elif opcion == "3":
            print("\n--- MODIFICACIÓN DE MATRÍCULA ---")
            try:
                id_mat = int(input("ID de la matrícula a modificar: "))
                
                # Verificar primero si existe antes de pedir nuevos datos
                reg_existente = Matricula.obtener_matricula_por_id(id_mat)
                if not reg_existente:
                    print(f"⚠️ No existe ninguna matrícula con ID {id_mat}.")
                    continue

                estudiantes = int(input("Nueva cantidad de estudiantes: "))
                repetidores = int(input("Nueva cantidad de repetidores: "))
                sobreedad = int(input("Nueva cantidad con sobreedad: "))
                n_anio_grado = int(input("Nuevo año/grado: "))
                id_departamento = int(input("Nuevo ID departamento: "))
                id_ciclo = int(input("Nuevo ID ciclo: "))
                id_nivel = int(input("Nuevo ID nivel: "))

                mat_mod = Matricula(
                    id_matricula=id_mat,
                    estudiantes=estudiantes,
                    repetidores=repetidores,
                    sobreedad=sobreedad,
                    n_anio_grado=n_anio_grado,
                    id_departamento=id_departamento,
                    id_ciclo=id_ciclo,
                    id_nivel=id_nivel
                )

                modificado = mat_mod.modificar_matricula()
                if modificado:
                    print("\n✅ Matrícula modificada correctamente.")
                    # CONSULTA POSTERIOR DE CONFIRMACIÓN REAL
                    print("🔍 Estado actualizado en la base de datos:")
                    reg_actualizado = Matricula.obtener_matricula_por_id(id_mat)
                    print(reg_actualizado)
                else:
                    print("❌ No se realizaron cambios en la matrícula.")

            except ValueError as e:
                print(f"⚠️ Error de entrada/validación: {e}")

        elif opcion == "4":
            print("\n--- BÚSQUEDA POR DEPARTAMENTO ---")
            try:
                id_dep = int(input("Ingrese el ID del departamento: "))
                resultados = Matricula.buscar_por_departamento(id_dep)
                if resultados:
                    print(f"\nSe encontraron {len(resultados)} registro(s):")
                    for r in resultados:
                        print(r)
                else:
                    print("No se encontraron registros para ese departamento.")
            except ValueError:
                print("⚠️ Debe ingresar un número entero para el ID.")

        elif opcion == "5":
            print("\n--- BÚSQUEDA POR CICLO LECTIVO ---")
            try:
                id_ciclo = int(input("Ingrese el ID del ciclo: "))
                resultados = Matricula.buscar_por_ciclo(id_ciclo)
                if resultados:
                    print(f"\nSe encontraron {len(resultados)} registro(s):")
                    for r in resultados:
                        print(r)
                else:
                    print("No se encontraron registros para ese ciclo lectivo.")
            except ValueError:
                print("⚠️ Debe ingresar un número entero para el ID.")

        elif opcion == "6":
            print("\n--- CONSULTAR VISTA COMPLETA ---")
            vista = Matricula.obtener_vista_matricula()
            if vista:
                print(f"\n{'ID':<6} | {'DEPARTAMENTO':<15} | {'CICLO':<6} | {'NIVEL':<12} | {'AÑO':<4} | {'MATRÍCULA':<10} | {'REPET.':<7} | {'SOBREED.':<8} | {'T.REP(%)':<9} | {'T.SOBR(%)':<9}")
                print("-" * 115)
                for fila in vista:
                    tasa_rep = fila.get('tasa_repitencia', 0.0)
                    tasa_sob = fila.get('tasa_sobreedad', 0.0)
                    print(f"{fila['id_matricula']:<6} | {fila['n_departamento']:<15} | {fila['ciclo_lectivo']:<6} | {fila['n_nivel']:<12} | {fila['n_anio_grado']:<4} | {fila['estudiantes']:<10} | {fila['repetidores']:<7} | {fila['sobreedad']:<8} | {tasa_rep:<9} | {tasa_sob:<9}")
            else:
                print("No se encontraron registros en la vista.")

        elif opcion == "0":
            print("\n¡Gracias por utilizar el sistema! 👋")
            break

        else:
            print("⚠️ Opción no válida. Intente de nuevo.")