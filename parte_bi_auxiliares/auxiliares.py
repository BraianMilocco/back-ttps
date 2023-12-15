""""
Archivo con funciones auxiliares para la generación de datos de prueba aleatorios.
"""

import random
import string
import random
from datetime import datetime, timedelta

deas_solidarios = {
    "Federal/Nacional": [0, 10, 50, 30, 18, 81],
    "Estatal/Provincial": [0, 10, 11, 25, 18, 41],
    "Municipal/Local": [0, 10, 11, 25, 18, 41],
    "Salud": [0, 10, 11, 25, 18, 41],
    "Educación": [0, 10, 50, 30, 18, 81],
    "Seguridad": [0, 10, 50, 30, 18, 81],
    "Infraestructura": [37, 71, 27, 36, 90, 44, 89],
    "Ministerios": [37, 71, 27, 36, 90, 44, 89],
    "Agencias gubernamentales": [37, 71, 27, 36, 90, 44, 89],
    "Corporaciones estatales": [37, 71, 27, 36, 90, 44, 89],
    "Tecnología": [37, 71, 27, 36, 90, 44, 89],
    "Finanzas": [37, 71, 27, 36, 90, 44, 89],
    "Manufactura": [37, 71, 27, 36, 90, 44, 89],
    "Servicios": [0, 10, 50, 30, 18, 81],
    "Pequeña y Mediana Empresa": [55, 77, 23, 30, 78, 87, 95, 92, 74],
    "Multinacional": [55, 77, 23, 30, 78, 87, 95, 92, 74],
    "Startup": [55, 77, 23, 30, 78, 87, 95, 92, 74],
    "Comercial": [55, 77, 23, 30, 78, 87, 95, 92, 74],
    "No lucrativa": [55, 77, 23, 30, 78, 87, 95, 92, 74],
    "Consultoría": [0, 10, 50, 30, 18, 26, 11],
    "Producción": [0, 10, 50, 30, 18, 26, 11],
}


def latitudes():
    return random.uniform(-90, 90)


def longitudes():
    return random.uniform(-180, 180)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def get_random_index(some_list):
    return random.choice(some_list)


def get_random_from_range(minimo, maximo):
    return random.randint(minimo, maximo)


def generar_fecha_aleatoria(fecha_min, fecha_max):
    """
    Genera una fecha y hora aleatoria dentro del rango proporcionado, incluyendo milisegundos.

    :param fecha_min: La fecha mínima en formato 'YYYY-MM-DD'.
    :param fecha_max: La fecha máxima en formato 'YYYY-MM-DD'.
    :return: Un objeto datetime con fecha y hora aleatoria.
    """
    # Convertir las fechas de entrada a objetos datetime
    fecha_min = datetime.strptime(fecha_min, "%Y-%m-%d")
    fecha_max = datetime.strptime(fecha_max, "%Y-%m-%d")

    # Calcular la diferencia en días entre las fechas
    diferencia_dias = (fecha_max - fecha_min).days

    # Generar un número aleatorio de días para sumar a la fecha mínima
    dias_aleatorios = random.randrange(diferencia_dias + 1)
    fecha_aleatoria = fecha_min + timedelta(days=dias_aleatorios)

    # Añadir hora, minutos, segundos y milisegundos aleatorios
    horas = random.randint(0, 23)
    minutos = random.randint(0, 59)
    segundos = random.randint(0, 59)
    milisegundos = random.randint(0, 999999)

    # Ajustar la fecha aleatoria con la hora aleatoria
    fecha_aleatoria = fecha_aleatoria.replace(
        hour=horas, minute=minutos, second=segundos, microsecond=milisegundos
    )

    return fecha_aleatoria


def fechas_estado_vencido(estado):
    desde = None
    hasta = None
    if estado == "Cardio-Asistido Certificado":
        desde = generar_fecha_aleatoria("2020-01-01", "2023-8-29")
        hasta = generar_fecha_aleatoria("2023-12-24", "2024-5-29")
    elif estado == "Cardio-Asistido Certificado Vencido":
        desde = generar_fecha_aleatoria("2018-01-01", "2019-8-29")
        hasta = generar_fecha_aleatoria(desde.strftime("%Y-%m-%d"), "2019-11-29")

    return desde, hasta


estados = [
    "En proceso de ser Cardio-Asistido",
    "Cardio-Asistido con DDJJ",
    "Cardio-Asistido Certificado",
    "Cardio-Asistido Certificado Vencido",
]
sectores = ["publico", "privado"]
tipos = {
    "publico": [
        "Federal/Nacional",
        "Estatal/Provincial",
        "Municipal/Local",
        "Salud",
        "Educación",
        "Seguridad",
        "Infraestructura",
        "Ministerios",
        "Agencias gubernamentales",
        "Corporaciones estatales",
    ],
    "privado": [
        "Tecnología",
        "Finanzas",
        "Manufactura",
        "Servicios",
        "Pequeña y Mediana Empresa",
        "Multinacional",
        "Startup",
        "Comercial",
        "No lucrativa",
        "Consultoría",
        "Producción",
    ],
}
