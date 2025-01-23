import os
import re
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup


# Inicializar las listas con un valor por defecto
marca = []
color = []
balance = []
nucleo = []
cara = []
formato = []
nivel_juego = []
acabado = []
forma = []
dureza = []
superficie = []
tipo_juego = []
jugador = []
coleccion_jugador = []
nombre_pala = []
precio = []
descripcion = []
enlaces = []
imagen = []

# Número total de páginas a procesar
total_paginas = 40

# Iterar a través de cada página
for page_number in range(1, total_paginas + 1):
    print(f"Procesando página {page_number}/{total_paginas}...")
    url = f"https://www.padelnuestro.com/palas-padel?_gl=1%2A1jxvsfi%2A_up%2AMQ..%2A_gs%2AMQ..&p={page_number}"  # Incluir el número de página
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Encontrar todos los enlaces que contienen información de las palas
    palas = soup.find_all('a', class_='product-label label-bottom')

    # Comprobar si se encontraron palas
    if not palas:
        print(f"No se encontraron palas en la página {page_number}.")
        continue  # Saltar a la siguiente página si no hay palas

    # Extraer los enlaces de cada pala
    for pala in palas:
        enlace = pala['href']
        enlaces.append(enlace)
    
    time.sleep(1)  # Esperar 1 segundo entre solicitudes

print(f"Se encontraron {len(enlaces)} enlaces de palas.")


# Función para extraer características de cada pala
def obtener_caracteristicas_pala(enlace):
    # Asegurarse de que el enlace comienza con "https://"
    if not enlace.startswith('http'):
        url_pala = f"https://www.padelnuestro.com{enlace}"  # Completar la URL con el enlace de la pala
    else:
        url_pala = enlace  # Si ya tiene "https://", usar la URL completa

    print(f"Procesando pala: {url_pala}...") 
    page = requests.get(url_pala)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Encontrar el contenedor de las características
    container = soup.find_all('div', class_='description-attributes')

    # Inicializar los valores con valores predeterminados (vacío o None)
    current_marca = current_color = current_balance = current_nucleo = current_caras = current_formato = ""
    current_nivel_juego = current_acabado = current_forma = current_superficie = current_dureza = ""
    current_tipo_juego = current_jugador = current_coleccion_jugador = ""
    current_descripcion = current_nombre = current_precio = current_imagen_url =""

    # Asegurarse de que el contenedor fue encontrado
    if container:
        # Iterar sobre cada contenedor de atributos
        for attribute in container:
            # Buscar el nombre del atributo
            label = attribute.find('span', class_='description-attributes-label')
            # Buscar el valor del atributo
            value = attribute.find('span', class_='description-attributes-value')

            if label and value:
                label_text = label.text.strip()
                value_text = value.text.strip()

                # Asignar los valores a las variables correspondientes según el nombre del atributo
                if 'Marca' in label_text:
                    current_marca = value_text
                elif 'Color' in label_text:
                    current_color = value_text
                elif 'Balance' in label_text:
                    current_balance = value_text
                elif 'Núcleo' in label_text:
                    current_nucleo = value_text
                elif 'Cara' in label_text:
                    current_caras = value_text
                elif 'Formato' in label_text:
                    current_formato = value_text
                elif 'Nivel de juego' in label_text:
                    current_nivel_juego = value_text
                elif 'Acabado' in label_text:
                    current_acabado = value_text
                elif 'Forma' in label_text:
                    current_forma = value_text
                elif 'Superficie' in label_text:
                    current_superficie = value_text
                elif 'Tipo de Juego' in label_text:
                    current_tipo_juego = value_text
                elif 'Jugador profesional' in label_text:
                    current_coleccion_jugador = value_text
                elif 'Jugador' in label_text:
                    current_jugador = value_text
                elif 'Dureza' in label_text:
                    current_dureza = value_text

    # Descripción (extraída según el HTML especificado)
    descripcion_tag = soup.find('div', class_='product attribute description')
    if descripcion_tag:
        current_descripcion = descripcion_tag.text.strip()  # Extraemos todo el texto dentro del contenedor 'value'
    
    # Nombre de la pala (extraído desde el <span> con clase 'base')
    nombre_tag = soup.find('span', class_='base')
    if nombre_tag:
        current_nombre = nombre_tag.text.strip()

    # Precio de la pala (extraído desde el <span> con clase 'price')
    precio_tag = soup.find('span', class_='price')
    if precio_tag:
        current_precio = precio_tag.text.strip()
    
    # Imagen de la pala (extraído desde el <img> con clase 'product-image')
    match = re.search(r'https://www\.padelnuestro\.com/media/catalog/product/[\w\-\_/.]+', page.text)
    if match:
        current_imagen_url = match.group(0)  # Usar group(0) para la URL completa
    
        
    # Añadir los valores de cada pala a las listas
    marca.append(current_marca)
    color.append(current_color)
    balance.append(current_balance)
    nucleo.append(current_nucleo)
    cara.append(current_caras)
    formato.append(current_formato)
    nivel_juego.append(current_nivel_juego)
    acabado.append(current_acabado)
    forma.append(current_forma)
    superficie.append(current_superficie)
    tipo_juego.append(current_tipo_juego)
    jugador.append(current_jugador)
    coleccion_jugador.append(current_coleccion_jugador)
    descripcion.append(current_descripcion)
    nombre_pala.append(current_nombre)
    precio.append(current_precio)
    dureza.append(current_dureza)
    imagen.append(current_imagen_url)

    time.sleep(1)  # Esperar 1 segundo entre solicitudes para evitar sobrecargar el servidor
    print(f"Pala {nombre_pala} procesada con éxito.\n")

# Extraer las características de cada pala
for enlace in enlaces:
    obtener_caracteristicas_pala(enlace)

# Crear el DataFrame con los datos extraídos
df = pd.DataFrame({
    'Nombre': nombre_pala, 
    'Marca': marca,
    'Precio': precio,
    'Color': color,
    'Balance': balance,
    'Núcleo': nucleo,
    'Cara': cara,
    'Formato': formato,
    'Dureza': dureza,
    'Acabado': acabado,
    'Forma': forma,
    'Superficie': superficie,
    'Jugador': jugador,
    'Tipo de juego': tipo_juego,
    'Nivel de juego': nivel_juego,
    'Jugador profesional': coleccion_jugador,
    'Enlace': enlaces,
    'Imagen': imagen,
    'Descripción': descripcion,
})

# Guardar el DataFrame en un archivo Excel
df.to_excel('C:/Users/alvar/TFG/PADELMASTER BACKEND/dataset_padel_nuestro/palas_padelnuestro_actualizado.xlsx', index=False)

# Mostrar el DataFrame final
print("Datos de las palas guardados exitosamente en 'palas_padelnuestro_actualizado.xlsx'.")