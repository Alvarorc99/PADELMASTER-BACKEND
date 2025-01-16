"Archivo de ejemplo para usar el índice FAISS (funciona correctamente)"

import json
import sys
from venv import logger
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import re
from langchain.prompts import PromptTemplate
from langchain_aws import ChatBedrock
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.config.config import *


def procesar_consulta(consulta):
    # Crear el modelo de lenguaje
    llm = ChatBedrock(model_id=LLM_MODEL_NAME, client=client)

    # Plantilla de prompt para extraer el nombre de la pala y el atributo
    prompt = """
    Dada la siguiente consulta: "{consulta}", 
    por favor, extrae el nombre de la pala y el atributo que se está preguntando. 
    El atributo puede ser cosas como: 'Precio', 'Superfície', 'Balance', 'Marca', 'Color', 'Núcleo', 'Cara', 'Formato', 'Dureza', 'Acabado', 'Forma', 'Jugador', 'Tipo de juego, 'Nivel de Juego', 'Colección Jugadores', 'Imagen', 'Enlace' y 'Descripción'.
    Devuelve un JSON con las claves 'nombre_pala' y 'atributo'.
    """

    formatted_prompt = prompt.format(consulta=consulta)
    
    # Obtener la respuesta del modelo
    response = llm.invoke(formatted_prompt)
    
    # Parsear la respuesta para obtener el nombre de la pala y el atributo
    try:
        resultado = response.content
        # Aquí deberías procesar el contenido devuelto por el modelo para extraer los datos en formato JSON
        datos = json.loads(resultado)
        nombre_pala = datos.get("nombre_pala")
        atributo = datos.get("atributo")
    except Exception as e:
        logger.error(f"Error al procesar la respuesta del modelo: {e}")
        return {"error": "No se pudo procesar la respuesta del modelo"}
    
    return nombre_pala, atributo

# Función para consultar el índice FAISS
def consultar_faiss(ruta_indice, nombre_pala, atributo):
    # Inicializar el modelo de embeddings
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    # Cargar el índice FAISS
    vector_store = FAISS.load_local(ruta_indice, embedding_model, allow_dangerous_deserialization=True)

    # Realizar la búsqueda por similitud con el nombre de la pala
    results = vector_store.similarity_search(nombre_pala, k=1)
    
    if results:
        pala = results[0].metadata  # La pala más relevante
        valor_atributo = pala.get(atributo)  # Obtener el valor del atributo
        
        if valor_atributo:
            return valor_atributo
        else:
            return f"No se encontró el atributo '{atributo}' para la pala {nombre_pala}."
    else:
        return f"No se encontró la pala {nombre_pala}."

# Función para reformular la respuesta en lenguaje natural
def reformular_respuesta(respuesta_faiss, nombre_pala, atributo):
    # Crear el modelo de lenguaje para reformular la respuesta
    llm = ChatBedrock(model_id=LLM_MODEL_NAME, client=client)
    
    prompt_reformulado = f"""
    El usuario preguntó por el atributo '{atributo}' de la pala '{nombre_pala}'. 
    El valor encontrado fue: {respuesta_faiss}. 
    Por favor, responde en lenguaje natural a esta consulta, de manera que el usuario lo entienda fácilmente.
    """

    response = llm.invoke(prompt_reformulado)
    return response.content

# Ejemplo de uso
consulta = "Que acabado tiene la SIUX GENESIS POWER 12K"
nombre_pala, atributo = procesar_consulta(consulta)
if nombre_pala and atributo:
    resultado_faiss = consultar_faiss("C:/Users/alvar/TFG/PADELMASTER BACKEND/faiss/faiss_index", nombre_pala, atributo)
    
    # Reformular la respuesta obtenida de FAISS en lenguaje natural
    respuesta_final = reformular_respuesta(resultado_faiss, nombre_pala, atributo)
    
    print(respuesta_final)