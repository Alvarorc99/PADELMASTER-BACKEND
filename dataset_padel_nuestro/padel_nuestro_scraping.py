import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

pd.set_option('display.max_colwidth', None)  # Para visualizar el contenido completo

# Función para extraer productos de una página
def obtener_productos(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # Buscamos todos los elementos que contienen las palas
    palas = soup.find_all('div', class_='product-item-info')
    return palas

# Función para extraer las características de cada pala desde su página de detalles
def obtener_caracteristicas_detalladas(enlace):
    try:
        product_page = requests.get(enlace)
        soup = BeautifulSoup(product_page.content, 'html.parser')
        
        # Contenedor principal de las características
        contenedor = soup.find('div', class_='product data items mage-tabs-disabled')
        if not contenedor:
            return {}

        # Extraer las características desde las etiquetas <span>
        caracteristicas = {}
        atributos = contenedor.find_all('div', class_='description-attributes')
        for atributo in atributos:
            etiqueta = atributo.find('span', class_='description-attributes-label')
            valor = atributo.find('span', class_='description-attributes-value')
            if etiqueta and valor:
                caracteristicas[etiqueta.text.strip()] = valor.text.strip()

        return caracteristicas

    except Exception as e:
        print(f"Error obteniendo características de {enlace}: {e}")
        return {}

# Función para extraer las características de cada pala
def obtener_caracteristicas_pala(pala):
    # Enlace a la pala
    enlace_tag = pala.find('a')
    enlace = enlace_tag['href'] if enlace_tag else None

    # Extraer características detalladas si hay un enlace
    caracteristicas_detalladas = obtener_caracteristicas_detalladas(enlace) if enlace else {}
    
    # Marca
    marca_tag = pala.find('span')
    marca = marca_tag.text.strip() if marca_tag else None

    # Año
    ano_tag = pala.find('span')
    ano = ano_tag.text.strip() if ano_tag else None

    # Modelo
    modelo_tag = pala.find('h3')
    modelo = modelo_tag.text.strip() if modelo_tag else None

    # Precio
    precio_tag = pala.find('span', class_='relative')
    precio = precio_tag.text.strip() if precio_tag else 'No disponible'

    ###########################
    # Descripción (extraída según el HTML especificado)
    descripcion = None
    if enlace:  # Si tenemos un enlace, intentamos acceder a la página del producto
        try:
            product_page = requests.get(enlace)
            product_soup = BeautifulSoup(product_page.content, 'html.parser')
            descripcion_tag = product_soup.find('div', class_='product attribute description')
            if descripcion_tag:
                value_tag = descripcion_tag.find('div', class_='value')
                descripcion = value_tag.text.strip() if value_tag else None
        except Exception as e:
            print(f"Error obteniendo la descripción de {enlace}: {e}")
    
    return {
        'Enlace': enlace,
        'Marca': marca,
        'Año': ano,
        'Modelo': modelo,
        'Precio': precio,
        'Descripción': descripcion
    }

# URL base
base_url = "https://www.padelnuestro.com/palas-padel?_gl=1%2A1jxvsfi%2A_up%2AMQ..%2A_gs%2AMQ..&p="

# Listas para almacenar la información
palas_data = []

# Iterar sobre las páginas
num_paginas = 37
for pagina in range(1, num_paginas + 1):
    url = f"{base_url}{pagina}"
    print(f"Obteniendo productos de {url}...")

    productos = obtener_productos(url)
    print(f"Número de productos encontrados en la página {pagina}: {len(productos)}")

    # Procesar cada producto
    for producto in productos:
        caracteristicas = obtener_caracteristicas_pala(producto)
        palas_data.append(caracteristicas)

    time.sleep(1)  # Respetar el servidor con un retraso entre solicitudes

# Crear un DataFrame con los datos recopilados
df = pd.DataFrame(palas_data)

# Guardar el DataFrame en un archivo Excel
df.to_excel('C:/Users/alvar/TFG/chatbot-padel/datasets/palas_padelful.xlsx', index=False)

# Mostrar el DataFrame final
print(df)
