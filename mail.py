# from fastapi import BackgroundTasks
from typing import List
from pydantic import EmailStr, BaseModel

# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jinja2 import Environment, FileSystemLoader
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from settings import settings


class EmailSchema(BaseModel):
    email: list[EmailStr]
    body: str
    subject: str


# conf = ConnectionConfig(
#     MAIL_USERNAME="braian.uv@hotmail.com",
#     MAIL_PASSWORD="Ttpspass2023!",
#     MAIL_FROM="braian.uv@hotmail.com",
#     MAIL_PORT=587,
#     MAIL_SERVER="smtp.office365.com",
#     # MAIL_STARTTLS=True,  # Use STARTTLS
#     # MAIL_SSL_TLS=False,  # Do not use SSL/TLS
# )


async def send_email(to: List[str], body: str):
    sender_email = settings.mail_email
    sender_password = settings.mail_pass
    smtp_server = settings.mail_server
    smtp_port = settings.mail_port
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(to)
    message["Subject"] = "Pedido DEA"

    # Agregar el cuerpo HTML al correo
    message.attach(MIMEText(body, "html"))

    for attempt in range(1, 4):  # Intenta hasta 3 veces
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                # server.ehlo()  # Identificarse con el servidor SMTP cuando se usa TLS
                server.starttls()
                # server.ehlo()  # Identificarse nuevamente después de iniciar TLS
                server.login(sender_email, sender_password)
                server.send_message(message)
            print("Correo enviado con éxito")
            # break  # Salir del bucle si el correo se envía con éxito
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


def render_email_template(lat: str, lon: str, url_aviso: str, url_maps: str):
    template = env.get_template("template.html")
    return template.render(lat=lat, lon=lon, url_aviso=url_aviso, url_maps=url_maps)
