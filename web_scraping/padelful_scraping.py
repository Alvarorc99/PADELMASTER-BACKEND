import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Listas para almacenar la información
marca = []
modelo = []
precio = []
enlace = []
temporada = []
potencia = []
control = []
rebote = []
manejo = []
punto_dulce = []
forma = []
peso = []
tacto = []
nucleo = []
caras = []
marco = []
contenido_completo = []

# Número total de páginas a procesar
total_paginas = 42

# Iterar a través de cada página
for page_number in range(1, total_paginas + 1):
    print(f"Procesando página {page_number}/{total_paginas}...")
    url = f"https://www.padelful.com/es/palas?page={page_number}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Encontrar todos los enlaces que contienen información de las palas
    palas = soup.find_all('a', class_="relative flex flex-col overflow-hidden rounded-lg p-4 hover:opacity-75 md:p-4 xl:w-auto h-80 w-full justify-self-center sm:h-96 lg:justify-self-auto border border-green-500 border-opacity-30")

    # Comprobar si se encontraron palas
    if not palas:
        print(f"No se encontraron palas en la página {page_number}.")
        continue  # Saltar a la siguiente página si no hay palas

    count_palas = 0

    # Procesar cada pala
    for pala in palas:
        # Extraer la marca y modelo
        marca_modelo_tag = pala.find('p', class_="relative font-mono text-sm font-semibold text-white md:text-base")
        modelo_tag = pala.find('h3', class_="relative font-bold text-white md:text-xl")
        
        if marca_modelo_tag and modelo_tag:
            # Extraer la marca y la temporada
            marca_text = marca_modelo_tag.text.strip()
            marca_parts = marca_text.split('/')
            marca_text = marca_parts[0].strip()  # Marca
            temporada_text = marca_parts[1].strip() if len(marca_parts) > 1 else "No disponible"  # Temporada
            
            marca.append(marca_text)
            temporada.append(temporada_text)  # Añadir temporada a la lista
            modelo.append(modelo_tag.text.strip())

            # Extraer el precio
            precio_tag = pala.find('span', class_="absolute left-2 top-14 rounded-md bg-transparent px-2 text-lg font-semibold text-neutral-700")
            if precio_tag:
                precio_text = precio_tag.text.strip()
                precio.append(precio_text)
            else:
                precio.append("No disponible")  # En caso de que no haya precio

            # Extraer el enlace
            enlace_text = pala['href']  # Obtener el atributo href del enlace
            enlace_completo = "https://www.padelful.com" + enlace_text  # Construir la URL completa
            enlace.append(enlace_completo)

            print(f"  Procesando pala: {modelo_tag.text.strip()}...")

            # Solicitar la página del enlace para extraer las características adicionales
            pala_page = requests.get(enlace_completo)
            pala_soup = BeautifulSoup(pala_page.content, 'html.parser')

            # Buscar el div que contiene la tabla con las características
            notas = pala_soup.find('div', class_="w-full rounded-lg bg-neutral-100 p-8")
            if notas:
                # Buscar la tabla dentro de este div
                table = notas.find('table', class_="mt-2 min-w-full divide-y divide-gray-300")
                if table:
                    # Extraer las filas de la tabla
                    rows = table.find('tbody', class_="divide-y divide-gray-200").find_all('tr')

                    # Inicializar valores para Potencia, Control, Rebote, Manejo y Punto dulce
                    potencia_val = control_val = rebote_val = manejo_val = punto_dulce_val = "No disponible"

                    for row in rows:
                        # Encontrar el nombre del atributo en la primera celda <td>
                        attribute_name = row.find('td', class_="whitespace-nowrap py-3.5 pl-4 pr-3 text-sm font-medium text-pista-900 sm:pl-0")
                        attribute_value = row.find('td', class_="whitespace-nowrap px-3 py-3.5 text-center text-sm font-medium text-pista-700")
                        
                        if attribute_name and attribute_value:
                            name = attribute_name.text.strip()
                            value = attribute_value.text.strip()

                            if name == 'Potencia':
                                potencia_val = value
                            elif name == 'Control':
                                control_val = value
                            elif name == 'Rebote':
                                rebote_val = value
                            elif name == 'Manejo':
                                manejo_val = value
                            elif name == 'Punto dulce':
                                punto_dulce_val = value

                    # Añadir los valores a las listas
                    potencia.append(potencia_val)
                    control.append(control_val)
                    rebote.append(rebote_val)
                    manejo.append(manejo_val)
                    punto_dulce.append(punto_dulce_val)
            
            # Características adicionales de la pala
            caracteristicas = pala_soup.find('div', class_="my-8 max-w-3xl")
            if caracteristicas:
                caracteristicas_div = caracteristicas.find_all('div', class_="bg-neutral-100 p-6")  # Obtener todas las características

                # Inicializar valores para Forma, Peso, Tacto, Núcleo, Caras y Marco
                forma_val = peso_val = tacto_val = nucleo_val = caras_val = marco_val = "No disponible"

                for row in caracteristicas_div:
                    caracteristica_name = row.find('p', class_="text-lg font-bold")
                    caracteristica_value = row.find('p', class_="text-sm")

                    if caracteristica_name and caracteristica_value:
                        name = caracteristica_name.text.strip()
                        value = caracteristica_value.text.strip()

                        if name == 'Forma':
                            forma_val = value
                        elif name == 'Peso':
                            peso_val = value
                        elif name == 'Tacto':
                            tacto_val = value
                        elif name == 'Núcleo':
                            nucleo_val = value
                        elif name == 'Caras':
                            caras_val = value
                        elif name == 'Marco':
                            marco_val = value

                # Añadir los valores a las listas correspondientes
                forma.append(forma_val)
                peso.append(peso_val)
                tacto.append(tacto_val)
                nucleo.append(nucleo_val)
                caras.append(caras_val)
                marco.append(marco_val)

            # Buscar el div que contiene el contenido
            contenido_div = pala_soup.find('div', class_="max-w-2xl prose")
            if contenido_div:
                js_toc_content = contenido_div.find('div', class_="js-toc-content")
                if js_toc_content:
                    # Extraer todo el texto del contenedor js-toc-content
                    text_content = ''.join([str(x) if isinstance(x, str) else x.text for x in js_toc_content.contents])
                    contenido_completo.append(text_content.strip())
                else:
                    contenido_completo.append("No disponible")
            else:
                contenido_completo.append("No disponible")
            count_palas += 1
    print(f"Página {page_number} procesada con éxito. Se procesaron {count_palas} palas.\n")
    time.sleep(2)

# Crear un DataFrame con los datos recopilados
df = pd.DataFrame({
    'Marca': marca,
    'Modelo': modelo,
    'Precio': precio,
    'Enlace': enlace,
    'Temporada': temporada,
    'Potencia': potencia,
    'Control': control,
    'Rebote': rebote,
    'Manejo': manejo,
    'Punto Dulce': punto_dulce,
    'Forma': forma,
    'Peso': peso,
    'Tacto': tacto,
    'Núcleo': nucleo,
    'Caras': caras,
    'Marco': marco,
    'Contenido Completo': contenido_completo  # Agregar la columna de contenido completo
})

# Guardar el DataFrame en un archivo Excel
df.to_excel('palas_padelful_con_caracteristicas.xlsx', index=False)

print("Proceso completado. Los datos han sido guardados en 'palas_padelful_con_caracteristicas.xlsx'.")
