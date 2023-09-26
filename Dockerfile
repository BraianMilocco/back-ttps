# Usa una imagen base de Python adecuada
FROM python:3.10.12

# Establece la variable de entorno para que Python no escriba archivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requisitos a la imagen
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido de la carpeta actual al directorio de trabajo en el contenedor
COPY . .

# Expone el puerto en el que se ejecuta la aplicación FastAPI
EXPOSE 8080

# Comando para iniciar la aplicación'
CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]