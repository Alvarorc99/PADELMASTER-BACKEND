import pandas as pd

# Leer el archivo Excel
df = pd.read_excel("C:/Users/alvar/TFG/PADELMASTER BACKEND/dataset_padel_nuestro/palas_padelnuestro_actualizado/palas_padelnuestro_actualizado.xlsx", engine = "openpyxl")

# Guardar como CSV
df.to_csv("C:/Users/alvar/TFG/PADELMASTER BACKEND/dataset_padel_nuestro/palas_padelnuestro_actualizado/palas_padelnuestro_actualizado.csv", index=False, encoding="utf-8")  
