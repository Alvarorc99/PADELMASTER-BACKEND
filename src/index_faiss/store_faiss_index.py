"""Este archivo genera y guarda un índice FAISS para una base de datos de documentos en formato JSON."""

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.vectorstores import FAISS
import pandas as pd
import os

def generar_guardar_indice_faiss(archivoJSON, rutaIndice):
    # Inicializar el modelo de embeddings
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_model = HuggingFaceEmbeddings(model_name=model_name)

    # Cargar el dataset
    df = pd.read_json(archivoJSON)

    # Crear documentos y generar embeddings
    print("Generando documentos y embeddings...")
    documents = []
    for _, row in df.iterrows():
        content = (
            f"Nombre: {row['Nombre']}, Marca: {row['Marca']}, Jugador: {row['Jugador']}, "
            f"Nivel de Juego: {row['Nivel de Juego']}, Tipo de juego: {row['Tipo de juego']}, "
            f"Forma: {row['Forma']}, Balance: {row['Balance']}, Dureza: {row['Dureza']}, "
            f"Precio: {row['Precio']} €, Formato: {row['Formato']}, Superficie: {row['Superfície']}, "
            f"Descripción: {row['Descripción']}"
        )

        metadata = row.to_dict()
        doc = Document(page_content=content, metadata=metadata)
        documents.append(doc)

    # Verificar cantidad de documentos creados
    print(f"Cantidad de documentos generados: {len(documents)}")

    # Ejemplo de documento
    print("Ejemplo de documento:")
    print(documents[0])
    
    # Generar embeddings para los documentos
    print("Generando embeddings para los documentos...")
    embeddings = embedding_model.embed_documents([doc.page_content for doc in documents])
    
    # Crear el índice FAISS
    print("Creando índice FAISS...")
    vector_store = FAISS.from_documents(documents, embedding_model)

    # Guardar el índice FAISS en disco
    try:
        os.makedirs(os.path.dirname(rutaIndice), exist_ok=True)
        vector_store.save_local(rutaIndice)
        print(f"Índice FAISS guardado en: {rutaIndice}")

    except Exception as e:
        print(f"Error al guardar el índice FAISS: {e}")

# Ruta al dataset y ubicación para guardar el índice
archivoJSON = "C:/Users/alvar/TFG/chatbot_aws/dataset_padel_nuestro/palas_padelnuestro.json"
rutaIndice = "C:/Users/alvar/TFG/chatbot_aws/faiss/faiss_index"

# Generar y guardar el índice FAISS
generar_guardar_indice_faiss(archivoJSON, rutaIndice)
