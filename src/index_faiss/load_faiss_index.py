""" Este archivo carga el índice FAISS desde disco"""

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

def cargar_indice_faiss_y_consultar(rutaIndice):
    # Inicializar el modelo de embeddings
    model_name = "sentence-transformers/all-MiniLm-L6-v2"
    embedding_model = HuggingFaceEmbeddings(model_name=model_name)

    # Cargar el índice FAISS
    print("Cargando índice FAISS desde disco...")
    vector_store = FAISS.load_local(rutaIndice, embedding_model, allow_dangerous_deserialization=True)
    
    return vector_store