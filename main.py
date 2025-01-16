import json
from typing import Optional
from fastapi import FastAPI, HTTPException
from langchain_aws import ChatBedrock
from pydantic import BaseModel
from src.config.config import *
from src.prompt import *
#from src.index_faiss import load_faiss_index
from src.qa import *

app = FastAPI()

class UserQuery(BaseModel):
    frase_usuario: str

@app.post("/consulta")
async def ask_chatbot(query: UserQuery):
    #print("Consulta en endpoint:", query.frase_usuario)
    try:
        response = get_qa(query.frase_usuario)
        if response.get("mensaje"):
            return response
        else:
            raise HTTPException(status_code=404, detail="No se encontraron resultados")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la consulta: {e}")
    

class FilterModel(BaseModel):
    marca: Optional[str] = None
    sexo: Optional[str] = None
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

        # Filtrar Jugador
        if filtros.get('sexo'):
            jugador_seleccionado = filtros['sexo'].lower()
            
            # Si el jugador seleccionado es 'Hombre' o 'Mujer', también considerar las opciones 'Hombre, Mujer' y 'Mujer, Hombre'
            if jugador_seleccionado == 'hombre' and 'hombre' not in pala['Sexo'].lower() and 'hombre, mujer' not in pala['Sexo'].lower():
                continue
            if jugador_seleccionado == 'mujer' and 'mujer' not in pala['Sexo'].lower() and 'hombre, mujer' not in pala['Sexo'].lower():
                continue
            # Si el jugador seleccionado es 'Junior', solo se devuelven las palas que tengan 'Junior'
            if jugador_seleccionado == 'junior' and 'junior' not in pala['Sexo'].lower():
                continue


        # Filtro Balance 
        if filtros.get('balance'):
            balance_selected = filtros['balance'].lower()
            pala_balance = pala.get('Balance', '').lower()

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
        if filtros.get('dureza'):
            dureza_selected = filtros['dureza'].lower()
            pala_dureza = pala.get('Dureza', '').lower()

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
        if filtros.get('acabado'):
            acabado_selected = filtros['acabado'].lower()
            pala_acabado = pala.get('Acabado', '').lower()

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
        if filtros.get('superficie'):
            superficie_selected = filtros['superficie'].lower()
            pala_superficie = pala.get('Superfície', '').lower()

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
        if filtros.get('tipo_juego'):
            tipo_juego_selected = filtros['tipo_juego'].lower()
            pala_tipo_juego = pala.get('Tipo de juego', '').lower()

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


        # Filtro Nivel de Juego
        if filtros.get('nivel_juego'):
            nivel_juego_selected = filtros['nivel_juego'].lower()
            pala_nivel_juego = pala.get('Nivel de Juego', '').lower()

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
        if filtros.get('marca') and filtros['marca'] and filtros['marca'].lower() not in pala['Marca'].lower():
            continue

        # Filtro Forma
        if filtros.get('forma') and filtros['forma'] and filtros['forma'].lower() != pala.get('Forma', '').lower():
            continue

        # Filtro Colección Jugadores
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
            "Imagen": pala["Imagen"],
            "Enlace": pala["Enlace"],
            "Descripción": pala["Descripción"]
        })
    
    # Limitar el número de recomendaciones a 5
    recomendaciones = recomendaciones[:3]

    contexto = formatear_recomendaciones(recomendaciones)
    llm = ChatBedrock(model_id=LLM_MODEL_NAME, client=client)
    #print("CONTEXTO",contexto) #! Debug OK
    
    try:
        prompt_recommendations = prompt_template_recommendations.format(user_input=contexto, filters=filtros)
        #print("PROMPT RECOMMENDATIONS",prompt_recommendations) #! Debug OK
        respuesta = llm.invoke(prompt_recommendations)
        #print("Datos enviados al frontend:", respuesta.content + "\n" + "Recomendaciones:", recomendaciones) #! Debug OK
    
    except Exception as e:
        print("Error al generar recomendaciones:", e)
        respuesta = None
    
    return {
        #"recomendaciones": recomendaciones,
        "modelo_respuesta": respuesta.content if respuesta and respuesta.content else "No se puedo obtener una respuesta."
    }