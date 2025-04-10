import logging
import boto3
from dotenv import load_dotenv
import os
from pathlib import Path

dotenv_path = Path(__file__).resolve().parent.parent.parent / '.env'
# Cargar las variables de entorno desde el archivo .env
load_dotenv(dotenv_path)

# Obtener las claves de AWS desde las variables de entorno
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")

client = boto3.client(
    'bedrock-runtime',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("PADELMASTER")

# Verifica que las claves se han cargado correctamente
# if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_REGION and LLM_MODEL_NAME and EMBEDDING_MODEL_NAME:
#     print("Las claves de AWS se han cargado correctamente.")
#     print(f"AWS_ACCESS_KEY_ID: {AWS_ACCESS_KEY_ID}")
#     print(f"AWS_SECRET_ACCESS_KEY: {AWS_SECRET_ACCESS_KEY}")
#     print(f"AWS_REGION: {AWS_REGION}")
#     print(f"LLM_MODEL_NAME: {LLM_MODEL_NAME}")
#     print(f"EMBEDDING_MODEL_NAME: {EMBEDDING_MODEL_NAME}")
# else:
#     print("Error: No se pudieron cargar las claves de AWS.")
