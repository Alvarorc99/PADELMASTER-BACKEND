import pandas as pd
import json

# Cargar el dataset limpio desde el CSV
df = pd.read_csv("C:/Users/alvar/TFG/chatbot-padel/datasets/dataset_padel_nuestro/palas_padelnuestro.csv")

# Convertir cada fila en un documento JSON
documentos = []
for _, row in df.iterrows():
    documento = {
        "Nombre": row["Nombre"],
        "Marca": row["Marca"],
        "Precio": row["Precio"],
        "Color": row["Color"],
        "Balance": row["Balance"],
        "Núcleo": row["Núcleo"],
        "Cara": row["Cara"],
        "Formato": row["Formato"],
        "Dureza": row["Dureza"],
        "Acabado": row["Acabado"],
        "Forma": row["Forma"],
        "Superfície": row["Superfície"],
        "Jugador": row["Jugador"],
        "Tipo de juego": row["Tipo de juego"],
        "Nivel de Juego": row["Nivel de Juego"],
        "Colección Jugadores": row["Colección Jugadores"],
        "Descripción": row["Descripción"],
    }
    documentos.append(documento)

# Guardar en formato JSON
with open("C:/Users/alvar/TFG/chatbot-padel/datasets/dataset_padel_nuestro/palas_padelnuestro.json", "w", encoding="utf-8") as f:
    json.dump(documentos, f, ensure_ascii=False, indent=4)

print("Archivo JSON documental creado exitosamente.")
