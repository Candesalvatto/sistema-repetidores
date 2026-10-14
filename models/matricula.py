from config.database import obtener_conexion, cerrar_conexion

class Matricula:
    def __init__(self, id_matricula=None, estudiantes=0, repetidores=0, sobreedad=0, n_anio_grado=0, id_departamento=None, id_ciclo=None, id_nivel=None):
        self.id_matricula = id_matricula
        self.estudiantes = estudiantes
        self.repetidores = repetidores
        self.sobreedad = sobreedad
        self.n_anio_grado = n_anio_grado
        self.id_departamento = id_departamento
        self.id_ciclo = id_ciclo
        self.id_nivel = id_nivel

    def __str__(self):
        return (f"[ID {self.id_matricula}] Año/Grado: {self.n_anio_grado}º | "
                f"Estudiantes: {self.estudiantes} | "
                f"Repetidores: {self.repetidores} (Tasa: {self.tasa_repitencia}%) | "
                f"Sobreedad: {self.sobreedad} (Tasa: {self.tasa_sobreedad}%)")

    # --- GETTERS Y SETTERS CON VALIDACIÓN Y ENCAPSULAMIENTO --- #
    @property
    def estudiantes(self):
        return getattr(self, '_estudiantes', 0)

    @estudiantes.setter
    def estudiantes(self, valor):
        if valor is not None and int(valor) < 0:
            raise ValueError("El número de estudiantes no puede ser negativo.")
        self._estudiantes = int(valor) if valor is not None else 0

    @property
    def repetidores(self):
        return getattr(self, '_repetidores', 0)

    @repetidores.setter
    def repetidores(self, valor):
        if valor is not None and int(valor) < 0:
            raise ValueError("El número de repetidores no puede ser negativo.")
        self._repetidores = int(valor) if valor is not None else 0

    @property
    def sobreedad(self):
        return getattr(self, '_sobreedad', 0)

    @sobreedad.setter
    def sobreedad(self, valor):
        if valor is not None and int(valor) < 0:
            raise ValueError("El número de estudiantes sobreedades no puede ser negativo.")
        self._sobreedad = int(valor) if valor is not None else 0

    # --- CAMPOS CALCULADOS REALEs (PROPIEDADES / TASAS NORMALIZADAS) --- #
    @property
    def tasa_repitencia(self):
        """Calcula la tasa de repitencia sobre la matrícula total (%)"""
        if self.estudiantes and self.estudiantes > 0:
            return round((self.repetidores / self.estudiantes) * 100, 2)
        return 0.0

    @property
    def tasa_sobreedad(self):
        """Calcula la tasa de sobreedad sobre la matrícula total (%)"""
        if self.estudiantes and self.estudiantes > 0:
            return round((self.sobreedad / self.estudiantes) * 100, 2)
        return 0.0

    # --- CRUD OPERATIONS --- #

    # -- CRUD: ALTA --- #
    def guardar_matricula(self):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()

            query = """
                INSERT INTO matricula (
                    id_matricula,
                    estudiantes,
                    repetidores,
                    sobreedad,
                    n_anio_grado,
                    id_departamento,
                    id_ciclo,
                    id_nivel
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(query, (
                self.id_matricula,
                self.estudiantes,
                self.repetidores,
                self.sobreedad,
                self.n_anio_grado,
                self.id_departamento,
                self.id_ciclo,
                self.id_nivel
            ))

            conexion.commit()
            cerrar_conexion(conexion, cursor)

            return self.id_matricula

        return None

    # -- CRUD: MODIFICACIÓN --- #
    def modificar_matricula(self):
        conexion = obtener_conexion()

        if conexion:
            cursor = conexion.cursor()

            query = """
                UPDATE matricula
                SET estudiantes = %s,
                    repetidores = %s,
                    sobreedad = %s,
                    n_anio_grado = %s,
                    id_departamento = %s,
                    id_ciclo = %s,
                    id_nivel = %s
                WHERE id_matricula = %s
            """

            cursor.execute(query, (
                self.estudiantes,
                self.repetidores,
                self.sobreedad,
                self.n_anio_grado,
                self.id_departamento,
                self.id_ciclo,
                self.id_nivel,
                self.id_matricula
            ))

            conexion.commit()
            modificado = cursor.rowcount > 0

            cerrar_conexion(conexion, cursor)

            return modificado

        return False

    # -- CRUD: CONSULTA --- #
    @staticmethod
    def obtener_matriculas():
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT * FROM matricula"
            cursor.execute(query)
            resultados = cursor.fetchall()
            cerrar_conexion(conexion, cursor)
            return resultados
        return []

    @staticmethod
    def obtener_matricula_por_id(id_matricula):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT * FROM matricula WHERE id_matricula = %s"
            cursor.execute(query, (id_matricula,))
            resultado = cursor.fetchone()
            cerrar_conexion(conexion, cursor)
            return resultado
        return None

    # -- BÚSQUEDA 1: POR DEPARTAMENTO -- #
    @staticmethod
    def buscar_por_departamento(id_departamento):
        conexion = obtener_conexion()

        if conexion:
            cursor = conexion.cursor(dictionary=True)

            query = """
                SELECT *
                FROM matricula
                WHERE id_departamento = %s
            """

            cursor.execute(query, (id_departamento,))
            resultados = cursor.fetchall()

            cerrar_conexion(conexion, cursor)

            return resultados

        return []

    # -- BÚSQUEDA 2: POR CICLO LECTIVO -- #
    @staticmethod
    def buscar_por_ciclo(id_ciclo):
        conexion = obtener_conexion()

        if conexion:
            cursor = conexion.cursor(dictionary=True)

            query = """
                SELECT *
                FROM matricula
                WHERE id_ciclo = %s
            """

            cursor.execute(query, (id_ciclo,))
            resultados = cursor.fetchall()

            cerrar_conexion(conexion, cursor)

            return resultados

        return []

    # -- CRUD: BAJA --- #
    @staticmethod
    def eliminar_matricula(id_matricula):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "DELETE FROM matricula WHERE id_matricula = %s"
            cursor.execute(query, (id_matricula,))
            conexion.commit()

            eliminado = cursor.rowcount > 0

            cerrar_conexion(conexion, cursor)

            return eliminado

        return False

    # -- CONSULTA DE LA VIEW -- #
    @staticmethod
    def obtener_vista_matricula():
        conexion = obtener_conexion()

        if conexion:
            cursor = conexion.cursor(dictionary=True)

            query = """
                SELECT *
                FROM vista_matricula_completa
            """

            cursor.execute(query)
            resultados = cursor.fetchall()

            cerrar_conexion(conexion, cursor)

            return resultados

        return []