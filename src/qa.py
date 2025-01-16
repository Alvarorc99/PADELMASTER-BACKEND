import datetime
import json
import time
from langchain_aws import ChatBedrock
from src.prompt import *
from src.schemas import IntentionOutput
from src.index_faiss.load_faiss_index import procesar_consulta, consultar_faiss, reformular_respuesta
from src.config.config import *

DATASET_PATH = "C:/Users/alvar/TFG/PADELMASTER BACKEND/dataset_padel_nuestro/palas_padelnuestro_actualizado/palas_padelnuestro_actualizado.json"
    
def get_qa(user_input: str):
    #print("Consulta recibida:", user_input)
    try:
        llm = ChatBedrock(model_id=LLM_MODEL_NAME, client=client)

        # Enviar la consulta al modelo para identificar la intención
        runnable = intention_template | llm.with_structured_output(schema=IntentionOutput)
        #print(f"Prompt que se enviará al modelo: {intention_template.template.format(user_input=user_input)}")
        #print("RUNNABLE:", runnable)

        respuesta = runnable.invoke({"user_input": user_input})
        print("Resultado de la intención:", respuesta)

        # Manejar las intenciones
        if respuesta.Saludo:
            print("Saludo recibido")
            prompt_message = greeting_template.format()
            message_response = llm.invoke(prompt_message)
            mensaje_usuario = message_response.content
            return {
                "mensaje": mensaje_usuario
            }

        elif respuesta.Consulta_tecnica:
            print("Consulta técnica recibida")
            prompt = prompt_template.format(user_input=user_input)
            respuesta = llm.invoke(prompt)
            return {
                "mensaje": respuesta.content
            }

        elif respuesta.Consulta_personalizada:
            print("Consulta personalizada recibida")
            nombre_pala, atributo = procesar_consulta(user_input)
            print("Nombre de la pala y atributo:", nombre_pala, atributo)
            if nombre_pala and atributo:
                resultado_faiss = consultar_faiss("C:/Users/alvar/TFG/PADELMASTER BACKEND/faiss/faiss_index", nombre_pala, atributo)
                respuesta_final = reformular_respuesta(resultado_faiss, nombre_pala, atributo)
                return {
                    "mensaje": respuesta_final
                }

        else:
            mensaje_usuario = "Lo siento, soy un asistente virtual encargado únicamente al mundo del pádel. No puedo ayudarte con esa consulta."
            return {
                "mensaje": mensaje_usuario
            }

    except Exception as e:
        print(f"Error en get_qa: {e}")
        return {"error": f"Error en el servidor: {e}"}

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
        mensaje += f"  **Imagen**: {pala['Imagen']}\n"
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
        mensaje += f"  **Enlace**: {pala['Enlace']}\n"
        mensaje += f"  **Descripción**: {pala['Descripción']}\n"
    
    return mensaje