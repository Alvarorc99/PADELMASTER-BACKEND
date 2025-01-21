import json
from langchain_aws import ChatBedrock
from src.prompt import *
from src.schemas import IntentionOutput, QuestionOutput
from src.index_faiss.load_faiss_index import procesar_consulta, consultar_faiss, reformular_respuesta, reformular_respuesta_sin_resultados
from src.config.config import *

DATASET_PATH = "C:/Users/alvar/TFG/PADELMASTER BACKEND/dataset_padel_nuestro/palas_padelnuestro_actualizado/palas_padelnuestro_actualizado.json"
    
def get_qa(user_input: str, conversation: list):
    #print("Consulta recibida:", user_input)
   
    try:
        # Uso de modelos
        llm_haiku = ChatBedrock(model_id=LLM_CLAUDE_3_HAIKU, client=claude_3_haiku_client)
        llm_sonnet = ChatBedrock(model_id=LLM_CLAUDE_SONNET, client=sonnet_client)

        runnable = conversation_template | llm_haiku.with_structured_output(schema=QuestionOutput)

        respuesta = runnable.invoke({"user_input": user_input, "conversation": conversation})
        pregunta_reformulada = respuesta.Pregunta

        # Enviar la consulta al modelo para identificar la intención
        runnable = intention_template | llm_haiku.with_structured_output(schema=IntentionOutput)
        #print(f"Prompt que se enviará al modelo: {intention_template.template.format(user_input=user_input)}")
        #print("RUNNABLE:", runnable)
        respuesta = runnable.invoke({"user_input": pregunta_reformulada})
        print("Resultado de la intención:", respuesta)
        
        #? Manejar las intenciones
        if respuesta.Saludo: # TODO OK
            print("Saludo recibido")
            prompt_message = greeting_template.format(user_input=user_input)
            message_response = llm_sonnet.invoke(prompt_message)
            mensaje_usuario = message_response.content
            return {
                "tipo": "Saludo",
                "mensaje": mensaje_usuario,
                "imagen_url": None,
            }
        
        elif respuesta.Consulta_tecnica: # TODO OK
            print("Consulta técnica recibida")
            prompt_message = prompt_template.format(user_input=pregunta_reformulada)
            message_response = llm_sonnet.invoke(prompt_message)
            mensaje_usuario = message_response.content
            return {
                "tipo": "Consulta_tecnica",
                "mensaje": mensaje_usuario,
                "imagen_url": None,
            }
        
        elif respuesta.Consulta_personalizada:
            print("Consulta personalizada recibida:", user_input)
            nombre_pala, atributo = procesar_consulta(consulta=user_input)
            print(f"Nombre de la pala {nombre_pala} y atributo {atributo}:")

            if nombre_pala and atributo:
                resultado_faiss = consultar_faiss("C:/Users/alvar/TFG/PADELMASTER BACKEND/faiss/faiss_index", nombre_pala, atributo)

                if resultado_faiss["similares"]:
                    palas_con_imagenes = [
                        f"{p['nombre']} (Imagen: {p['imagen']})" for p in resultado_faiss["similares"]
                    ]
                    respuesta_final = reformular_respuesta_sin_resultados(palas_con_imagenes, nombre_pala, atributo)
                    print("No ha encontrado la pala y ha devuelto palas similares:", respuesta_final)
                    return {
                        "tipo": "Consulta_personalizada",
                        "mensaje": respuesta_final,
                        "imagen_url": imagen_url,
                    }
                elif resultado_faiss["exacto"]:
                    valor_atributo = resultado_faiss["exacto"]["atributo"]
                    imagen_url = resultado_faiss["exacto"]["imagen"]
                    respuesta_final = reformular_respuesta(valor_atributo, nombre_pala, atributo)
                    print("Ha encontrado la pala. Datos: ", respuesta_final)                    
                    return {
                        "tipo": "Consulta_personalizada",
                        "mensaje": respuesta_final,
                        "imagen_url": imagen_url,
                    }
                else:
                    return {
                        "tipo": "Consulta_personalizada",
                        "mensaje": f"No se encontró ninguna información sobre la pala '{nombre_pala}'.",
                        "imagen_url": None,
                    }
            else:
                return{
                    "tipo": "Consulta_personalizada",
                    "mensaje": "No se pudieron procesar los datos de la consulta.",
                    "imagen_url": None,
                }
                
        elif respuesta.Recomendacion:
            print("Recomendación recibida")
            prompt_message = recomendation.format(mensaje=pregunta_reformulada)
            message_response = llm_sonnet.invoke(prompt_message)
            mensaje_usuario = message_response.content
            return {
                "tipo": "Recomendacion",
                "mensaje": mensaje_usuario
            }

        else:
            mensaje_usuario = "Lo siento, soy un asistente virtual encargado únicamente al mundo del pádel. No puedo ayudarte con esa consulta."
            return {
                "mensaje": mensaje_usuario
            }
    except ValueError as e:
        logger.error(f"Error al desempaquetar valores: {e}")
        return {"error": "Error al interpretar la consulta. Por favor, revisa tu entrada."}
    except Exception as e:
        print(f"Error inesperado: {e}")
        return {"error": f"Error interno: {str(e)}"}

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