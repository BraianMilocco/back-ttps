import sqlite3


class DB:
    RUTA_DB = "test____asd.db"

    def __init__(self):
        self.conexion = None

    def conectar_db(self, ruta_db=None):
        if ruta_db is None:
            ruta_db = self.RUTA_DB
        conexion = sqlite3.connect(ruta_db)
        self.conexion = conexion
        return conexion

    def consultar_db(self, consulta):
        cursor = self.conexion.cursor()
        cursor.execute(consulta)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    def insertar_db(self, consulta):
        try:
            cursor = self.conexion.cursor()
            cursor.execute(consulta)
            self.conexion.commit()  # Importante para confirmar la inserción
            cursor.close()
            return True  # O algún mensaje de éxito
        except Exception as e:
            print(f"Error al insertar: {e}")
            return False  # O algún mensaje de error
        return True

    def actualizar_db(self, consulta):
        try:
            cursor = self.conexion.cursor()
            cursor.execute(consulta)
            self.conexion.commit()  # Importante para confirmar la inserción
            cursor.close()
            return True  # O algún mensaje de éxito
        except Exception as e:
            print(f"Error al actualizar: {e}")
            return False

    def close_db(self):
        self.conexion.close()
        self.conexion = None
