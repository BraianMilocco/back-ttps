"""
Archivo usado para crear la db del datawarehouse en un primer momento.
No tiene todas las tablas o columnas porque el modelo fue cambiando y se uso mas
el archivo db.py para hacer adiciones a la db mas rapido.

"""

import sqlite3

# Conectar a la base de datos SQLite
conexion = sqlite3.connect("db_etl.db")
cursor = conexion.cursor()


# Confirmar y guardar los cambios en la base de datos
conexion.commit()


create_table_queries = {
    "sedes_espacios": """

        CREATE TABLE sedes_espacios (

            id INTEGER PRIMARY KEY,

            sector TEXT,

            tipo TEXT,

            superficie INTEGER,

            cantidad_pisos INTEGER,

            cantidad_personas_externas INTEGER,

            cantidad_personas_estables INTEGER,

            aprobado BOOLEAN,

            estado TEXT,

            cardio_asistido_desde DATETIME,

            cardio_asistido_vence DATETIME,

            personal_capacitado BOOLEAN,

            senaletica_adecuada BOOLEAN,

            deas INTEGER

        );

    """,
    "entidades": """

        CREATE TABLE entidades (

            id INTEGER PRIMARY KEY,

            razon_social TEXT,

            cuit TEXT

        );

    """,
    "representantes": """

        CREATE TABLE representantes (

            id INTEGER PRIMARY KEY,

            rol TEXT,

            fecha_nacimiento DATETIME

        );

    """,
    "provincias": """

        CREATE TABLE provincias (

            id INTEGER PRIMARY KEY,

            nombre TEXT,

            extension_km INTEGER,

            poblacion INTEGER,

            dias_duracion_certificado INTEGER

        );

    """,
    "muertes_subitas": """

        CREATE TABLE muertes_subitas (

            id INTEGER PRIMARY KEY,

            fecha DATETIME,

            sexo TEXT,

            edad INTEGER,

            fallecio BOOLEAN,

            rcp BOOLEAN,

            tiempo_rcp INTEGER

        );

    """,
    "localidades": """

        CREATE TABLE localidades (

            id INTEGER PRIMARY KEY,

            nombre TEXT,

            extension_km INTEGER,

            poblacion INTEGER,

            provincias_id INTEGER,

            FOREIGN KEY (provincias_id) REFERENCES provincias (id)

        );

    """,
    "inconvenientes": """

        CREATE TABLE inconvenientes (

            id INTEGER PRIMARY KEY,

            fecha DATETIME,

            falta_insumos BOOLEAN,

            en_sitio BOOLEAN,

            respondido_a_descargas BOOLEAN,

            cantidad_descargas INTEGER

        );

    """,
    "hechos_muertes_subitas": """

        CREATE TABLE hechos_muertes_subitas (

            id INTEGER PRIMARY KEY,

            id_sedes_espacios INTEGER,

            id_muertes_subitas INTEGER,

            id_inconvenientes INTEGER,

            id_localidades INTEGER,

            FOREIGN KEY (id_sedes_espacios) REFERENCES sedes_espacios (id),

            FOREIGN KEY (id_muertes_subitas) REFERENCES muertes_subitas (id),

            FOREIGN KEY (id_inconvenientes) REFERENCES inconvenientes (id),

            FOREIGN KEY (id_localidades) REFERENCES localidades (id)

        );

    """,
    "hechos_espacios": """

        CREATE TABLE hechos_espacios (

            id INTEGER PRIMARY KEY,

            id_sedes_espacios INTEGER,

            id_entidades INTEGER,

            id_representantes INTEGER,

            id_localidades INTEGER,

            valida BOOLEAN,
            
            pendiente BOOLEAN,
            
            fecha_creacion DATETIME,
    
            FOREIGN KEY (id_sedes_espacios) REFERENCES sedes_espacios (id),

            FOREIGN KEY (id_entidades) REFERENCES entidades (id),

            FOREIGN KEY (id_representantes) REFERENCES representantes (id),

            FOREIGN KEY (id_localidades) REFERENCES localidades (id)

        );

    """,
}


# Ejecutar las queries para crear las tablas

for table_name, create_query in create_table_queries.items():
    cursor.execute(create_query)

conexion.commit()

tables_created = cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
).fetchall()

print(tables_created)

conexion.close()
