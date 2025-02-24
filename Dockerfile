# Usa una imagen base de Python
FROM python:3.9.13

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /backend

# Copia los archivos del backend al contenedor
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Crea un volumen para persistir FAISS
VOLUME ["/backend/faiss_data"]

# Expone el puerto de FastAPI
EXPOSE 8000

# Comando para ejecutar FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
