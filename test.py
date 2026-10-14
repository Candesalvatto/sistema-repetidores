from models.matricula import Matricula

def test_guardar_matricula():
    # Crear una instancia de Matricula con datos de prueba
    matricula = Matricula(id_matricula = 9999, estudiantes=30, repetidores=5, sobreedad=2, n_anio_grado=3, id_departamento=14007, id_ciclo=5, id_nivel=1)

    # Guardar la matrícula en la base de datos
    matricula.guardar_matricula()

    # Verificar que se haya guardado correctamente
    assert matricula.id_matricula is not None, "La matrícula no se guardó correctamente."

    #mostrar ultimos registros
    matriculas = Matricula.obtener_matriculas()
    print("Últimos registros de matrícula:")
    for m in matriculas[-5:]:  # Mostrar los últimos 5 registros
        print(m)

def borrar_matricula(id_matricula):
    # Borrar la matrícula de prueba
    resultado = Matricula.eliminar_matricula(id_matricula)
    assert resultado is True, "La matrícula no se borró correctamente."

def ver_matriculas():
    # Obtener todas las matrículas
    matriculas = Matricula.obtener_matriculas()
    print("Matrículas en la base de datos:")
    for m in matriculas:
        print(m)

if __name__ == "__main__":
    ver_matriculas()  # Mostrar todas las matrículas
    # Borrar la matrícula de prueba si existe
    