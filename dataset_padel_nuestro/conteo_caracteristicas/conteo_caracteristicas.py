"""File to analyze the dataset and extract the number of unique values for each characteristic"""

import pandas as pd
from src.config.config import *

file_path = DATASET_PATH
df = pd.read_json(file_path)

caracteristicas_a_contar = [
    "Balance", "Cara", "Dureza", "Acabado", 
    "Forma", "Superficie", "Sexo", 
    "Tipo de juego", "Nivel de juego",
    "Marca", "Jugador profesional", 
    "Núcleo", "Precio"
]

def contar_valores_unicos(df, columnas):
    for columna in columnas:
        if columna in df.columns:
            conteo = df[columna].value_counts(dropna=True)
            print(f"Característica: {columna}")
            for valor, cantidad in conteo.items():
                print(f"  - {valor}: {cantidad}")
            print("\n")
        else:
            print(f"La columna '{columna}' no existe en el dataset.\n")

contar_valores_unicos(df, caracteristicas_a_contar)
