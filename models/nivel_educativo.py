from config.database import obtener_conexion, cerrar_conexion

class NivelEducativo:
    def __init__(self, id_nivel=None, n_nivel=""):
        self.id_nivel = id_nivel
        self.n_nivel = n_nivel

    def __str__(self):
        return f"[{self.id_nivel}] Nivel: {self.n_nivel}"

    # --- GETTERS Y SETTERS CON VALIDACIÓN Y ENCAPSULAMIENTO --- #
    @property
    def id_nivel(self):
        return getattr(self, '_id_nivel', None)

    @id_nivel.setter
    def id_nivel(self, valor):
        if valor is not None and int(valor) <= 0:
            raise ValueError("El ID del nivel educativo debe ser un número entero positivo.")
        self._id_nivel = int(valor) if valor is not None else None

    @property
    def n_nivel(self):
        return getattr(self, '_n_nivel', "")

    @n_nivel.setter
    def n_nivel(self, valor):
        if valor is not None and str(valor).strip() == "":
            raise ValueError("El nombre del nivel educativo no puede estar vacío.")
        self._n_nivel = str(valor).strip() if valor is not None else ""

    # --- MÉTODOS CRUD --- #
    def guardar_nivel_educativo(self):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "INSERT INTO nivel_educativo (id_nivel, n_nivel) VALUES (%s, %s)"
            cursor.execute(query, (self.id_nivel, self.n_nivel))
            conexion.commit()
            cerrar_conexion(conexion, cursor)
            return self.id_nivel
        return None

    def modificar_nivel_educativo(self):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "UPDATE nivel_educativo SET n_nivel = %s WHERE id_nivel = %s"
            cursor.execute(query, (self.n_nivel, self.id_nivel))
            conexion.commit()
            modificado = cursor.rowcount > 0  # Verificación real por rowcount
            cerrar_conexion(conexion, cursor)
            return modificado
        return False

    @staticmethod
    def borrar_nivel_educativo(id_nivel):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "DELETE FROM nivel_educativo WHERE id_nivel = %s"
            cursor.execute(query, (id_nivel,))
            conexion.commit()
            borrado = cursor.rowcount > 0  # Verificación real por rowcount
            cerrar_conexion(conexion, cursor)
            return borrado
        return False

    @staticmethod
    def obtener_niveles_educativos():
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT * FROM nivel_educativo"
            cursor.execute(query)
            resultados = cursor.fetchall()
            cerrar_conexion(conexion, cursor)
            return resultados
        return []