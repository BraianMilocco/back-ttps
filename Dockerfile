# Usa una imagen base de Python adecuada
FROM python:3.10.12

# Establece la variable de entorno para que Python no escriba archivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala las dependencias
RUN pip install --upgrade pip \
    && pip install fastapi uvicorn

# Copia el código de la aplicación al contenedor
COPY . . 

# Establece el directorio de trabajo
WORKDIR /app

# Inicia la aplicación con uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# Comando para iniciar la aplicación'
# CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]