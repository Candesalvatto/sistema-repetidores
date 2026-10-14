from config.database import obtener_conexion, cerrar_conexion

class Departamento:
    def __init__(self, id_departamento=None, n_departamento=""):
        self.id_departamento = id_departamento
        self.n_departamento = n_departamento

    def __str__(self):
        return f"[{self.id_departamento}] {self.n_departamento}"

    # --- GETTERS Y SETTERS CON VALIDACIÓN Y ENCAPSULAMIENTO --- #
    @property
    def id_departamento(self):
        return getattr(self, '_id_departamento', None)

    @id_departamento.setter
    def id_departamento(self, valor):
        if valor is not None and int(valor) <= 0:
            raise ValueError("El ID del departamento debe ser un número entero positivo.")
        self._id_departamento = int(valor) if valor is not None else None

    @property
    def n_departamento(self):
        return getattr(self, '_n_departamento', "")

    @n_departamento.setter
    def n_departamento(self, valor):
        if valor is not None and str(valor).strip() == "":
            raise ValueError("El nombre del departamento no puede estar vacío.")
        self._n_departamento = str(valor).strip() if valor is not None else ""

    # --- MÉTODOS CRUD --- #
    def guardar_departamento(self):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "INSERT INTO departamentos (id_departamento, n_departamento) VALUES (%s, %s)"
            cursor.execute(query, (self.id_departamento, self.n_departamento))
            conexion.commit()
            cerrar_conexion(conexion, cursor)
            return self.id_departamento
        return None

    def modificar_departamento(self):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "UPDATE departamentos SET n_departamento = %s WHERE id_departamento = %s"
            cursor.execute(query, (self.n_departamento, self.id_departamento))
            conexion.commit()
            modificado = cursor.rowcount > 0
            cerrar_conexion(conexion, cursor)
            return modificado
        return False

    @staticmethod
    def obtener_departamentos():
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT * FROM departamentos"
            cursor.execute(query)
            resultados = cursor.fetchall()
            cerrar_conexion(conexion, cursor)
            return resultados
        return []

    @staticmethod
    def obtener_departamento_por_nombre(nombre):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT * FROM departamentos WHERE n_departamento LIKE %s"
            cursor.execute(query, (f"%{nombre}%",))
            resultados = cursor.fetchall()
            cerrar_conexion(conexion, cursor)
            return resultados
        return []

    @staticmethod
    def borrar_departamento(id_departamento):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "DELETE FROM departamentos WHERE id_departamento = %s"
            cursor.execute(query, (id_departamento,))
            conexion.commit()
            borrado = cursor.rowcount > 0
            cerrar_conexion(conexion, cursor)
            return borrado
        return False