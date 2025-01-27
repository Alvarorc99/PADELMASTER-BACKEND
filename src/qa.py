from dataclasses import dataclass
import json
from typing import Optional
from fastapi import requests
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
            message_response = llm_haiku.invoke(prompt_message)
            mensaje_usuario = message_response.content
            return {
                "tipo": "Saludo",
                "mensaje": mensaje_usuario,
                "imagen_url": None,
            }
        
        elif respuesta.Consulta_tecnica: # TODO OK
            print("Consulta técnica recibida")
            prompt_message = prompt_template.format(user_input=pregunta_reformulada)
            message_response = llm_haiku.invoke(prompt_message)
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
                    imagen_url_similar = resultado_faiss["similares"][0].get("imagen_url", "URL_DE_IMAGEN_POR_DEFECTO")
                    print("Imagen URL similar:", imagen_url_similar)
                    
                    # Crear lista de palas con imágenes en el formato adecuado
                    palas_con_imagenes = [
                        f"{p['nombre']} (Imagen: {p['imagen_url']})" for p in resultado_faiss["similares"]
                    ]
                    
                    respuesta_final = reformular_respuesta_sin_resultados(palas_con_imagenes, nombre_pala, atributo)
                    print("No ha encontrado la pala y ha devuelto palas similares:", respuesta_final)
                    
                    return {
                        "tipo": "Consulta_personalizada",
                        "mensaje": respuesta_final,
                        "imagenes": resultado_faiss["similares"],  # Devuelve todas las palas con sus imágenes
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
            message_response = llm_haiku.invoke(prompt_message)
            mensaje_usuario = message_response.content
            return {
                "tipo": "Recomendacion",
                "mensaje": mensaje_usuario
            }
        
        elif respuesta.Recomendacion_personalizada:
            print("Recomendación personalizada recibida")
            prompt_recomendacion_personalizada = recomendacion_personalizada_template.format(user_input=pregunta_reformulada)
            message_response = llm_haiku.invoke(prompt_recomendacion_personalizada)
            print("Datos extraidos:", message_response.content)

            message_data = json.loads(message_response.content)  # Convertir a diccionario

            # Validar y convertir 'Precio' si es necesario
            if "Precio" in message_data and isinstance(message_data["Precio"], list) and len(message_data["Precio"]) == 2:
                message_data["Precio"] = tuple(message_data["Precio"])  # Asegurarte de que sea una tupla
            elif "Precio" in message_data and not isinstance(message_data["Precio"], (tuple, list)):
                print("Error: El campo 'Precio' tiene un formato incorrecto:", message_data["Precio"])
                message_data["Precio"] = None  # O lanza una excepción si es crítico

            # if isinstance(message_data.get("Precio"), tuple):
            #     message_data["Precio"] = list(message_data["Precio"])

            print("Datos de entrada (JSON):", message_data) #! OK
            
            filtros = FilterModel(
                Marca=message_data.get("Marca"),
                Sexo=message_data.get("Sexo"),
                Forma=message_data.get("Forma"),
                Balance=message_data.get("Balance"),
                Dureza=message_data.get("Dureza"),
                Acabado=message_data.get("Acabado"),
                Superficie=message_data.get("Superficie"),
                Nucleo=message_data.get("Núcleo"),
                Cara=message_data.get("Cara"),
                Nivel_de_juego=message_data.get("Nivel_de_juego"),
                Tipo_de_juego=message_data.get("Tipo_de_juego"),
                Jugador_profesional=message_data.get("Jugador_profesional"),
                Precio_min=message_data.get("Precio_min"),
                Precio_max=message_data.get("Precio_max")
            )
            #print(f"Filtros creados: {filtros.__dict__}") #! Esto sale todo a None
            #print("Claves esperadas por FilterModel:", FilterModel.__annotations__.keys()) #! Esto sale todo a None

            recomendaciones = apply_filters(filtros)

            print("Recomendaciones:", recomendaciones)

            return {
                "tipo": "Recomendacion_personalizada",
                "mensaje": recomendaciones,
                "imagen_url": None,
            }

        else:
            mensaje_usuario = "Lo siento, soy un asistente virtual encargado únicamente al mundo del pádel. No puedo ayudarte con esa consulta."
            return {
                "tipo": "Otro",
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
    # Limpiar la cadena
    precio_limpio = precio_str.replace("€", "").replace(",", ".").strip()  # Eliminar símbolo y reemplazar coma por punto
    try:
        return float(precio_limpio)
    except ValueError:
        raise ValueError(f"No se pudo convertir el precio: {precio_str}")


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
        mensaje += f"  **Superficie**: {pala['Superficie']}\n"
        mensaje += f"  **Tipo de juego**: {pala['Tipo de juego']}\n"
        mensaje += f"  **Nivel de juego**: {pala['Nivel de juego']}\n"
        mensaje += f"  **Jugador profesional**: {pala['Jugador profesional']}\n"
        mensaje += f"  **Enlace**: {pala['Enlace']}\n"
        mensaje += f"  **Descripción**: {pala['Descripción']}\n"
    
    return mensaje



# Definir un modelo de datos con las características de las palas
@dataclass
class FilterModel:
    Marca: Optional[str] = None
    Precio_min: Optional[float] = None
    Precio_max: Optional[float] = None
    Sexo: Optional[str] = None
    Forma: Optional[str] = None
    Balance: Optional[str] = None
    Dureza: Optional[str] = None
    Acabado: Optional[str] = None
    Superficie: Optional[str] = None
    Nucleo: Optional[str] = None
    Cara: Optional[str] = None
    Nivel_de_juego: Optional[str] = None
    Tipo_de_juego: Optional[str] = None
    Jugador_profesional: Optional[str] = None

def apply_filters(filtros: FilterModel):
    dataset = cargar_dataset()
    
    #filtros = filtros.model_dump()
    filtros = filtros.__dict__
    print(f"Filtros aplicados: {filtros}")  #! No sale tipo_de_juego y nivel_de_juego
    
    # Aplicar filtros sobre el dataset
    recomendaciones = []
    for pala in dataset:
        #print(f"Pala: {pala}")
        #print(f"Precio: {pala['Precio']}")
        precio_float = convertir_precio(pala['Precio'])  # Convertir el precio a float
        #print(f"Precio_float: {precio_float}")
        precio_min = filtros.get('Precio_min', None)
        precio_max = filtros.get('Precio_max', None)
        #print(f"Valor de precio_min: {precio_min}, de precio_max: {precio_max}")

        # Filtros obligatorios (Jugador, Precio, Nivel de juego)
        if precio_min is not None and precio_float < precio_min:
            continue
        if precio_max is not None and precio_float > precio_max:
            continue

        # Filtrar Jugador
        if filtros.get('Sexo'):
            jugador_seleccionado = filtros['Sexo'].lower()

            #print("Sexo seleccionado:", jugador_seleccionado)
            
            if 'Sin dato' in pala['Sexo'].lower():
                continue
            # Si el jugador seleccionado es 'Hombre' o 'Mujer', también considerar las opciones 'Hombre, Mujer' y 'Mujer, Hombre'
            if jugador_seleccionado == 'hombre' and 'hombre' not in pala['Sexo'].lower() and 'hombre, mujer' not in pala['Sexo'].lower():
                continue
            if jugador_seleccionado == 'mujer' and 'mujer' not in pala['Sexo'].lower() and 'hombre, mujer' not in pala['Sexo'].lower():
                continue
            # Si el jugador seleccionado es 'Junior', solo se devuelven las palas que tengan 'Junior'
            if jugador_seleccionado == 'junior' and 'junior' not in pala['Sexo'].lower():
                continue


        # Filtro Balance 
        if filtros.get('Balance'):
            balance_selected = filtros['Balance'].lower()
            pala_balance = pala.get('Balance', '').lower()

            #print("Balance seleccionado:", balance_selected)

            if 'Sin dato' in pala_balance:
                continue
            if balance_selected == "bajo" and not (
                "bajo" in pala_balance or "medio, bajo" in pala_balance):
                continue
            if balance_selected == "medio" and not (
                "medio" in pala_balance or "medio, bajo" in pala_balance or "alto, medio" in pala_balance):
                continue
            if balance_selected == "alto" and not (
                "alto" in pala_balance or "alto, medio" in pala_balance):
                continue

        # Filtro Dureza
        if filtros.get('Dureza'):
            dureza_selected = filtros['Dureza'].lower()
            pala_dureza = pala.get('Dureza', '').lower()

            #print("Dureza seleccionada:", dureza_selected)
                    
            if 'Sin dato' in pala_dureza:
                continue
            if dureza_selected == "blanda" and not (
                "blanda" in pala_dureza or "media, blanda" in pala_dureza):
                continue
            if dureza_selected == "media" and not (
                "media" in pala_dureza or "media, blanda" in pala_dureza or "dura, media" in pala_dureza):
                continue
            if dureza_selected == "dura" and not (
                "dura" in pala_dureza or "dura, media" in pala_dureza):
                continue


        # Filtro Acabado
        if filtros.get('Acabado'):
            acabado_selected = filtros['Acabado'].lower()
            pala_acabado = pala.get('Acabado', '').lower()

            #print("Acabado seleccionado:", acabado_selected)

            if 'Sin dato' in pala_acabado:
                continue
            if acabado_selected == "arenoso" and not any(
                x in pala_acabado for x in ["arenoso", "brillo, arenoso", "mate, arenoso", "relieve 3d, arenoso"]):
                continue
            if acabado_selected == "brillo" and not any(
                x in pala_acabado for x in ["brillo", "brillo, arenoso", "brillo, mate", "brillo, relieve 3d"]):
                continue
            if acabado_selected == "mate" and not any(
                x in pala_acabado for x in ["mate", "brillo, mate", "mate, relieve 3d", "mate, arenoso"]):
                continue
            if acabado_selected == "relieve 3d" and not any(
                x in pala_acabado for x in ["relieve 3d", "relieve 3d, arenoso", "mate, relieve 3d", "brillo, relieve 3d"]):
                continue
            if acabado_selected == "rugosa" and "rugosa" != pala_acabado:
                continue

            # Manejo de combinaciones inversas
            if acabado_selected in ["brillo, arenoso", "mate, arenoso", "relieve 3d, arenoso"]:
                if not any(x in pala_acabado for x in [acabado_selected, "arenoso", acabado_selected.split(", ")[0]]):
                    continue
            if acabado_selected in ["brillo, mate", "mate, relieve 3d", "brillo, relieve 3d"]:
                if not any(x in pala_acabado for x in [acabado_selected, acabado_selected.split(", ")[0], acabado_selected.split(", ")[1]]):
                    continue

        # Filtro Superficie con combinaciones
        if filtros.get('Superficie'):
            superficie_selected = filtros['Superficie'].lower()
            pala_superficie = pala.get('Superficie', '').lower()

            #print("Superficie seleccionada:", superficie_selected)

            if 'Sin dato' in pala_superficie:
                continue
            if superficie_selected == "arenosa" and not any(
                x in pala_superficie for x in ["arenosa", "rugosa, arenosa"]):
                continue
            if superficie_selected == "rugosa" and not any(
                x in pala_superficie for x in ["rugosa", "rugosa, arenosa"]):
                continue
            if superficie_selected == "lisa" and "lisa" != pala_superficie:
                continue

            # Manejo de combinaciones inversas
            if superficie_selected == "rugosa, arenosa" and not any(
                x in pala_superficie for x in ["rugosa", "arenosa", "rugosa, arenosa"]):
                continue


        # Filtro Tipo de Juego
        if filtros.get('Tipo_de_juego'):
            tipo_juego_selected = filtros['Tipo_de_juego'].lower()
            pala_tipo_juego = pala.get('Tipo de juego', '').lower()

            #print("Tipo de juego seleccionado:", tipo_juego_selected)

            if 'Sin dato' in pala_tipo_juego:
                continue
            if tipo_juego_selected == "control" and not any(
                x in pala_tipo_juego for x in ["control", "control, potencia"]):
                continue
            if tipo_juego_selected == "potencia" and not any(
                x in pala_tipo_juego for x in ["potencia", "control, potencia"]):
                continue
            if tipo_juego_selected == "polivalente" and "polivalente" != pala_tipo_juego:
                continue
            if tipo_juego_selected == "control, potencia" and not any(
                x in pala_tipo_juego for x in ["control", "potencia", "control, potencia"]):
                continue


        # Filtro Nivel de juego
        if filtros.get('Nivel_de_juego'):
            nivel_juego_selected = filtros['Nivel_de_juego'].lower()
            pala_nivel_juego = pala.get('Nivel de juego').lower()

            #print("Nivel de juego seleccionado:", nivel_juego_selected)

            if 'Sin dato' in pala_nivel_juego:
                continue
            if nivel_juego_selected == "principiante / intermedio" and not any(
                x in pala_nivel_juego for x in ["principiante / intermedio", "avanzado / competición, principiante / intermedio"]):
                continue
            if nivel_juego_selected == "avanzado / competición" and not any(
                x in pala_nivel_juego for x in ["avanzado / competición", "avanzado / competición, profesional", "avanzado / competición, principiante / intermedio"]):
                continue
            if nivel_juego_selected == "profesional" and not any(
                x in pala_nivel_juego for x in ["profesional", "avanzado / competición, profesional", "avanzado / competición, principiante / intermedio"]):
                continue
            if nivel_juego_selected == "avanzado / competición, profesional" and not any(
                x in pala_nivel_juego for x in ["avanzado / competición, profesional", "profesional", "avanzado / competición, principiante / intermedio"]):
                continue
            if nivel_juego_selected == "avanzado / competición, principiante / intermedio" and not any(
                x in pala_nivel_juego for x in ["avanzado / competición, principiante / intermedio", "principiante / intermedio", "avanzado / competición", "avanzado / competición, profesional"]):
                continue

        # Filtro Marca
        if filtros.get('Marca') and filtros['Marca'] and filtros['Marca'].lower() not in pala['Marca'].lower():
            continue


        # Filtro Forma
        if filtros.get('Forma'): #! Antes estaba de otra forma asi que no se si estará bien
            forma_selected = filtros['Forma'].lower()

            #print("Forma seleccionada:", forma_selected)
            
            # Si el valor de forma en la pala es 'Sin dato', se pasa al siguiente filtro
            if 'Sin dato' in pala.get('Forma', '').lower():
                continue

            # Comprobación de forma
            if forma_selected and forma_selected != pala.get('Forma', '').lower():
                continue


        # Filtro Jugador profesional #! Cuidado con colección_jugadores que ahora se llama Jugador profesional
        if filtros.get('Jugador_profesional') and filtros['Jugador_profesional'] and filtros['Jugador_profesional'].lower() != pala.get('Jugador profesional', '').lower():
            continue

        # Añadir la pala si cumple todos los filtros aplicables
        recomendaciones.append({
            "Nombre": pala["Nombre"],
            "Marca": pala["Marca"],
            "Color": pala["Color"],
            "Balance": pala["Balance"],
            "Dureza": pala["Dureza"],
            "Acabado": pala["Acabado"],
            "Superficie": pala["Superficie"],
            "Tipo de juego": pala["Tipo de juego"],
            "Nivel de juego": pala["Nivel de juego"],
            "Jugador profesional": pala["Jugador profesional"],
            "Precio": pala["Precio"],
            "Imagen": pala["Imagen"],
            "Enlace": pala["Enlace"],
            "Descripción": pala["Descripción"]
        })
    
    # Limitar el número de recomendaciones a 5
    recomendaciones = recomendaciones[:10]

    contexto = formatear_recomendaciones(recomendaciones)
    llm_haiku = ChatBedrock(model_id=LLM_CLAUDE_3_HAIKU, client=claude_3_haiku_client)
    #print("CONTEXTO",contexto) #! Debug OK
    
    try:
        prompt_recommendations = prompt_template_recommendations.format(user_input=contexto, filters=filtros)
        #print("PROMPT RECOMMENDATIONS",prompt_recommendations) #! Debug OK
        respuesta = llm_haiku.invoke(prompt_recommendations)
        #print("\nRESPUESTA: ", respuesta.content)
    
    except Exception as e:
        print("Error al generar recomendaciones:", e)
        respuesta = None
    
    return respuesta.content
    # return {
    #     "modelo_respuesta": respuesta.content if respuesta and respuesta.content else "No se puedo obtener una respuesta."
    # }