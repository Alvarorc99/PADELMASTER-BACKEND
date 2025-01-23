import pandas as pd

# Cargar el dataset
file_path = "C:/Users/alvar/TFG/PADELMASTER BACKEND/dataset_padel_nuestro/palas_padelnuestro_actualizado/palas_padelnuestro_actualizado.json"
df = pd.read_json(file_path)

# Características a analizar
caracteristicas_a_contar = [
    "Balance", "Cara", "Dureza", "Acabado", 
    "Forma", "Superficie", "Sexo", 
    "Tipo de juego", "Nivel de juego",
    "Marca", "Jugador profesional", 
    "Núcleo", "Formato", "Precio"
]

# Contar valores únicos por característica seleccionada
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

# Ejecutar el conteo
contar_valores_unicos(df, caracteristicas_a_contar)
