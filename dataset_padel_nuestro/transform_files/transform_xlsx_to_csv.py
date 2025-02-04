import pandas as pd
from src.config.config import *

# Leer el archivo Excel
df = pd.read_excel(DATASET_XLSX_PATH, engine = "openpyxl")

# Guardar como CSV
df.to_csv(DATASET_CSV_PATH, index=False, encoding="utf-8")  
