"""File to define the functions for the QA process"""

from dataclasses import dataclass
import json
import random
from typing import Optional
from langchain_aws import ChatBedrock
from datetime import datetime
import src.prompt as pro
import src.schemas as sch
from src.index_faiss.load_faiss_index import process_query, consult_faiss, reformular_respuesta, reformular_respuesta_sin_resultados
from src.config.config import *
    
def get_qa(user_input: str, conversation: list):
    """
    Función que recibe una consulta del usuario y devuelve una respuesta en formato JSON.
    
    Args:
        user_input (str): La consulta del usuario.
        conversation (list): La conversación entre el usuario y el chatbot.

    Returns:
        Respuesta en formato JSON.
    """   
    try:
        conversation_window = conversation[-5:]
        cleaned_conversation = [
            {
                'usuario': item['user_input'], 
                'respuesta': item['answer'], 
                'tipo': item['type']
            } 
                for item in conversation_window
        ]
        logger.debug("Cleaned conversation context: %s", cleaned_conversation)

        llm_haiku = ChatBedrock(model_id=LLM_CLAUDE_3_HAIKU, client=claude_3_haiku_client)

        runnable = pro.conversation_template | llm_haiku.with_structured_output(schema=sch.QuestionOutput)
        answer = runnable.invoke({"user_input": user_input, "conversation": cleaned_conversation})
        reformulated_question = answer.Question
        logger.info("Reformulated question: %s", reformulated_question)

        runnable = pro.intention_template | llm_haiku.with_structured_output(schema=sch.IntentionOutput)
        intention = runnable.invoke({"user_input": reformulated_question})
        logger.info("User intention determined: %s", intention)

        if intention.Greeting:
            current_hour = datetime.now().hour
            prompt_message = pro.greeting_template.format(user_input=reformulated_question, current_hour=current_hour)
            answer = llm_haiku.invoke(prompt_message)
            chatbot_response = answer.content
            logger.info("Chatbot response (greeting): %s", chatbot_response)
            return {
                "type": "Greeting",
                "answer": chatbot_response,
            }
        
        elif intention.Technical_query:
            prompt_message = pro.prompt_template.format(user_input=user_input, conversation=cleaned_conversation)
            answer = llm_haiku.invoke(prompt_message)
            chatbot_response = answer.content
            logger.info("Chatbot response (technical query): %s", chatbot_response)
            return {
                "type": "Technical_query",
                "answer": chatbot_response,
            }
        
        elif intention.Personalized_query:
            nombre_pala, atributos = process_query(query=reformulated_question)

            if nombre_pala and atributos:
                resultado_faiss = consult_faiss(FAISS_INDEX_PATH, nombre_pala, atributos)

                if resultado_faiss["similares"]:
                    chatbot_response = reformular_respuesta_sin_resultados(nombre_pala)
                    
                    return {
                        "type": "Personalized_query",
                        "answer": chatbot_response,
                        "img": resultado_faiss["similares"],
                        "similares": True,
                    }
                elif resultado_faiss["exacto"]:
                    valores_atributos = resultado_faiss["exacto"]["atributos"]
                    imagen_url = resultado_faiss["exacto"]["imagen"]
                    chatbot_response = reformular_respuesta(valores_atributos, nombre_pala, atributos, cleaned_conversation)
                    
                    return {
                        "type": "Personalized_query",
                        "answer": chatbot_response,
                        "img": imagen_url,
                    }
                else:
                    return {
                        "type": "Personalized_query",
                        "answer": f"No se encontró ninguna información sobre la pala '{nombre_pala}'.",
                    }
            else:
                return{
                    "type": "Personalized_query",
                    "answer": "No se pudieron procesar los datos de la consulta.",
                }

                
        elif intention.Recommendation:
            prompt_message = pro.recomendation.format(message=reformulated_question, conversation=cleaned_conversation)
            answer = llm_haiku.invoke(prompt_message)
            chatbot_response = answer.content
            logger.info("Chatbot response (recommendation): %s", chatbot_response)
            return {
                "type": "Recommendation",
                "answer": chatbot_response
            }
        
        elif intention.Personalized_recommendation:
            prompt_personalized_recommendation = pro.recomendacion_personalizada_template.format(user_input=reformulated_question, conversation=cleaned_conversation)
            answer = llm_haiku.invoke(prompt_personalized_recommendation)
            logger.info("Answer reformulated: %s", answer.content)

            message_data = json.loads(answer.content)

            # Validar y convertir "Precio" si es necesario
            if "Precio" in message_data and isinstance(message_data["Precio"], list) and len(message_data["Precio"]) == 2:
                message_data["Precio"] = tuple(message_data["Precio"])  
            elif "Precio" in message_data and not isinstance(message_data["Precio"], (tuple, list)):
                logger.error("Error: El campo 'Precio' tiene un formato incorrecto:", message_data["Precio"])
                message_data["Precio"] = None 
            
            filters = FilterModel(
                Marca=message_data.get("Marca"),
                Sexo=message_data.get("Sexo"),
                Forma=message_data.get("Forma"),
                Balance=message_data.get("Balance"),
                Dureza=message_data.get("Dureza"),
                Acabado=message_data.get("Acabado"),
                Superficie=message_data.get("Superficie"),
                Núcleo=message_data.get("Núcleo"),
                Cara=message_data.get("Cara"),
                Nivel_de_juego=message_data.get("Nivel_de_juego"),
                Tipo_de_juego=message_data.get("Tipo_de_juego"),
                Jugador_profesional=message_data.get("Jugador_profesional"),
                Precio_min=message_data.get("Precio_min"),
                Precio_max=message_data.get("Precio_max")
            )

            chatbot_response, recommendations = apply_filters(filters) 
            logger.info("Chatbot response (personalized_recommendation): %s", chatbot_response)
            return {
                "type": "Personalized_recommendation",
                "answer": chatbot_response,
                "recommendations": recommendations,
            }

        else:
            prompt_message = pro.other_intention_template.format(user_input=reformulated_question, conversation=cleaned_conversation)
            answer = llm_haiku.invoke(prompt_message)
            chatbot_response = answer.content
            logger.info("Chatbot response (Other): %s", chatbot_response)
            return {
                "type": "Other",
                "answer": chatbot_response
            }
    except Exception as e:
        logger.info("Unexcepted error in get_qa: %s", e)
        return {"answer": "Lo siento, la consulta no se ha podido procesar."}

def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def convert_price(precio_str: str) -> float:
    """Convierte una cadena de precio con formato europeo a float."""
    precio_limpio = precio_str.replace("€", "").replace(",", ".").strip()
    try:
        return float(precio_limpio)
    except ValueError:
        raise ValueError(f"No se pudo convertir el precio: {precio_str}")


def format_recommendations(recommendations):
    """Devuelve las recomendaciones formateadas como una cadena de texto legible."""
    if not recommendations:
        return "No se encontraron palas de pádel que coincidan con tus criterios."
    
    mensaje = "Aquí tienes algunas recomendaciones de palas de pádel basadas en tus criterios:\n\n"
    for pala in recommendations:
        mensaje += f"• **Nombre**: {pala['Nombre']}\n"
        mensaje += f"  **Sexo**: {pala['Sexo']}\n"
        mensaje += f"  **Precio**: {pala['Precio']}\n"
        mensaje += f"  **Balance**: {pala['Balance']}\n"
        mensaje += f"  **Dureza**: {pala['Dureza']}\n"
        mensaje += f"  **Núcleo**: {pala['Núcleo']}\n"
        mensaje += f"  **Cara**: {pala['Cara']}\n"
        mensaje += f"  **Acabado**: {pala['Acabado']}\n"
        mensaje += f"  **Forma**: {pala['Forma']}\n"
        mensaje += f"  **Superficie**: {pala['Superficie']}\n"
        mensaje += f"  **Tipo de juego**: {pala['Tipo de juego']}\n"
        mensaje += f"  **Nivel de juego**: {pala['Nivel de juego']}\n"
        mensaje += f"  **Jugador profesional**: {pala['Jugador profesional']}\n"
        mensaje += f"  **Descripción**: {pala['Descripción']}\n"
    
    return mensaje

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
    Núcleo: Optional[str] = None
    Cara: Optional[str] = None
    Nivel_de_juego: Optional[str] = None
    Tipo_de_juego: Optional[str] = None
    Jugador_profesional: Optional[str] = None

def apply_filters(filtros: FilterModel):
    dataset = load_dataset()
    
    filtros = filtros.__dict__
    
    recommendations = []
    for pala in dataset:

        precio_float = convert_price(pala['Precio'])
        precio_min = filtros.get('Precio_min', None)
        precio_max = filtros.get('Precio_max', None)

        # Filtras por Precio
        if precio_min is not None and precio_float < precio_min:
            continue
        if precio_max is not None and precio_float > precio_max:
            continue

        # Filtrar Jugador
        if filtros.get('Sexo'):
            jugador_seleccionado = filtros['Sexo'].lower()
            
            if 'Sin dato' in pala['Sexo'].lower():
                continue
            if jugador_seleccionado == 'hombre' and 'hombre' not in pala['Sexo'].lower() and 'hombre, mujer' not in pala['Sexo'].lower():
                continue
            if jugador_seleccionado == 'mujer' and 'mujer' not in pala['Sexo'].lower() and 'hombre, mujer' not in pala['Sexo'].lower():
                continue
            if jugador_seleccionado == 'junior' and 'junior' not in pala['Sexo'].lower():
                continue

        # Filtro Balance 
        if filtros.get('Balance'):
            balance_selected = filtros['Balance'].lower()
            pala_balance = pala.get('Balance', '').lower()

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

            # Manejo de combinaciones
            if acabado_selected in ["brillo, arenoso", "mate, arenoso", "relieve 3d, arenoso"]:
                if not any(x in pala_acabado for x in [acabado_selected, "arenoso", acabado_selected.split(", ")[0]]):
                    continue
            if acabado_selected in ["brillo, mate", "mate, relieve 3d", "brillo, relieve 3d"]:
                if not any(x in pala_acabado for x in [acabado_selected, acabado_selected.split(", ")[0], acabado_selected.split(", ")[1]]):
                    continue

        # Filtro Superficie
        if filtros.get('Superficie'):
            superficie_selected = filtros['Superficie'].lower()
            pala_superficie = pala.get('Superficie', '').lower()

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

            # Manejo de combinaciones
            if superficie_selected == "rugosa, arenosa" and not any(
                x in pala_superficie for x in ["rugosa", "arenosa", "rugosa, arenosa"]):
                continue

        # Filtro Tipo de juego
        if filtros.get('Tipo_de_juego'):
            tipo_juego_selected = filtros['Tipo_de_juego'].lower()
            pala_tipo_juego = pala.get('Tipo de juego', '').lower()

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
        
        # Filtrar por Núcleo
        if filtros.get('Núcleo'):
            nucleo_selected = filtros['Núcleo'].lower()
            pala_nucleo = pala.get('Núcleo', '').lower()

            if 'Sin dato' in pala_nucleo:
                continue
            if nucleo_selected != pala_nucleo:
                continue

        # Filtrar por Cara
        if filtros.get('Cara'):
            cara_selected = filtros['Cara'].lower()
            pala_cara = pala.get('Cara', '').lower()

            if 'Sin dato' in pala_cara:
                continue
            if cara_selected != pala_cara:
                continue
        
        # Filtrar por Forma
        if filtros.get('Forma'):
            forma_selected = filtros['Forma'].lower()
            pala_forma = pala.get('Forma', '').lower()

            if 'Sin dato' in pala_forma:
                continue
            if forma_selected != pala_forma:
                continue

        # Filtro Marca
        if filtros.get('Marca') and filtros['Marca'] and filtros['Marca'].lower() not in pala['Marca'].lower():
            continue

        # Filtro Jugador profesional
        if filtros.get('Jugador_profesional') and filtros['Jugador_profesional'] and filtros['Jugador_profesional'].lower() != pala.get('Jugador profesional', '').lower():
            continue

        recommendations.append({
            "Nombre": pala["Nombre"],
            "Sexo": pala["Sexo"],
            "Marca": pala["Marca"],
            "Color": pala["Color"],
            "Balance": pala["Balance"],
            "Dureza": pala["Dureza"],
            "Acabado": pala["Acabado"],
            "Superficie": pala["Superficie"],
            "Núcleo": pala["Núcleo"],
            "Cara": pala["Cara"],
            "Forma": pala["Forma"],
            "Tipo de juego": pala["Tipo de juego"],
            "Nivel de juego": pala["Nivel de juego"],
            "Jugador profesional": pala["Jugador profesional"],
            "Precio": pala["Precio"],
            "Imagen": pala["Imagen"],
            "Enlace": pala["Enlace"],
            "Descripción": pala["Descripción"]
        })

    random.shuffle(recommendations)
    
    recommendations = recommendations[:3]

    context = format_recommendations(recommendations)
    llm_haiku = ChatBedrock(model_id=LLM_CLAUDE_3_HAIKU, client=claude_3_haiku_client)
    
    try:
        prompt_recommendations = pro.prompt_template_recommendations.format(user_input=context, filters=filtros)
        respuesta = llm_haiku.invoke(prompt_recommendations)
    
    except Exception as e:
        logger.error("Error al generar recomendaciones:", e)
        respuesta = None
    
    return respuesta.content, recommendations