import jwt
import requests
from datetime import datetime, timedelta
from settings import settings


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expiration_minutes
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def get_data_from_token(payload: dict):
    return {
        "email": payload.get("sub"),
        "rol": payload.get("rol"),
        "provincia": payload.get("provincia"),
        "provincia_id": payload.get("provincia_id"),
        "id": payload.get("id"),
    }


def get_dea_marcas():
    headers = {
        "Content-Type": "application/json",
    }
    url = "https://api.claudioraverta.com/deas/"
    data = None
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
    else:
        print(response.status_code)
    return data


def get_dea_modelos(marca):
    headers = {
        "Content-Type": "application/json",
    }
    marcas = get_dea_marcas()
    id_dea = None
    for dea in marcas:
        if marca == dea["marca"]:
            id_dea = dea["id"]
            break
    if not id_dea:
        return None
    url = f"https://api.claudioraverta.com/deas/{id_dea}/modelos/"
    data = None
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
    else:
        print(response.status_code)
    return data
