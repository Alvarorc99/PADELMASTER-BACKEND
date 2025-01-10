import pandas as pd

# Leer el archivo Excel
df = pd.read_excel("C:/Users/alvar/TFG/chatbot-padel/datasets/dataset_padel_nuestro/palas_padelnuestro.xlsx", engine = "openpyxl")

# Guardar como CSV
df.to_csv("C:/Users/alvar/TFG/chatbot-padel/datasets/dataset_padel_nuestro/palas_padelnuestro.csv", index=False, encoding="utf-8")  
