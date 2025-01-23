"Archivo para usar el índice FAISS (funciona medianamente correcto)"

import json
import sys
from venv import logger
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import re
from langchain_aws import ChatBedrock
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.prompt import procesar_consulta_prompt
from src.config.config import *

import json
import logging
import re

import json
import logging
import re

def procesar_consulta(consulta):
    try:
        llm = ChatBedrock(model_id=LLM_CLAUDE_3_HAIKU, client=claude_3_haiku_client)
        formatted_prompt = procesar_consulta_prompt.format(consulta=consulta)

        response = llm.invoke(formatted_prompt)
        
        if not response or not response.content:
            raise ValueError("La respuesta del modelo está vacía o no se recibió contenido.")
        
        resultado = response.content
        resultado = resultado.replace("```json", "").replace("```", "").replace("`", "").strip()
        print(f"Resultado bruto del modelo: '{resultado}'")
    
        datos = json.loads(resultado)
        nombre_pala = datos.get("nombre_pala").strip().lower()
        atributo = datos.get("atributo")
        print(f"Nombre pala: {nombre_pala}, Atributo: {atributo}")
        
        return nombre_pala, atributo
    except Exception as e:
        logging.error(f"Error inesperado al procesar la consulta: {str(e)}")
        return None, None

# Función para consultar el índice FAISS
def consultar_faiss(ruta_indice, nombre_pala, atributo):
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    vector_store = FAISS.load_local(ruta_indice, embedding_model, allow_dangerous_deserialization=True)

    # Realizar la búsqueda por similitud con el nombre de la pala
    results = vector_store.similarity_search(nombre_pala, k=10)
    # print("Resultado de la consulta FAISS:", )
    # for result in results:
    #     print(result.metadata)
    
    if results:
        palas_similares = [
            {
                "nombre": result.metadata.get('Nombre', 'Desconocido'),
                "imagen_url": result.metadata.get('Imagen', 'URL_DE_IMAGEN_POR_DEFECTO'),
            }
            for result in results
        ]  
        
        # Asegúrate de usar el nombre correcto
        print("Palas similares encontradas:", [p["nombre"] for p in palas_similares])

        for result in results:
            if result.metadata.get('Nombre', '').strip().lower() == nombre_pala:
                valor_atributo = result.metadata.get(atributo)
                imagen_url = result.metadata.get('Imagen', 'URL_DE_IMAGEN_POR_DEFECTO')
                return {"exacto": {"atributo": valor_atributo, "imagen": imagen_url}, "similares": []}
            
        return {"exacto": None, "similares": palas_similares}
            
    return {"exacto": None, "similares": []}

# Función para reformular la respuesta en lenguaje natural
def reformular_respuesta(respuesta_faiss, nombre_pala, atributo):
    # Crear el modelo de lenguaje para reformular la respuesta
    llm_haiku = ChatBedrock(model_id=LLM_CLAUDE_3_HAIKU, client=claude_3_haiku_client)
    
    prompt_reformulado = f"""
    El usuario ha preguntado sobre el atributo '{atributo}' de la pala '{nombre_pala}'.
    El valor encontrado es: {respuesta_faiss}.
    Por favor, responde de manera clara, amigable y educada a la consulta del usuario.

    Si se trata de un precio, menciona el valor numérico y la moneda.
    No incluyas enlaces externos ni sugieras otras fuentes.
    
    Por favor, reformula la respuesta de forma adecuada: 
    """

    response = llm_haiku.invoke(prompt_reformulado)

    if response and response.content:
        return response.content.strip()

    else:
        logger.error( "Lo siento, no pude procesar tu consulta correctamente.")
        return None, None
    
def reformular_respuesta_sin_resultados(palas_similares, nombre_pala, atributo):
    # Crear el modelo de lenguaje para reformular la respuesta
    llm_haiku = ChatBedrock(model_id=LLM_CLAUDE_3_HAIKU, client=claude_3_haiku_client)
    
    prompt_sin_respuesta = f"""
    No se ha encontrado ninguna pala con el nombre exacto '{nombre_pala}' en nuestra base de datos.
    Las palas más similares encontradas son: {', '.join(palas_similares)}.
    Indícale al usuario que la pala por la que ha preguntado no existe, pero puede hacer preguntas sobre estas palas (en formato lista): {', '.join(palas_similares)}.
    Por favor, responde de manera clara y amigable.
    """

    response = llm_haiku.invoke(prompt_sin_respuesta)

    if response and response.content:
        return response.content.strip()
    else:
        logger.error( "Lo siento, no pude procesar tu consulta correctamente.")
        return None, None