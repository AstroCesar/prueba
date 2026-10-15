import os
import requests
from dotenv import load_dotenv

load_dotenv()

def obtener_dato_de_prueba(pregunta):
    api_key = os.getenv("API_KEY")
    modelo = os.getenv("MODEL_NAME")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"
    body = {
        "contents": [
            {"parts": [{"text": pregunta}]}
        ]
    }
    headers = {"x-goog-api-key": api_key}
    respuesta = requests.post(url, headers=headers, json=body)
    datos = respuesta.json()
    return datos["candidates"][0]["content"]["parts"][0]["text"]


print(obtener_dato_de_prueba("¿que lleva un completo en chile?, en 15 palabras."))