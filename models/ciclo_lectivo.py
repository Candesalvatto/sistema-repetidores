from config.database import obtener_conexion, cerrar_conexion

class CicloLectivo:
    def __init__(self, id_ciclo=None, ciclo_lectivo=0):
        self.id_ciclo = id_ciclo
        self.ciclo_lectivo = ciclo_lectivo

    def __str__(self):
        return f"[{self.id_ciclo}] Ciclo Lectivo: {self.ciclo_lectivo}"

    # --- GETTERS Y SETTERS CON VALIDACIÓN Y ENCAPSULAMIENTO --- #
    @property
    def id_ciclo(self):
        return getattr(self, '_id_ciclo', None)

    @id_ciclo.setter
    def id_ciclo(self, valor):
        if valor is not None and int(valor) <= 0:
            raise ValueError("El ID del ciclo lectivo debe ser un número entero positivo.")
        self._id_ciclo = int(valor) if valor is not None else None

    @property
    def ciclo_lectivo(self):
        return getattr(self, '_ciclo_lectivo', 0)

    @ciclo_lectivo.setter
    def ciclo_lectivo(self, valor):
        if valor is not None and int(valor) < 1900:
            raise ValueError("El año del ciclo lectivo debe ser un año válido (mayor a 1900).")
        self._ciclo_lectivo = int(valor) if valor is not None else 0

    # --- MÉTODOS CRUD --- #
    def guardar_ciclo_lectivo(self):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "INSERT INTO ciclo_lectivo (id_ciclo, ciclo_lectivo) VALUES (%s, %s)"
            cursor.execute(query, (self.id_ciclo, self.ciclo_lectivo))
            conexion.commit()
            cerrar_conexion(conexion, cursor)
            return self.id_ciclo
        return None

    def modificar_ciclo_lectivo(self):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "UPDATE ciclo_lectivo SET ciclo_lectivo = %s WHERE id_ciclo = %s"
            cursor.execute(query, (self.ciclo_lectivo, self.id_ciclo))
            conexion.commit()
            modificado = cursor.rowcount > 0  # Verificación real por rowcount
            cerrar_conexion(conexion, cursor)
            return modificado
        return False

    @staticmethod
    def eliminar_ciclo_lectivo(id_ciclo):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "DELETE FROM ciclo_lectivo WHERE id_ciclo = %s"
            cursor.execute(query, (id_ciclo,))
            conexion.commit()
            eliminado = cursor.rowcount > 0  # Verificación real por rowcount
            cerrar_conexion(conexion, cursor)
            return eliminado
        return False

    @staticmethod
    def obtener_ciclo_lectivo_por_id(id_ciclo):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT * FROM ciclo_lectivo WHERE id_ciclo = %s"
            cursor.execute(query, (id_ciclo,))
            resultado = cursor.fetchone()
            cerrar_conexion(conexion, cursor)
            return resultado
        return None

    @staticmethod
    def obtener_ciclos_lectivos():
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT * FROM ciclo_lectivo"
            cursor.execute(query)
            resultados = cursor.fetchall()
            cerrar_conexion(conexion, cursor)
            return resultados
        return []