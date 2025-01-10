import pandas as pd
import json

# Cargar el dataset limpio desde el CSV
df = pd.read_csv("C:/Users/alvar/TFG/chatbot-padel/Datasets padelful/palas_padelful.csv")

# Convertir cada fila en un documento JSON
documentos = []
for _, row in df.iterrows():
    documento = {
        "Marca": row["Marca"],
        "Modelo": row["Modelo"],
        "Precio": row["Precio"],
        "Enlace": row["Enlace"],
        "Temporada": row["Temporada"],
        "Potencia": row["Potencia"],
        "Control": row["Control"],
        "Rebote": row["Rebote"],
        "Manejo": row["Manejo"],
        "Punto Dulce": row["Punto Dulce"],
        "Forma": row["Forma"],
        "Peso": row["Peso"],
        "Tacto": row["Tacto"],
        "Núcleo": row["Núcleo"],
        "Caras": row["Caras"],
        "Marco": row["Marco"],
        "Contenido Completo": row["Contenido Completo"]
    }
    documentos.append(documento)

# Guardar en formato JSON
with open("C:/Users/alvar/TFG/chatbot-padel/Datasets padelful/palas_padelful.json", "w", encoding="utf-8") as f:
    json.dump(documentos, f, ensure_ascii=False, indent=4)

print("Archivo JSON documental creado exitosamente.")
