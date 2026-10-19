import os
import requests
from dotenv import load_dotenv

load_dotenv()

def armar_peticion(pregunta):
    if not isinstance(pregunta, str) or not pregunta.strip():
        raise ValueError("Escribe una pregunta antes de continuar.")
    api_key = os.getenv("API_KEY")
    modelo = os.getenv("MODEL_NAME")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"
    body = {
        "contents": [
            {"parts": [{"text": pregunta}]}
        ]
    }
    headers = {"x-goog-api-key": api_key}
    return url, headers, body

def enviar_peticion(url, headers, body):
    try:
        respuesta = requests.post(url, headers=headers, json=body, timeout=90)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as error:
        raise RuntimeError("Gemini no respondió. Inténtalo de nuevo en un momento.") from error
    try:
        respuesta.raise_for_status()
    except requests.exceptions.HTTPError as error:
        if respuesta.status_code == 503:
            raise RuntimeError(
                "Gemini está ocupado ahora. Inténtalo de nuevo en un momento."
            ) from error
        if respuesta.status_code in (400, 401, 403):
            raise RuntimeError(
                "Gemini rechazó la petición. Revisa la clave o los datos enviados."
            ) from error
        raise RuntimeError(
            f"Gemini devolvió un error HTTP {respuesta.status_code}."
        ) from error
    try:
        return respuesta.json()
    except requests.exceptions.JSONDecodeError as error:
        raise RuntimeError("Gemini respondió, pero no pude leer su respuesta.") from error

def extraer_texto(datos):
    try:
        return datos["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError) as error:
        raise RuntimeError(
            "Gemini respondió, pero no encontré el texto esperado."
        ) from error

def obtener_dato_de_prueba(pregunta):
    url, headers, body = armar_peticion(pregunta)
    datos = enviar_peticion(url, headers, body)
    return extraer_texto(datos)
try:
    print(obtener_dato_de_prueba("¿que lleva un completo en chile?, en 15 palabras."))
except (ValueError, RuntimeError) as error:
    print("No pude obtener la respuesta:", error)
