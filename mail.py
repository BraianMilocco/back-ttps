from fastapi import BackgroundTasks
from typing import List
from pydantic import EmailStr, BaseModel
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jinja2 import Environment, FileSystemLoader
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time


class EmailSchema(BaseModel):
    email: list[EmailStr]
    body: str
    subject: str


conf = ConnectionConfig(
    MAIL_USERNAME="ttps_grupo6_2023@yahoo.com",
    MAIL_PASSWORD="Pass!Grupo!6!",
    MAIL_FROM="ttps_grupo6_2023@yahoo.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.mail.yahoo.com",
    MAIL_STARTTLS=True,  # Use STARTTLS
    MAIL_SSL_TLS=False,  # Do not use SSL/TLS
)


async def send_email(to: List[str], body: str):
    sender_email = "ttps_grupo6_2023@yahoo.com"
    sender_password = "Pass!Grupo!6!"  # Asegúrate de que esta es la contraseña correcta o contraseña de aplicación si usas 2FA.

    # Configuración del servidor SMTP de Yahoo
    smtp_server = "smtp.mail.yahoo.com"
    smtp_port = 587  # Usar 465 para SSL

    # Crear el objeto MIMEMultipart y configurar los encabezados
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(to)
    message["Subject"] = "Pedido DEA"

    # Agregar el cuerpo HTML al correo
    message.attach(MIMEText(body, "html"))

    for attempt in range(1, 4):  # Intenta hasta 3 veces
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.ehlo()  # Identificarse con el servidor SMTP cuando se usa TLS
                server.starttls()
                server.ehlo()  # Identificarse nuevamente después de iniciar TLS
                server.login(sender_email, sender_password)
                server.send_message(message)
            print("Correo enviado con éxito")
            break  # Salir del bucle si el correo se envía con éxito
        except smtplib.SMTPServerDisconnected as e:
            print(f"Fallo al enviar correo, intento {attempt} de 3: {e}")
            time.sleep(2 ** (attempt - 1))  # Backoff exponencial
        except smtplib.SMTPAuthenticationError as e:
            print(f"Error de autenticación: {e}")
            break  # No reintentar si hay un error de autenticación
        except Exception as e:
            print(f"Error inesperado: {e}")
            break  # Romper el ciclo para cualquier otro error inesperado


env = Environment(loader=FileSystemLoader("templates"))


def render_email_template(lat: str, lon: str):
    template = env.get_template("template.html")
    return template.render(lat=lat, lon=lon)
