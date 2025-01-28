"""This file generates and saves a FAISS index for a database of documents in JSON format."""

from venv import logger
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.vectorstores import FAISS
import pandas as pd
import os

def generar_guardar_indice_faiss(archivoJSON, rutaIndice):
    logger.info(f"Inizializing the generation of the FAISS index from the dataset '{archivoJSON}'.")
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_model = HuggingFaceEmbeddings(model_name=model_name)

    df = pd.read_json(archivoJSON)
    logger.info(f"Dataset loaded from '{archivoJSON}' with {len(df)} rows.")

    logger.info(f"Generating embeddings for the documents...")
    documents = []
    for _, row in df.iterrows():
        content = (
            f"Nombre: {row['Nombre']}, Marca: {row['Marca']}, Sexo: {row['Sexo']}, "
            f"Nivel de juego: {row['Nivel de juego']}, Tipo de juego: {row['Tipo de juego']}, "
            f"Forma: {row['Forma']}, Balance: {row['Balance']}, Dureza: {row['Dureza']}, "
            f"Precio: {row['Precio']} €, Superficie: {row['Superficie']}, "
            f"Enlace: {row['Enlace']}, Imagen: {row['Imagen']}, Descripción: {row['Descripción']}"
        )

        metadata = row.to_dict()
        metadata["Nombre"] = metadata["Nombre"].strip().lower()
        doc = Document(page_content=content, metadata=metadata)
        documents.append(doc)

    logger.info(f"Generated {len(documents)} documents.")

    logger.debug(f"Example of document: {documents[0]}")
    
    logger.info("Generating embeddings...")
    embeddings = embedding_model.embed_documents([doc.page_content for doc in documents])
    
    logger.info("Creating FAISS index...")
    vector_store = FAISS.from_documents(documents, embedding_model)

    try:
        os.makedirs(os.path.dirname(rutaIndice), exist_ok=True)
        vector_store.save_local(rutaIndice)
        logger.info(f"Index saved to '{rutaIndice}'.")

    except Exception as e:
        logger.error(f"Error saving the index to '{rutaIndice}': {e}")

# Ruta al dataset y ubicación para guardar el índice
archivoJSON = "C:/Users/alvar/TFG/PADELMASTER BACKEND/dataset_padel_nuestro/palas_padelnuestro_actualizado/palas_padelnuestro_actualizado.json"
rutaIndice = "C:/Users/alvar/TFG/PADELMASTER BACKEND/faiss/faiss_index"

# Generar y guardar el índice FAISS
generar_guardar_indice_faiss(archivoJSON, rutaIndice)
