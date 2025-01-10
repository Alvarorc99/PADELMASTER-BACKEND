# backend.py (FastAPI)
import json
from typing import Dict, Optional, Union
from fastapi import FastAPI, HTTPException
from langchain_aws import ChatBedrock
from pydantic import BaseModel
from src.config.config import *
from src.prompt import prompt_template, prompt_template_recommendations
from src.index_faiss import load_faiss_index
from langchain.embeddings import HuggingFaceEmbeddings


app = FastAPI()

rutaIndice = "C:/Users/alvar/TFG/chatbot_aws/faiss/faiss_index"
model_name = "sentence-transformers/all-MiniLm-L6-v2"
embedding_model = HuggingFaceEmbeddings(model_name=model_name)
vector_store = None

def cargar_indice():
    global vector_store
    if vector_store is None:
        vector_store = load_faiss_index.cargar_indice_faiss_y_consultar(rutaIndice)
    return vector_store

class UserQuery(BaseModel):
    frase_usuario: str

@app.post("/consulta")
async def ask_chatbot(query: UserQuery):
    llm = ChatBedrock(model_id=LLM_MODEL_NAME, client=client)

    consulta = query.frase_usuario

    try:
        
        # Formatear el prompt con la consulta del usuario
        prompt = prompt_template.format(user_input=consulta)
        
        # Obtener la respuesta del modelo LLM
        respuesta = llm.invoke(prompt)

        # print("Respuesta del modelo:")
        # print(respuesta)
        
        # Devolver la respuesta del modelo
        return {"Respuesta": respuesta.content}
    except Exception as e:
        return {"Error": f"Hubo un problema al procesar la consulta: {e}"}
    

class FilterModel(BaseModel):
    marca: Optional[str] = None
    jugador: Optional[str] = None
    forma: Optional[str] = None
    balance: Optional[str] = None
    dureza: Optional[str] = None
    acabado: Optional[str] = None
    superficie: Optional[str] = None
    tipo_juego: Optional[str] = None
    nivel_juego: Optional[str] = None
    coleccion_jugadores: Optional[str] = None
    precio_min: Optional[int] = None
    precio_max: Optional[int] = None

DATASET_PATH = "C:/Users/alvar/TFG/chatbot_aws/dataset_padel_nuestro/palas_padelnuestro.json"

def cargar_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def convertir_precio(precio_str: str) -> float:
    """Convierte una cadena de precio con formato europeo a float."""
    precio_limpio = precio_str.replace("€", "").replace(",", ".").strip()  # Eliminar símbolos y espacios
    return float(precio_limpio)

def formatear_recomendaciones(recomendaciones):
    """Devuelve las recomendaciones formateadas como una cadena de texto legible."""
    if not recomendaciones:
        return "No se encontraron palas de pádel que coincidan con tus criterios."
    
    mensaje = "Aquí tienes algunas recomendaciones de palas de pádel basadas en tus criterios:\n\n"
    for pala in recomendaciones:
        mensaje += f"• **Nombre**: {pala['Nombre']}\n"
        mensaje += f"  **Marca**: {pala['Marca']}\n"
        mensaje += f"  **Precio**: {pala['Precio']}\n"
        mensaje += f"  **Color**: {pala['Color']}\n"
        mensaje += f"  **Balance**: {pala['Balance']}\n"
        mensaje += f"  **Dureza**: {pala['Dureza']}\n"
        mensaje += f"  **Acabado**: {pala['Acabado']}\n"
        mensaje += f"  **Superfície**: {pala['Superfície']}\n"
        mensaje += f"  **Tipo de juego**: {pala['Tipo de juego']}\n"
        mensaje += f"  **Nivel de Juego**: {pala['Nivel de Juego']}\n"
        mensaje += f"  **Colección Jugadores**: {pala['Colección Jugadores']}\n"
        mensaje += f"  **Descripción**: {pala['Descripción']}\n"
    
    return mensaje

@app.post("/recommend")
async def apply_filters(filter_data: FilterModel):
    dataset = cargar_dataset()
    
    filtros = filter_data.model_dump()
    #print(f"Filtros aplicados: {filtros}")  #! Debug OK
    
    # Aplicar filtros sobre el dataset
    recomendaciones = []
    for pala in dataset:
        precio_float = convertir_precio(pala["Precio"])  # Convertir el precio a float
        
        # Filtros obligatorios (Jugador, Precio, Nivel de Juego)
        if filtros['precio_min'] and precio_float < filtros['precio_min']:
            continue
        if filtros['precio_max'] and precio_float > filtros['precio_max']:
            continue
        # Filtrar por "Jugador"
        if filtros['jugador']:
            jugador_filtro = filtros['jugador'].lower()
            
            # Si el filtro es "Hombre", se incluyen las palas con "Hombre" o "Hombre, Mujer"
            if jugador_filtro == "hombre" and not any(jugador in pala.get('Jugador', '').lower() for jugador in ['hombre', 'hombre, mujer']):
                continue
            # Si el filtro es "Mujer", se incluyen las palas con "Mujer" o "Hombre, Mujer"
            elif jugador_filtro == "mujer" and not any(jugador in pala.get('Jugador', '').lower() for jugador in ['mujer', 'hombre, mujer']):
                continue
        if filtros['nivel_juego'] and filtros['nivel_juego'].lower() != pala.get('Nivel de Juego', '').lower():
            continue

        # Filtros opcionales (solo si tienen valor)
        if filtros.get('marca') and filtros['marca'] and filtros['marca'].lower() not in pala['Marca'].lower():
            continue
        if filtros.get('forma') and filtros['forma'] and filtros['forma'].lower() != pala.get('Forma', '').lower():
            continue
        if filtros.get('balance') and filtros['balance'] and filtros['balance'].lower() != pala.get('Balance', '').lower():
            continue
        if filtros.get('dureza') and filtros['dureza'] and filtros['dureza'].lower() != pala.get('Dureza', '').lower():
            continue
        if filtros.get('acabado') and filtros['acabado'] and filtros['acabado'].lower() != pala.get('Acabado', '').lower():
            continue
        if filtros.get('superficie') and filtros['superficie'] and filtros['superficie'].lower() != pala.get('Superfície', '').lower():
            continue
        if filtros.get('tipo_juego') and filtros['tipo_juego'] and filtros['tipo_juego'].lower() != pala.get('Tipo de juego', '').lower():
            continue
        if filtros.get('coleccion_jugadores') and filtros['coleccion_jugadores'] and filtros['coleccion_jugadores'].lower() != pala.get('Colección Jugadores', '').lower():
            continue

        # Añadir la pala si cumple todos los filtros aplicables
        recomendaciones.append({
            "Nombre": pala["Nombre"],
            "Marca": pala["Marca"],
            "Color": pala["Color"],
            "Balance": pala["Balance"],
            "Dureza": pala["Dureza"],
            "Acabado": pala["Acabado"],
            "Superfície": pala["Superfície"],
            "Tipo de juego": pala["Tipo de juego"],
            "Nivel de Juego": pala["Nivel de Juego"],
            "Colección Jugadores": pala["Colección Jugadores"],
            "Precio": pala["Precio"],
            "Descripción": pala["Descripción"]
        })

    contexto = formatear_recomendaciones(recomendaciones)
    llm = ChatBedrock(model_id=LLM_MODEL_NAME, client=client)
    print("CONTEXTO",contexto) #! Debug OK
    
    try:
        prompt_recommendations = prompt_template_recommendations.format(user_input=contexto, filters=filtros)
        print("PROMPT RECOMMENDATIONS",prompt_recommendations)
        respuesta = llm.invoke(prompt_recommendations)
        print("Datos enviados al frontend:", respuesta.content + "\n" + "Recomendaciones:", recomendaciones)
    
    except Exception as e:
        print("Error al generar recomendaciones:", e)
        respuesta = None
    
    return {
        #"recomendaciones": recomendaciones,
        "modelo_respuesta": respuesta.content if respuesta and respuesta.content else "No se puedo obtener una respuesta."
    }