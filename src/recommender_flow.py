
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
# Función para recoger las entradas del usuario
def recolectar_preferencias():
    marca_preferida = input("(Opcional, separa por comas) ¿Tienes marcas preferidas? (Bullpadel/Nox/Siux/Adidas...): ").split(',')
    preferencias = {
        'Marca': marca_preferida or None
    }
    
    return preferencias
# Función para filtrar resultados por marcas y precio máximo
def filtrar_resultados(resultados, preferencias):
    resultados_filtrados = []
    for result in resultados:
        marca = result.metadata.get('Marca', '').lower()
        # Mostrar información para depuración
        print(f"Procesando pala: {result.metadata.get('Nombre')}")
        # Filtro por marcas y precio
        if (not preferencias['Marca'] or any(marca in m.lower() for m in preferencias['Marca'])):
            resultados_filtrados.append(result)
    return resultados_filtrados
# Función principal para cargar el índice FAISS y recomendar palas
def recomendar_palas(ruta_indice):
    preferencias = recolectar_preferencias()
    # Inicializar el modelo de embeddings
    model_name = "sentence-transformers/all-MiniLm-L6-v2"
    embedding_model = HuggingFaceEmbeddings(model_name=model_name)
    # Cargar el índice FAISS
    vector_store = FAISS.load_local(ruta_indice, embedding_model, allow_dangerous_deserialization=True)
    # Construcción de la consulta de búsqueda basada en preferencias obligatorias
    consulta = (
        f"Marca: {preferencias['Marca']}"
    )
    # Realizar búsqueda por similitud
    resultados = vector_store.similarity_search(consulta, k=100)
    # Aplicar filtros estrictos para marcas y precio máximo
    resultados_filtrados = filtrar_resultados(resultados, preferencias)
    if resultados_filtrados:
        print("\nRecomendaciones de palas basadas en tus preferencias:")
        for i, result in enumerate(resultados_filtrados[:100], 1):
            print(f"\nResultado {i}:")
            print(f"Nombre: {result.metadata.get('Nombre')}")
            print(f"Marca: {result.metadata.get('Marca')}")
            print(f"Precio: {result.metadata.get('Precio')}")
            print(f"Descripción: {result.metadata.get('Descripción')[:200]}...")
    else:
        print("No se encontraron palas que cumplan con tus criterios.")
# Ruta al índice FAISS
ruta_indice = "C:/Users/alvar/TFG/chatbot_aws/faiss/faiss_index"
recomendar_palas(ruta_indice)
