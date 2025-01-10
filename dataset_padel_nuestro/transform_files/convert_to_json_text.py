import pandas as pd
import json

# Cargar el archivo CSV
df = pd.read_csv("C:/Users/alvar/TFG/chatbot-padel/Datasets padelful/palas_padelful.csv")

# Esto convierte cada valor de texto a minúsculas y elimina espacios en blanco
# for col in df.columns:
#     if df[col].dtype == "object" and col != "Enlace a la pala en padelful":
#         df[col] = df[col].str.lower().str.strip()

# Crear lista de documentos en formato JSON
documentos = []
for _, row in df.iterrows():
    # Crear un bloque de texto con toda la información relevante de cada pala
    texto = (
        f"La pala {row['Marca']} {row['Modelo']} de la temporada {row['Temporada']} "
        f"tiene un precio de {row['Precio']} euros. Posee una potencia de {row['Potencia']} "
        f"y un control de {row['Control']}. Su rebote es de {row['Rebote']}, manejo de {row['Manejo']}, "
        f"y punto dulce de {row['Punto Dulce']}. Esta pala tiene una forma {row['Forma']} y un peso de {row['Peso']}. "
        f"Su tacto es {row['Tacto']}, con un núcleo de {row['Núcleo']}, caras de {row['Caras']} y marco de {row['Marco']}. "
        f"Para más detalles, consulta el enlace: {row['Enlace']}. "
        f"Descripción completa: {row['Contenido Completo']}"
    )
    documentos.append({"documento": texto})

# Guardar en un archivo JSON con codificación UTF-8
with open("dataset_padel_documentos.json", "w", encoding="utf-8") as file:
    json.dump(documentos, file, ensure_ascii=False, indent=4)
