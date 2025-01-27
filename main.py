import json
from typing import Optional
from fastapi import FastAPI, HTTPException
from langchain_aws import ChatBedrock
from pydantic import BaseModel
from src.config.config import *
from src.prompt import *
from src.qa import *

app = FastAPI()

class UserQuery(BaseModel):
    frase_usuario: str
    conversacion: list

@app.post("/consulta")
async def ask_chatbot(query: UserQuery):
    #print("Consulta en endpoint:", query.frase_usuario)
    try:
        response = get_qa(query.frase_usuario, query.conversacion)
        if response.get("mensaje"):
            return response
        else:
            raise HTTPException(status_code=404, detail="No se encontraron resultados")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la consulta: {e}")
    

# class FilterModel(BaseModel):
#     Marca: Optional[str] = None
#     Precio: Optional[tuple[int, int]] = None
#     Sexo: Optional[str] = None
#     Forma: Optional[str] = None
#     Balance: Optional[str] = None
#     Dureza: Optional[str] = None
#     Acabado: Optional[str] = None
#     Formato: Optional[str] = None
#     Superficie: Optional[str] = None
#     Núcleo: Optional[str] = None
#     Cara: Optional[str] = None
#     Nivel_de_juego: Optional[str] = None
#     Tipo_de_juego: Optional[str] = None
#     Jugador_profesional: Optional[str] = None



# @app.post("/recommend")
# async def apply_filters(filter_data: FilterModel):
#     dataset = cargar_dataset()
    
#     filtros = filter_data.model_dump()
#     print(f"Filtros aplicados: {filtros}")  #! Debug OK
    
#     # Aplicar filtros sobre el dataset
#     recomendaciones = []
#     for pala in dataset:

#         precio_float = convertir_precio(pala["Precio"])  # Convertir el precio a float
#         precio_min, precio_max = filtros.get('Precio', (None, None))

#         # Filtros obligatorios (Jugador, Precio, Nivel de juego)
#         if precio_min is not None and precio_float < precio_min:
#             continue
#         if precio_max is not None and precio_float > precio_max:
#             continue

#         # Filtrar Jugador
#         if filtros.get('Sexo'):
#             jugador_seleccionado = filtros['Sexo'].lower()
            
#             if 'Sin dato' in pala['Sexo'].lower():
#                 continue
#             # Si el jugador seleccionado es 'Hombre' o 'Mujer', también considerar las opciones 'Hombre, Mujer' y 'Mujer, Hombre'
#             if jugador_seleccionado == 'hombre' and 'hombre' not in pala['Sexo'].lower() and 'hombre, mujer' not in pala['Sexo'].lower():
#                 continue
#             if jugador_seleccionado == 'mujer' and 'mujer' not in pala['Sexo'].lower() and 'hombre, mujer' not in pala['Sexo'].lower():
#                 continue
#             # Si el jugador seleccionado es 'Junior', solo se devuelven las palas que tengan 'Junior'
#             if jugador_seleccionado == 'junior' and 'junior' not in pala['Sexo'].lower():
#                 continue


#         # Filtro Balance 
#         if filtros.get('balance'):
#             balance_selected = filtros['balance'].lower()
#             pala_balance = pala.get('Balance', '').lower()

#             if 'Sin dato' in pala_balance:
#                 continue
#             if balance_selected == "bajo" and not (
#                 "bajo" in pala_balance or "medio, bajo" in pala_balance):
#                 continue
#             if balance_selected == "medio" and not (
#                 "medio" in pala_balance or "medio, bajo" in pala_balance or "alto, medio" in pala_balance):
#                 continue
#             if balance_selected == "alto" and not (
#                 "alto" in pala_balance or "alto, medio" in pala_balance):
#                 continue

#         # Filtro Dureza
#         if filtros.get('dureza'):
#             dureza_selected = filtros['dureza'].lower()
#             pala_dureza = pala.get('Dureza', '').lower()
                    
#             if 'Sin dato' in pala_dureza:
#                 continue
#             if dureza_selected == "blanda" and not (
#                 "blanda" in pala_dureza or "media, blanda" in pala_dureza):
#                 continue
#             if dureza_selected == "media" and not (
#                 "media" in pala_dureza or "media, blanda" in pala_dureza or "dura, media" in pala_dureza):
#                 continue
#             if dureza_selected == "dura" and not (
#                 "dura" in pala_dureza or "dura, media" in pala_dureza):
#                 continue


#         # Filtro Acabado
#         if filtros.get('acabado'):
#             acabado_selected = filtros['acabado'].lower()
#             pala_acabado = pala.get('Acabado', '').lower()

#             if 'Sin dato' in pala_acabado:
#                 continue
#             if acabado_selected == "arenoso" and not any(
#                 x in pala_acabado for x in ["arenoso", "brillo, arenoso", "mate, arenoso", "relieve 3d, arenoso"]):
#                 continue
#             if acabado_selected == "brillo" and not any(
#                 x in pala_acabado for x in ["brillo", "brillo, arenoso", "brillo, mate", "brillo, relieve 3d"]):
#                 continue
#             if acabado_selected == "mate" and not any(
#                 x in pala_acabado for x in ["mate", "brillo, mate", "mate, relieve 3d", "mate, arenoso"]):
#                 continue
#             if acabado_selected == "relieve 3d" and not any(
#                 x in pala_acabado for x in ["relieve 3d", "relieve 3d, arenoso", "mate, relieve 3d", "brillo, relieve 3d"]):
#                 continue
#             if acabado_selected == "rugosa" and "rugosa" != pala_acabado:
#                 continue

#             # Manejo de combinaciones inversas
#             if acabado_selected in ["brillo, arenoso", "mate, arenoso", "relieve 3d, arenoso"]:
#                 if not any(x in pala_acabado for x in [acabado_selected, "arenoso", acabado_selected.split(", ")[0]]):
#                     continue
#             if acabado_selected in ["brillo, mate", "mate, relieve 3d", "brillo, relieve 3d"]:
#                 if not any(x in pala_acabado for x in [acabado_selected, acabado_selected.split(", ")[0], acabado_selected.split(", ")[1]]):
#                     continue

#         # Filtro Superficie con combinaciones
#         if filtros.get('superficie'):
#             superficie_selected = filtros['superficie'].lower()
#             pala_superficie = pala.get('Superficie', '').lower()

#             if 'Sin dato' in pala_superficie:
#                 continue
#             if superficie_selected == "arenosa" and not any(
#                 x in pala_superficie for x in ["arenosa", "rugosa, arenosa"]):
#                 continue
#             if superficie_selected == "rugosa" and not any(
#                 x in pala_superficie for x in ["rugosa", "rugosa, arenosa"]):
#                 continue
#             if superficie_selected == "lisa" and "lisa" != pala_superficie:
#                 continue

#             # Manejo de combinaciones inversas
#             if superficie_selected == "rugosa, arenosa" and not any(
#                 x in pala_superficie for x in ["rugosa", "arenosa", "rugosa, arenosa"]):
#                 continue


#         # Filtro Tipo de Juego
#         if filtros.get('tipo_juego'):
#             tipo_juego_selected = filtros['tipo_juego'].lower()
#             pala_tipo_juego = pala.get('Tipo de juego', '').lower()

#             if 'sin dato' in pala_tipo_juego:
#                 continue
#             if tipo_juego_selected == "control" and not any(
#                 x in pala_tipo_juego for x in ["control", "control, potencia"]):
#                 continue
#             if tipo_juego_selected == "potencia" and not any(
#                 x in pala_tipo_juego for x in ["potencia", "control, potencia"]):
#                 continue
#             if tipo_juego_selected == "polivalente" and "polivalente" != pala_tipo_juego:
#                 continue
#             if tipo_juego_selected == "control, potencia" and not any(
#                 x in pala_tipo_juego for x in ["control", "potencia", "control, potencia"]):
#                 continue


#         # Filtro Nivel de juego
#         if filtros.get('nivel_juego'):
#             nivel_juego_selected = filtros['nivel_juego'].lower()
#             pala_nivel_juego = pala.get('Nivel de juego', '').lower()

#             if 'Sin dato' in pala_nivel_juego:
#                 continue
#             if nivel_juego_selected == "principiante / intermedio" and not any(
#                 x in pala_nivel_juego for x in ["principiante / intermedio", "avanzado / competición, principiante / intermedio"]):
#                 continue
#             if nivel_juego_selected == "avanzado / competición" and not any(
#                 x in pala_nivel_juego for x in ["avanzado / competición", "avanzado / competición, profesional", "avanzado / competición, principiante / intermedio"]):
#                 continue
#             if nivel_juego_selected == "profesional" and not any(
#                 x in pala_nivel_juego for x in ["profesional", "avanzado / competición, profesional", "avanzado / competición, principiante / intermedio"]):
#                 continue
#             if nivel_juego_selected == "avanzado / competición, profesional" and not any(
#                 x in pala_nivel_juego for x in ["avanzado / competición, profesional", "profesional", "avanzado / competición, principiante / intermedio"]):
#                 continue
#             if nivel_juego_selected == "avanzado / competición, principiante / intermedio" and not any(
#                 x in pala_nivel_juego for x in ["avanzado / competición, principiante / intermedio", "principiante / intermedio", "avanzado / competición", "avanzado / competición, profesional"]):
#                 continue

#         # Filtro Marca
#         if filtros.get('marca'): #! Antes estaba de otra forma asi que no se si estará bien
#             marca_selected = filtros['marca'].lower()
            
#             # Si el valor de marca en la pala es 'Sin dato', se pasa al siguiente filtro
#             if 'Sin dato' in pala['Marca'].lower():
#                 continue

#             # Comprobación de marca
#             if marca_selected and marca_selected not in pala['Marca'].lower():
#                 continue


#         # Filtro Forma
#         if filtros.get('forma'): #! Antes estaba de otra forma asi que no se si estará bien
#             forma_selected = filtros['forma'].lower()
            
#             # Si el valor de forma en la pala es 'Sin dato', se pasa al siguiente filtro
#             if 'sin dato' in pala.get('Forma', '').lower():
#                 continue

#             # Comprobación de forma
#             if forma_selected and forma_selected != pala.get('Forma', '').lower():
#                 continue


#         # Filtro Jugador profesional #! Cuidado con colección_jugadores que ahora se llama Jugador profesional
#         if filtros.get('coleccion_jugadores') and filtros['coleccion_jugadores'] and filtros['coleccion_jugadores'].lower() != pala.get('Jugador profesional', '').lower():
#             continue

#         # Añadir la pala si cumple todos los filtros aplicables
#         recomendaciones.append({
#             "Nombre": pala["Nombre"],
#             "Marca": pala["Marca"],
#             "Color": pala["Color"],
#             "Balance": pala["Balance"],
#             "Dureza": pala["Dureza"],
#             "Acabado": pala["Acabado"],
#             "Superficie": pala["Superficie"],
#             "Tipo de juego": pala["Tipo de juego"],
#             "Nivel de juego": pala["Nivel de juego"],
#             "Jugador profesional": pala["Jugador profesional"],
#             "Precio": pala["Precio"],
#             "Imagen": pala["Imagen"],
#             "Enlace": pala["Enlace"],
#             "Descripción": pala["Descripción"]
#         })
    
#     # Limitar el número de recomendaciones a 5
#     recomendaciones = recomendaciones[:5]

#     contexto = formatear_recomendaciones(recomendaciones)
#     llm_haiku = ChatBedrock(model_id=LLM_CLAUDE_3_HAIKU, client=claude_3_haiku_client)
#     #print("CONTEXTO",contexto) #! Debug OK
    
#     try:
#         prompt_recommendations = prompt_template_recommendations.format(user_input=contexto, filters=filtros)
#         #print("PROMPT RECOMMENDATIONS",prompt_recommendations) #! Debug OK
#         respuesta = llm_haiku.invoke(prompt_recommendations)
#         #print("Datos enviados al frontend:", respuesta.content + "\n" + "Recomendaciones:", recomendaciones) #! Debug OK
    
#     except Exception as e:
#         print("Error al generar recomendaciones:", e)
#         respuesta = None
    
#     return {
#         #"recomendaciones": recomendaciones,
#         "modelo_respuesta": respuesta.content if respuesta and respuesta.content else "No se puedo obtener una respuesta."
#     }