"Archivo de ejemplo para usar el índice FAISS (funciona medianamente correcto)"

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

def cargar_indice_faiss_y_consultar(rutaIndice, consulta):
    # Inicializar el modelo de embeddings
    model_name = "sentence-transformers/all-MiniLm-L6-v2"
    embedding_model = HuggingFaceEmbeddings(model_name=model_name)

    # Cargar el índice FAISS
    print("Cargando índice FAISS desde disco...")
    vector_store = FAISS.load_local(rutaIndice, embedding_model, allow_dangerous_deserialization=True)

    # Realizar la consulta y generar el embedding de la consulta
    print("Realizando búsqueda por similitud...")
    #query_embedding = embedding_model.embed_query(consulta)
    results = vector_store.similarity_search(consulta, k=5)

    # Mostrar los resultados
    for i, result in enumerate(results, 1):
        print(f"\nResultado {i}:")
        print(f"Nombre de la pala: {result.metadata.get('Nombre')}")
        print(f"Texto relevante: {result.page_content}")
        print(f"Metadatos: {result.metadata}")

# Ruta al índice y consulta de ejemplo
rutaIndice = "C:/Users/alvar/TFG/chatbot_aws/faiss/faiss_index"
consulta = "DUNLOP INFERNO GOLD"

# Cargar el índice y realizar la consulta
cargar_indice_faiss_y_consultar(rutaIndice, consulta)
