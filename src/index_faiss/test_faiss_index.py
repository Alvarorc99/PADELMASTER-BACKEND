"""Example file to use the FAISS index"""

import json
import sys
from venv import logger
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain_aws import ChatBedrock
from src.config.config import *
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


def procesar_consulta(consulta):
    # Crear el modelo de lenguaje
    llm = ChatBedrock(model_id=LLM_CLAUDE_3_HAIKU, client=claude_3_haiku_client)

    # Plantilla de prompt para extraer el nombre de la pala y el atributo
    prompt = """
    Dada la siguiente consulta: "{consulta}", 
    por favor, extrae el nombre de la pala y el atributo que se está preguntando. 
    El atributo puede ser cosas como: 'Precio', 'Superficie', 'Balance', 'Marca', 'Color', 'Núcleo', 'Cara', 'Dureza', 'Acabado', 'Forma', 'Jugador', 'Tipo de juego, 'Nivel de juego', 'Jugador profesional', 'Imagen', 'Enlace' y 'Descripción'.
    Devuelve un JSON con las claves 'nombre_pala' y 'atributo'.
    """

    formatted_prompt = prompt.format(consulta=consulta)
    
    response = llm.invoke(formatted_prompt)
    
    # Parsear la respuesta para obtener el nombre de la pala y el atributo
    try:
        resultado = response.content
        datos = json.loads(resultado)
        nombre_pala = datos.get("nombre_pala")
        atributo = datos.get("atributo")
    except Exception as e:
        logger.error(f"Error al procesar la respuesta del modelo: {e}")
        return {"error": "No se pudo procesar la respuesta del modelo"}
    
    return nombre_pala, atributo

def consultar_faiss(ruta_indice, nombre_pala, atributo):
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    vector_store = FAISS.load_local(ruta_indice, embedding_model, allow_dangerous_deserialization=True)
    results = vector_store.similarity_search(nombre_pala, k=1)
    
    if results:
        pala = results[0].metadata 
        valor_atributo = pala.get(atributo) 
        
        if valor_atributo:
            return valor_atributo
        else:
            return f"No se encontró el atributo '{atributo}' para la pala {nombre_pala}."
    else:
        return f"No se encontró la pala {nombre_pala}."

def reformular_respuesta(respuesta_faiss, nombre_pala, atributo):
    llm = ChatBedrock(model_id=LLM_CLAUDE_3_HAIKU, client=claude_3_haiku_client)
    
    prompt_reformulado = f"""
    El usuario preguntó por el atributo '{atributo}' de la pala '{nombre_pala}'. 
    El valor encontrado fue: {respuesta_faiss}. 
    Por favor, responde en lenguaje natural a esta consulta, de manera que el usuario lo entienda fácilmente.
    """

    response = llm.invoke(prompt_reformulado)
    return response.content

# Ejemplo de uso
consulta = "Que precio tiene la pala BABOLAT TECHNICAL VIPER 2023?"
nombre_pala, atributo = procesar_consulta(consulta)
if nombre_pala and atributo:
    resultado_faiss = consultar_faiss(FAISS_INDEX_PATH, nombre_pala, atributo)
    respuesta_final = reformular_respuesta(resultado_faiss, nombre_pala, atributo)
    print(respuesta_final)