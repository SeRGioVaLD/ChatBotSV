import google.generativeai as genai
from dotenv import load_dotenv
import textwrap
import os

load_dotenv()

ruta_archivo = "static/contexto_elrapido.txt" 
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

contenido = ""
def leer_archivo():
    global contenido
    try:
        with open(ruta_archivo, "r") as archivo:
            contenido = archivo.read()
    except FileNotFoundError:
        contenido = "El archivo no se encontró."

leer_archivo()

def to_markdown(text):
    text = text.replace('•', '  *')
    text = text.replace('*', '')
    return textwrap.indent(text, '')

def to_plain_text(text):
    return text.strip()

model = genai.GenerativeModel(model_name="gemini-pro")

messages = [
    {
        'role': 'user',
        'parts': [contenido]
    }
]

messages.append({
        'role': 'model',
        'parts': [""]
    }
)

def enviarChat(mensaje):
    
    print("PREGUNTA: ", mensaje)
    
    messages.append({
        'role': 'user',
        'parts': [mensaje]
    })

    response = model.generate_content(messages)
    
    modelo_respuesta = to_markdown(response.text)
    
    messages.append({
        'role': 'model',
        'parts': [modelo_respuesta]
    })

    return modelo_respuesta

chat = enviarChat("quienes son los choferes?")

print(chat)

chat = enviarChat("cuales son los precios?")

print(chat)