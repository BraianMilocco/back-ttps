import sqlite3

""""
Este archivo es el mismo que db_etl.py solo que este tiene los metodos utilizados
Para crear tablas o modificar tablas de la db. 
"""


class DB:
    RUTA_DB = "test.db"

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

    def close_db(self):
        self.conexion.close()
        self.conexion = None

    def modificar_tabla_espacios_obligados(self):
        try:
            cursor = self.conexion.cursor()
            cursor.execute(
                "ALTER TABLE espacios_obligados ADD COLUMN estado_auxiliar TIPO_DATO"
            )
            cursor.execute("UPDATE espacios_obligados SET estado_auxiliar = estado")
            self.conexion.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error al modificar la tabla: {e}")
            return False

    def modificar_tabla_agregar_fecha_nacimiento(self):
        try:
            cursor = self.conexion.cursor()
            # Agregar la columna fecha_nacimiento de tipo DATETIME
            cursor.execute("ALTER TABLE users ADD COLUMN fecha_nacimiento DATETIME")

            # Opcional: Actualizar la columna con datos, si es necesario
            # Aquí tendrás que definir cómo quieres establecer estas fechas

            self.conexion.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error al modificar la tabla: {e}")
            return False

    def modificar_hechos_espacios(self):
        cursor = self.conexion.cursor()
        cursor.execute("ALTER TABLE hechos_espacios ADD COLUMN valida  BOOLEAN")
        self.conexion.commit()
        cursor = self.conexion.cursor()
        cursor.execute("ALTER TABLE hechos_espacios ADD COLUMN pendiente  BOOLEAN")
        self.conexion.commit()
        cursor = self.conexion.cursor()
        cursor.execute("ALTER TABLE hechos_espacios ADD COLUMN fecha_creacion DATETIME")
        self.conexion.commit()
        cursor.close()

    def crear_tabla_localidades(self):
        cursor = self.conexion.cursor()
        cursor.execute(
            """
            CREATE TABLE localidades (

            id INTEGER PRIMARY KEY,

            nombre TEXT,

            extension_km INTEGER,

            poblacion INTEGER,

            provincias_id INTEGER,

            FOREIGN KEY (provincias_id) REFERENCES provincias (id)

            );
            """
        )
        self.conexion.commit()
        cursor.close()

    def agregar_localidad_a_sede(self):
        cursor = self.conexion.cursor()

        # Añadir la columna 'localidad_id' a la tabla 'sedes'
        cursor.execute("ALTER TABLE sedes ADD localidad_id INT")

        # Establecer la columna 'localidad_id' como clave foránea que referencia a 'localidades'
        # cursor.execute("""
        #     ALTER TABLE sedes
        #     ADD CONSTRAINT fk_localidades
        #     FOREIGN KEY (localidad_id) REFERENCES localidades(id)
        # """)

        self.conexion.commit()

    def agregar_campo_etl_a_tablas(self):
        # Traer Todas las Tablas de la Base de Datos
        cursor = self.conexion.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()
        for tabla in tablas:
            # Agregar un campo BOOL que se llame etl
            cursor.execute(f"ALTER TABLE {tabla[0]} ADD COLUMN etl BOOLEAN")
            # Actualizar el campo etl a False
            cursor.execute(f"UPDATE {tabla[0]} SET etl = 0")
            self.conexion.commit()
        cursor.close()

    def agregar_edad_usuarios(self):
        cursor = self.conexion.cursor()
        cursor.execute("ALTER TABLE representantes ADD COLUMN edad INTEGER")
        self.conexion.commit()
        cursor.close()

    def agregar_porcentaje_solidarios_a_sedes_espacios(self):
        cursor = self.conexion.cursor()
        cursor.execute("ALTER TABLE sedes_espacios ADD COLUMN deas_solidarios INTEGER")
        self.conexion.commit()
        cursor.close()

    def crear_tabla_cambios_de_estados(self):
        cursor = self.conexion.cursor()
        cursor.execute(
            """
            CREATE TABLE cambios_de_estados (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            dias INTEGER,

            estado_anterior TEXT,

            estado_nuevo TEXT,

            sedes_espacios_id INTEGER,

            FOREIGN KEY (sedes_espacios_id) REFERENCES sedes_espacios (id)

            );
            """
        )
        self.conexion.commit()
        cursor.close()


# # # # Ejemplo de consulta SQL
# db = DB()
# db.conectar_db('db_etl_provincias_y_localidades.db')
# db.crear_tabla_cambios_de_estados()
