"File to use the FAISS index in Personalized_query"

import json
import sys
from venv import logger
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain_aws import ChatBedrock
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.prompt import process_query_prompt
from src.config.config import *

import json
import logging

def process_query(query):
    try:
        logging.info(f"Starting the process of the query: {query}")
        llm = ChatBedrock(model_id=LLM_CLAUDE_3_HAIKU, client=claude_3_haiku_client)
        formatted_prompt = process_query_prompt.format(query=query)
        logging.info(f"Formatted prompt sent to the model: {formatted_prompt[:100]}...")

        response = llm.invoke(formatted_prompt)
        
        if not response or not response.content:
            raise ValueError("La respuesta del modelo está vacía o no se recibió contenido.")
        
        resultado = response.content
        resultado = resultado.replace("```json", "").replace("```", "").replace("`", "").strip()
        logging.info(f"Processed result: {resultado[:100]}...") 
    
        datos = json.loads(resultado)
        nombre_pala = datos.get("nombre_pala").strip().lower()
        atributos = datos.get("atributos", [])
        
        return nombre_pala, atributos
    except Exception as e:
        logging.error(f"Error inesperado al procesar la consulta: {str(e)}")
        return None, []

def consult_faiss(index_path, nombre_pala, atributos):
    logger.info(f"Consulting FAISS index with name: {nombre_pala}, attribute: {atributos}")
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    logging.info(f"Embeddings model '{EMBEDDING_MODEL_NAME}' loaded correctly.")
    vector_store = FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)
    logger.info(f"FAISS index loaded from the '{index_path}' path.")

    results = vector_store.similarity_search(nombre_pala, k=15)
    logger.info(f"Number of results found: '{len(results)}'.")

    if results:
        palas_similares = [
            {
                "nombre": result.metadata.get('Nombre', 'Desconocido'),
                "imagen_url": result.metadata.get('Imagen', 'URL_DE_IMAGEN_POR_DEFECTO'),
            }
            for result in results
        ]  
        
        logger.info(f"Similar names founded: {[p['nombre'] for p in palas_similares]}.")

        for result in results:
            if result.metadata.get('Nombre', '').strip().lower() == nombre_pala:
                valores_atributos = {
                    atributo: result.metadata.get(atributo, "Información no disponible")
                    for atributo in atributos
                }
                imagen_url = result.metadata.get('Imagen', 'URL_DE_IMAGEN_POR_DEFECTO')
                logger.info(f"Name found with exact match: '{nombre_pala}'.")
                return {"exacto": {"atributos": valores_atributos, "imagen": imagen_url}, "similares": []}
            
        return {"exacto": None, "similares": palas_similares}
    
    logger.info("No results were found in the FAISS index.")
    return {"exacto": None, "similares": []}

def reformular_respuesta(respuesta_faiss, nombre_pala, atributos, conversation):
    """
    Reformula una respuesta unificada para todos los atributos solicitados de una pala.
    """
    llm_haiku = ChatBedrock(model_id=LLM_CLAUDE_3_HAIKU, client=claude_3_haiku_client)

    atributos_filtrados = {attr: respuesta_faiss[attr] for attr in atributos if attr in respuesta_faiss}
    atributos_solicitados = ", ".join(atributos)
    atributos_texto = "\n".join(
        f"- {atributo}: {valor}" for atributo, valor in atributos_filtrados.items()
    )
    
    prompt_reformulado = f"""
    El usuario ha preguntado sobre los atributos "{atributos_solicitados}" de la pala de pádel "{nombre_pala}".
    Los valores de los atributos encontrados son: "{atributos_texto}".
    Te proporciono el historial de conversación con el usuario por si es necesario: "{conversation}".

    Si el atributo se refiere a un precio, asegúrate de mencionar el valor numérico seguido de la moneda correspondiente.
    Si es otro tipo de atributo, como el balance, la marca, el color, el núcleo, la cara, el acabado, la forma, la superficie, el sexo, la dureza, el nivel de juego, el tipo de juego o el jugador profesional, proporciona la información de forma precisa y contextualizada.
    Evita incluir enlaces externos, sugerir fuentes adicionales o agregar información irrelevante.  
    La respuesta debe centrarse exclusivamente en la información solicitada y ser lo más útil posible para el usuario.  

    Por favor, genera una respuesta clara y detallada incluyendo todos los atributos y sus valores. 
    Responde directamente al usuario de forma clara y amigable.
    """

    response = llm_haiku.invoke(prompt_reformulado)

    if response and response.content:
        logger.info(f"Answer reformulated: '{response.content.strip()}'.")
        return response.content.strip()

    else:
        logger.error( "Lo siento, no pude procesar tu consulta correctamente.")
        return None, None
    
def reformular_respuesta_sin_resultados(nombre_pala):
    """
    Reformula una respuesta para informar al usuario que no se ha encontrado ninguna pala con el nombre exacto solicitado.
    """
    logger.info(f"Reformulating the answer of '{nombre_pala}'.")
    llm_haiku = ChatBedrock(model_id=LLM_CLAUDE_3_HAIKU, client=claude_3_haiku_client)
    
    prompt_sin_respuesta = f"""
    No se ha encontrado ninguna pala con el nombre exacto '{nombre_pala}' en nuestra base de datos.
    Indícale al usuario que la pala por la que ha preguntado no existe, pero puede hacer preguntas sobre las siguientes palas (no las estas viendo, pero el usuario si que tiene acceso a ellas). No menciones nombres de palas.
    Además, termina la respuesta con un mensaje del estilo "A continuación se muestran las palas más similares encontradas".
    Por favor, responde de manera directa al usuario de forma clara y amigable.
    """

    response = llm_haiku.invoke(prompt_sin_respuesta)

    if response and response.content:
        logger.info(f"Answer reformulated: '{response.content.strip()}'.")
        return response.content.strip()
    else:
        logger.error("No content was received in the model response.")
        return None, None