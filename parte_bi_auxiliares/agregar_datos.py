"""
Este es el script utilizado para cargar datos a las diferentes tablas de la base de datos 'original'.
Con el fin de tener un data set bastante aleatorio y grande para poder realizar los graficos de power bi
"""
# import string

# from db import DB
# from auxiliares import (
#     sectores,
#     tipos,
#     latitudes,
#     longitudes,
#     id_generator,
#     get_random_index,
#     get_random_from_range,
#     estados,
#     generar_fecha_aleatoria,
#     fechas_estado_vencido,
# )
# from localidades import localidades, provincias_localidades_en_db

# # db = DB()
# # db.conectar_db("test.db")

# INSERT_AT = 5000

# base_query = "INSERT INTO localidades (nombre, provincias_id, poblacion, extension_km) VALUES "
# for localidad in localidades:
#     base_query += '("{}", {}, {}, {}),'.format(
#         localidad["nombre"],
#         localidad["provincia_id"],
#         localidad["poblacion"],
#         localidad["extension_km"],
#     )
# base_query = base_query[:-1] + ";"
# resultad = db.insertar_db(base_query)
# print(resultad)

# def get_ids_entidades():
#     consulta = "SELECT id FROM entidades;"
#     resultados = db.consultar_db(consulta)
#     return [resultado[0] for resultado in resultados]


# def get_entidad(id):
#     base_id = 100

#     return {
#         "id": base_id + id,
#         "cuit": id_generator(25, string.digits),
#         "razon_social": id_generator(30),
#     }


# def get_sede(id, entidad_id):
#     base_id = 20
#     _id = base_id + id
#     sector = get_random_index(sectores)
#     tipo = get_random_index(tipos[sector])
#     return {
#         "id": _id,
#         "nombre": id_generator(25),
#         "numero": _id,
#         "sector": sector,
#         "tipo": tipo,
#         "latitud": latitudes(),
#         "longitud": longitudes(),
#         "superficie": get_random_from_range(100, 10000),
#         "cantidad_pisos": get_random_from_range(0, 20),
#         "cantidad_personas_externas": get_random_from_range(0, 1000),
#         "cantidad_personas_estables": get_random_from_range(0, 1000),
#         "provincia_id": get_random_from_range(1, 24),
#         "entidad_id": entidad_id,
#     }


# def get_espacio(id, sede_id):
#     id_base = 5020
#     _id = id_base + id
#     estado_auxiliar = get_random_index(estados)
#     desde, hasta = fechas_estado_vencido(estado_auxiliar)
#     return {
#         "id": _id,
#         "nombre": id_generator(25),
#         "aprobado": get_random_index(
#             [True, False, True, True, True, True, True, True, True]
#         ),
#         "estado": "En proceso de ser Cardio-Asistido",
#         "estado_auxiliar": estado_auxiliar,
#         "sede_id": sede_id,
#         "cardio_asistido_desde": desde,
#         "cardio_asistido_vence": hasta,
#         "cardio_asistido_vencido": (
#             estado_auxiliar == "Cardio-Asistido Certificado Vencido"
#         ),
#         "ddjj_personal_capacitado": True
#         if estado_auxiliar != "En proceso de ser Cardio-Asistido"
#         else get_random_index([True, False]),
#         "ddjj_senaletica_adecuada": True
#         if estado_auxiliar != "En proceso de ser Cardio-Asistido"
#         else get_random_index([True, False]),
#         "ddjj_cantidad_deas": get_random_from_range(0, 10)
#         if estado_auxiliar != "En proceso de ser Cardio-Asistido"
#         else get_random_from_range(1, 300),
#     }


# cantidad_creada = 0
# entidades = []

# # Crear Entidades
# for i in range(100000):
#     entidades.append(get_entidad(i))
#     cantidad_creada += 1
#     if cantidad_creada ==  INSERT_AT:
#         consulta = 'INSERT INTO entidades (id, cuit, razon_social) VALUES '
#         for entidad in entidades:
#             consulta += '({}, "{}", "{}"),'.format(entidad["id"], entidad["cuit"], entidad["razon_social"])
#         consulta = consulta[:-1] + ';'
#         resultad = db.insertar_db(consulta)
#         if not resultad:
#             break
#         cantidad_creada = 0
#         entidades = []

# sedes = []
# sedes_creadas = 0
# entidades_ids = get_ids_entidades()

# for i in range(1000000):
#     sedes.append(get_sede(i, get_random_index(entidades_ids)))
#     sedes_creadas += 1
#     if sedes_creadas == INSERT_AT:
#         consulta = "INSERT INTO sedes (id, nombre, numero, sector, tipo, latitud, longitud, superficie, cantidad_pisos, cantidad_personas_externas, cantidad_personas_estables, provincia_id, entidad_id) VALUES "
#         for sede in sedes:
#             consulta += (
#                 '({}, "{}", {}, "{}", "{}", {}, {}, {}, {}, {}, {}, {}, {}),'.format(
#                     sede["id"],
#                     sede["nombre"],
#                     sede["numero"],
#                     sede["sector"],
#                     sede["tipo"],
#                     sede["latitud"],
#                     sede["longitud"],
#                     sede["superficie"],
#                     sede["cantidad_pisos"],
#                     sede["cantidad_personas_externas"],
#                     sede["cantidad_personas_estables"],
#                     sede["provincia_id"],
#                     sede["entidad_id"],
#                 )
#             )
#         consulta = consulta[:-1] + ";"
#         resultad = db.insertar_db(consulta)
#         if not resultad:
#             break
#         sedes_creadas = 0
#         sedes = []

# Crear Espacio
# espacios = []
# espacios_creados = 0
# id_sede_start = 5020
# while id_sede_start < 1000020:
#     espacios.append(get_espacio(espacios_creados, id_sede_start))
#     espacios_creados += 1
#     id_sede_start += 1
#     if espacios_creados == INSERT_AT:
#         consulta = "INSERT INTO espacios_obligados (id, nombre, aprobado, estado, estado_auxiliar, sede_id, cardio_asistido_desde, cardio_asistido_vence, cardio_asistido_vencido, ddjj_personal_capacitado, ddjj_senaletica_adecuada, ddjj_cantidad_deas) VALUES "
#         for espacio in espacios:
#             consulta += (
#                 '({}, "{}", {}, "{}", "{}", {}, "{}", "{}", {}, {}, {}, {}),'.format(
#                     espacio["id"],
#                     espacio["nombre"],
#                     espacio["aprobado"],
#                     espacio["estado"],
#                     espacio["estado_auxiliar"],
#                     espacio["sede_id"],
#                     espacio["cardio_asistido_desde"],
#                     espacio["cardio_asistido_vence"],
#                     espacio["cardio_asistido_vencido"],
#                     espacio["ddjj_personal_capacitado"],
#                     espacio["ddjj_senaletica_adecuada"],
#                     espacio["ddjj_cantidad_deas"],
#                 )
#             )
#         consulta = consulta[:-1] + ";"
#         resultad = db.insertar_db(consulta)
#         if not resultad:
#             break
#         espacios = []
# if espacios:
#     consulta = "INSERT INTO espacios_obligados (id, nombre, aprobado, estado, estado_auxiliar, sede_id, cardio_asistido_desde, cardio_asistido_vence, cardio_asistido_vencido, ddjj_personal_capacitado, ddjj_senaletica_adecuada, ddjj_cantidad_deas) VALUES "
#     for espacio in espacios:
#         consulta += (
#             '({}, "{}", {}, "{}", "{}", {}, "{}", "{}", {}, {}, {}, {}),'.format(
#                 espacio["id"],
#                 espacio["nombre"],
#                 espacio["aprobado"],
#                 espacio["estado"],
#                 espacio["estado_auxiliar"],
#                 espacio["sede_id"],
#                 espacio["cardio_asistido_desde"],
#                 espacio["cardio_asistido_vence"],
#                 espacio["cardio_asistido_vencido"],
#                 espacio["ddjj_personal_capacitado"],
#                 espacio["ddjj_senaletica_adecuada"],
#                 espacio["ddjj_cantidad_deas"],
#             )
#         )
#     consulta = consulta[:-1] + ";"
#     resultad = db.insertar_db(consulta)
#     espacios_creados = 0
#     espacios = []

# Agregar user y espacio_user


# def get_representante(id):
#     _id = id + 1200000
#     return {
#         "id": _id,
#         "email": f"{id_generator(256)}@mail.com",
#         "hashed_password": id_generator(26),
#         "fecha_nacimiento": generar_fecha_aleatoria("1949-01-01", "2005-01-01"),
#         "rol": "representante",
#     }

# def get_espacio_user(id):
#     _id = id + 10
#     valida = get_random_index([True, False, True, True, False, True, True, True, True ])
#     pendiente = get_random_index([True, False, True, True ]) if not valida else False
#     return {
#         "espacio_id": get_random_from_range(5020, 100000),
#         "user_id": id,
#         "valida": valida,
#         "pendiente": pendiente,
#         "fecha_creacion": generar_fecha_aleatoria("2023-01-01", "2023-12-20"),
#     }

# representantes = []
# representantes_creados = 0
# espacios_user = []
# espacios_user_creados = 0

# for i in range(250000):
#     representantes.append(get_representante(i))
#     representantes_creados += 1
#     espacios_user.append(get_espacio_user(i))
#     if representantes_creados == INSERT_AT:
#         consulta = (
#             "INSERT INTO users (id, fecha_nacimiento, rol, email, hashed_password) VALUES "
#         )
#         for representante in representantes:
#             consulta += '({}, "{}", "{}", "{}", "{}"),'.format(
#                 representante["id"],
#                 representante["fecha_nacimiento"],
#                 representante["rol"],
#                 representante["email"],
#                 representante["hashed_password"],
#             )
#         consulta = consulta[:-1] + ";"
#         resultad = db.insertar_db(consulta)
#         if not resultad:
#             break
#         consulta = (
#             "INSERT INTO espacio_user (espacio_id, user_id, valida, pendiente, fecha_creacion) VALUES "
#         )
#         for espacio_user in espacios_user:
#             consulta += '({}, {}, {}, {}, "{}"),'.format(
#                 espacio_user["espacio_id"],
#                 espacio_user["user_id"],
#                 espacio_user["valida"],
#                 espacio_user["pendiente"],
#                 espacio_user["fecha_creacion"],
#             )
#         consulta = consulta[:-1] + ";"
#         resultad = db.insertar_db(consulta)
#         if not resultad:
#             break
#         espacios_user = []
#         representantes_creados = 0
#         representantes = []

# if representantes_creados:
#     consulta = (
#         "INSERT INTO users (id, rol, fecha_nacimiento, email, hashed_password) VALUES "
#     )
#     for representante in representantes:
#         consulta += '({}, "{}", "{}", "{}", "{}"),'.format(
#             representante["id"],
#             representante["rol"],
#             representante["fecha_nacimiento"],
#             representante["email"],
#             representante["hashed_password"],
#         )
#     consulta = consulta[:-1] + ";"
#     resultad = db.insertar_db(consulta)
#     consulta = (
#         "INSERT INTO espacio_user (espacio_id, user_id, valida, pendiente, fecha_creacion) VALUES "
#     )
#     for espacio_user in espacios_user:
#         consulta += '({}, {}, {}, {}, "{}"),'.format(
#             espacio_user["espacio_id"],
#             espacio_user["user_id"],
#             espacio_user["valida"],
#             espacio_user["pendiente"],
#             espacio_user["fecha_creacion"],
#         )
#     consulta = consulta[:-1] + ";"
#     resultad = db.insertar_db(consulta)
#     espacios_user = []
#     representantes_creados = 0
#     representantes = []


# def get_muerte_subita(id):
#     _id = id + 5
#     user_id = id + 10
#     rcp = get_random_index([True, False, True, True, False, True, True, True, True])
#     tiempo_rcp = get_random_from_range(0, 30) if rcp else 0
#     return {
#         "id": _id,
#         "fecha": generar_fecha_aleatoria("2023-01-01", "2023-12-20"),
#         "sexo": get_random_index(
#             [
#                 "Masculino",
#                 "Femenino",
#                 "X",
#                 "Masculino",
#                 "Femenino",
#                 "Masculino",
#                 "Femenino",
#             ]
#         ),
#         "edad": get_random_from_range(1, 96),
#         "fallecio": get_random_index(
#             [True, False, False, True, False, False, True, False, True]
#         ),
#         "espacio_obligado_id": get_random_from_range(10, 1000020),
#         "rcp": rcp,
#         "tiempo_rcp": tiempo_rcp,
#         "user_id": user_id,
#     }


# def get_incovenientes(id, fecha):
#     _id = id + 5
#     respondio_con_descargas_electricas = get_random_index(
#         [True, False, False, True, False, False, True, False, True]
#     )
#     cantidad_de_descargas = (
#         get_random_from_range(0, 30) if respondio_con_descargas_electricas else 0
#     )

#     return {
#         "id": _id,
#         "fecha": fecha,
#         "falta_insumos": get_random_index(
#             [True, False, False, True, False, False, True, False, True]
#         ),
#         "estaba_en_sitio": get_random_index(
#             [True, False, False, True, False, False, True, False, True]
#         ),
#         "respondio_con_descargas_electricas": respondio_con_descargas_electricas,
#         "cantidad_de_descargas": cantidad_de_descargas,
#         "muerte_subita_id": _id,
#     }


# # Agregar muerte súbita e incovenientes
# muertesubita = []
# muertesubita_creados = 0
# incovenientes = []
# incovenientes_creados = 0


# for i in range(450000):
#     muerte_ = get_muerte_subita(i)
#     muertesubita.append(muerte_)
#     muertesubita_creados += 1
#     tiene_incovenientes = get_random_index(
#         [True, False, False, True, False, False, True, False, True]
#     )
#     if tiene_incovenientes:
#         incovenientes.append(get_incovenientes(i, muerte_["fecha"]))
#         incovenientes_creados += 1
#     if muertesubita_creados == INSERT_AT:
#         consulta = "INSERT INTO muertes_subitas (id, fecha, sexo, edad, fallecio, espacio_obligado_id, rcp, tiempo_rcp, user_id) VALUES "
#         for muerte in muertesubita:
#             consulta += '({}, "{}", "{}", {}, {}, {}, {}, {}, {}),'.format(
#                 muerte["id"],
#                 muerte["fecha"],
#                 muerte["sexo"],
#                 muerte["edad"],
#                 muerte["fallecio"],
#                 muerte["espacio_obligado_id"],
#                 muerte["rcp"],
#                 muerte["tiempo_rcp"],
#                 muerte["user_id"],
#             )
#         consulta = consulta[:-1] + ";"
#         resultad = db.insertar_db(consulta)
#         if not resultad:
#             break
#         if incovenientes:
#             consulta = "INSERT INTO incovenientes (id, fecha, falta_insumos, estaba_en_sitio, respondio_con_descargas_electricas, cantidad_de_descargas, muerte_subita_id) VALUES "
#             for inconveniente in incovenientes:
#                 consulta += '({}, "{}", {}, {}, {}, {}, {}),'.format(
#                     inconveniente["id"],
#                     inconveniente["fecha"],
#                     inconveniente["falta_insumos"],
#                     inconveniente["estaba_en_sitio"],
#                     inconveniente["respondio_con_descargas_electricas"],
#                     inconveniente["cantidad_de_descargas"],
#                     inconveniente["muerte_subita_id"],
#                 )
#             consulta = consulta[:-1] + ";"
#             resultad = db.insertar_db(consulta)
#             if not resultad:
#                 break
#         muertesubita = []
#         muertesubita_creados = 0
#         incovenientes = []
#         incovenientes_creados = 0
# if muertesubita:
#     consulta = "INSERT INTO muertes_subitas (id, fecha, sexo, edad, fallecio, espacio_obligado_id, rcp, tiempo_rcp, user_id) VALUES "
#     for muerte in muertesubita:
#         consulta += '({}, "{}", "{}", {}, {}, {}, {}, {}, {}),'.format(
#             muerte["id"],
#             muerte["fecha"],
#             muerte["sexo"],
#             muerte["edad"],
#             muerte["fallecio"],
#             muerte["espacio_obligado_id"],
#             muerte["rcp"],
#             muerte["tiempo_rcp"],
#             muerte["user_id"],
#         )
#     consulta = consulta[:-1] + ";"
#     resultad = db.insertar_db(consulta)
#     if incovenientes:
#         consulta = "INSERT INTO incovenientes (id, fecha, falta_insumos, estaba_en_sitio, respondio_con_descargas_electricas, cantidad_de_descargas, muerte_subita_id) VALUES "
#         for inconveniente in incovenientes:
#             consulta += '({}, "{}", {}, {}, {}, {}, {}),'.format(
#                 inconveniente["id"],
#                 inconveniente["fecha"],
#                 inconveniente["falta_insumos"],
#                 inconveniente["estaba_en_sitio"],
#                 inconveniente["respondio_con_descargas_electricas"],
#                 inconveniente["cantidad_de_descargas"],
#                 inconveniente["muerte_subita_id"],
#             )
#         consulta = consulta[:-1] + ";"
#         resultad = db.insertar_db(consulta)
#     muertesubita = []
#     muertesubita_creados = 0
#     incovenientes = []
#     incovenientes_creados = 0


# def get_users_without_espacio():
#     consulta = (
#         """select users.id
#         from users
#         where users.id not in (
#         select espacio_user.user_id  from espacio_user
#         );"""
#     )
#     resultados = db.consultar_db(consulta)
#     return [resultado[0] for resultado in resultados]


# users_sin_espacio = get_users_without_espacio()
# for user_id in users_sin_espacio:
#     valida = get_random_index([True, False, True, True, False, True, True, True, True ])
#     fecha_aleatoria = generar_fecha_aleatoria("2023-01-01", "2023-12-20")
#     pendiente = get_random_index([True, False, True, True ]) if not valida else False
#     consulta = (f"INSERT INTO espacio_user (espacio_id, user_id, valida, pendiente, fecha_creacion) VALUES "
#                 f"({get_random_from_range(900000, 1000000)}, {user_id}, {valida}, "
#                 f"{pendiente}, '{fecha_aleatoria}');")
#     resultad = db.insertar_db(consulta)
#     if not resultad:
#         break

# def get_sedes_ids():
#     consulta = "SELECT id, provincia_id  FROM sedes;"
#     resultados = db.consultar_db(consulta)
#     return resultados


# sedes_ids = get_sedes_ids()
# sedes_listas = []
# for sede_id in sedes_ids:
#     localidad = get_random_index(
#         provincias_localidades_en_db[str(sede_id[1])]
#     )
#     base_sql = f"UPDATE sedes SET localidad_id = {localidad} WHERE id = {sede_id[0]};"
#     db.insertar_db(base_sql)
