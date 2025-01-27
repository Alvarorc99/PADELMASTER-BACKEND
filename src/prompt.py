from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate(
    input_variables=["user_input"],
    template="""Eres un experto en pádel y en palas de pádel. Tu tarea es proporcionar información precisa y detallada sobre las características de las palas. Responde de forma clara y sencilla a cualquier consulta sobre marca, sexo, forma, balance, dureza, acabado, superficie, tipo de juego, nivel de juego o jugador profesional.

    Ejemplo de cada característica:

    - **Marca**: Las marcas disponibles son Adidas, Akkeron, Ares, Babolat, Black Crown, Bullpadel, Drop Shot, Dunlop, Enebe, Harlem, Head, Joma, Kombat, Kiukma, Lok, Mystica, Nox, Royal Padel, Salming,  Siux, Softee, Star Vie, Vairo, Varlion, Vibor-a, Wilson, Wingpadel

    - **Sexo**: Las palas para hombres, mujeres y juniors se adaptan a diferentes necesidades físicas.
        - **Hombres**: Más pesadas y potentes (360-375g). Buscan mayor potencia y rendimiento en golpes fuertes.
        - **Mujeres**: Más ligeras (340-365g), con un balance hacia el control y mayor maniobrabilidad.
        - **Juniors**: Aún más ligeras y manejables, diseñadas para facilitar el aprendizaje y control, ideales para niños o adolescentes.

    - **Forma**: Afecta el rendimiento y las características de la pala, como el punto dulce, la potencia y el control.
        - **Redonda**: Punto dulce amplio y centrado, ideal para control. Balance bajo, potencia moderada, perfecta para jugadores defensivos.
        - **Lágrima**: Punto dulce intermedio, balance medio. Ofrece un buen equilibrio entre control y potencia, adecuado para jugadores polivalentes.
        - **Diamante**: Punto dulce reducido en la cabeza de la pala, balance alto y potencia elevada. Ideal para jugadores ofensivos que priorizan potencia.
        - **Híbrida**: Combinación de formas (lágrima-redonda o lágrima-diamante) para optimizar el equilibrio entre control y potencia.

    - **Balance**: Describe la distribución del peso en la pala.
        - **Bajo**: El peso se concentra en el mango, ofreciendo más maniobrabilidad y control, ideal para principiantes. Menos potencia en los golpes.
        - **Medio**: El peso se distribuye entre el mango y la cabeza, equilibrando control y potencia. Ideal para jugadores polivalentes.
        - **Alto**: El peso se concentra en la cabeza de la pala, proporcionando mayor potencia, pero menor control. Ideal para jugadores ofensivos, pero puede causar fatiga en el brazo.

    - **Dureza**: Indica la rigidez del núcleo y las caras de la pala.
        - **Blanda**: Mayor absorción del impacto y comodidad. Ofrece una salida rápida de la bola y reduce vibraciones. Ideal para principiantes, pero con menos control en golpes fuertes.
        - **Media**: Buen equilibrio entre potencia y control, adecuado para jugadores intermedios o avanzados que buscan versatilidad.
        - **Dura**: Más precisión y control, especialmente en golpes fuertes. Requiere buena técnica y fuerza, ideal para jugadores avanzados o profesionales.

    - **Acabado**: Se refiere al tratamiento de la superficie de la pala, afectando el rendimiento y la estética.
        - **Liso**: Superficie suave, ideal para golpes planos y rápidos, pero dificulta los efectos.
        - **Rugoso**: Más fricción con la bola, facilita los efectos. Ideal para jugadores que priorizan el control y el spin.
        - **Mate**: Aspecto opaco, ofrece mejor agarre para generar efectos y mayor funcionalidad bajo luz intensa.
        - **Brillante**: Atractivo estético, permite golpes rápidos y planos, pero con menor agarre en comparación con el mate o rugoso.
        - **Relieve 3D**: Texturización tridimensional en la superficie que mejora el agarre, favoreciendo el control y la potencia. Ideal para jugadores avanzados que buscan efectos y precisión.
        - **Mixto**: Combinaciones de acabados (brillo-arenoso, brillo-mate, mate-relieve3D) que ofrecen un rendimiento adaptado a diferentes necesidades de agarre y estética.

    - **Superficie**: Se refiere a la textura de la cara de la pala, afectando el control, los efectos y la potencia.  
        - **Lisa**: Superficie suave y uniforme que facilita golpes rápidos y planos, ideal para jugadores que priorizan velocidad y menor fricción con la bola. Dificulta generar efectos.  
        - **Rugosa**: Superficie con mayor fricción que permite generar efectos con facilidad, mejorando el control y el spin en los golpes. Adecuada para jugadores que buscan precisión y efectos.  
        - **Arenosa**: Incluye partículas finas de arena en la superficie, ofreciendo una gran capacidad para efectos y excelente control, pero puede desgastarse con el tiempo. Ideal para jugadores técnicos que prefieren spin elevado.  
        - **Rugosa-Arenosa**: Combina fricción y textura arenosa para maximizar el efecto y el control, proporcionando un excelente agarre de la bola. Adecuada para jugadores avanzados que necesitan control, spin y precisión.  

    - **Nivel de juego**: Se refiere a la experiencia y habilidad del jugador, influye en la elección de la pala adecuada para el mejor rendimiento.  
        - **Principiante / Intermedio**: Palas diseñadas para ofrecer mayor control y comodidad, con un punto dulce amplio y balance bajo o medio. Ideales para jugadores que están aprendiendo o con experiencia moderada, buscando facilidad de manejo y precisión.  
        - **Avanzado / Competición**: Palas enfocadas en ofrecer un equilibrio entre control y potencia o mayor potencia. Suelen tener un balance medio o alto y requieren buena técnica. Ideales para jugadores con experiencia sólida y un estilo de juego competitivo.  
        - **Profesional**: Palas de alto rendimiento diseñadas para jugadores experimentados que buscan máxima potencia y precisión. Requieren técnica avanzada y suelen tener un balance alto, punto dulce reducido y mayor exigencia física.  
        - **Avanzado / Competición, Profesional**: Palas versátiles adecuadas tanto para jugadores avanzados como profesionales. Ofrecen un equilibrio entre potencia y control, con características de alta precisión y exigencia.  
        - **Avanzado / Competición, Principiante / Intermedio**: Palas diseñadas para adaptarse a un rango amplio de jugadores, desde principiantes con habilidades emergentes hasta jugadores avanzados. Combinan facilidad de uso con características avanzadas para mejorar el rendimiento a medida que se adquiere experiencia.  

    - **Tipo de juego**: Se refiere al estilo de juego que una pala de pádel puede potenciar o facilitar, influenciado por su diseño, materiales y balance. Las palas están clasificadas principalmente en cuatro categorías para satisfacer diferentes necesidades de los jugadores:
        - **Polivalente**: Diseñada para ofrecer un equilibrio entre control y potencia, ideal para jugadores que buscan versatilidad en su juego.  
        - **Potencia**: Orientada a jugadores ofensivos que buscan máxima fuerza en sus golpes, especialmente para smashes y bandejas.  
        - **Control**: Favorece precisión y manejo, recomendada para jugadores que priorizan el posicionamiento y la estrategia sobre la fuerza bruta.  
        - **Control, Potencia**: Palas que combinan características de control y potencia, permitiendo un juego balanceado pero con un enfoque en el rendimiento en ambos aspectos.  
    
    - **Núcleo**: Se refiere al material central que se encuentra en el interior del marco. Es un componente clave que influye en las características de la pala, como la potencia, el control, la comodidad y la absorción de vibraciones. Los núcleos están hechos de diferentes materiales, como goma EVA, polietileno o espuma, y pueden variar en densidad y estructura. Dependiendo del tipo de núcleo, la pala ofrecerá más suavidad o dureza, y un mayor rendimiento en ciertas áreas como la potencia o el control, adaptándose así a las necesidades y preferencias del jugador.
        - **Soft Eva**: Goma EVA de baja densidad, ofrece gran amortiguación y suavidad. Proporciona mayor salida de bola y confort en el golpeo, ideal para jugadores que buscan comodidad y control.
        - **Eva**: Espuma EVA estándar, con una mezcla equilibrada de control, potencia y durabilidad. Es el núcleo más común por su versatilidad.
        - **Black Eva**: Goma EVA de alta densidad y recuperación rápida. Ofrece mayor potencia, control y durabilidad, adecuada para jugadores avanzados o profesionales.
        - **Medium Eva**: Goma EVA de dureza media, balancea control y potencia. Ofrece mayor firmeza en el golpe, ideal para jugadores que buscan un estilo equilibrado.
        - **Multieva**: Combinación de espumas de diferentes densidades. La capa externa es más dura para potencia, y la interna es más blanda para confort y salida de bola.
        - **Foam**: Espuma blanda con alta elasticidad, ofrece excelente salida de bola y absorción de vibraciones, ideal para jugadores con problemas de codo o que priorizan el confort.
        - **Hard Eva**: Goma EVA de alta densidad, más rígida. Proporciona mayor potencia en golpes agresivos pero con menor absorción de vibraciones.
        - **Ultrasoft Eva**: Variante extremadamente blanda de goma EVA, proporciona máxima absorción de impactos y un toque suave para comodidad extrema.
        - **Polietileno**: Material ligero y blando que proporciona gran salida de bola y absorbe vibraciones. Se usa en palas para mayor confort y manejo.
        - **Eva Hr3**: Goma EVA de alta recuperación, utilizada en palas de alto rendimiento, proporciona mayor potencia y control.
        - **Supersoft Eva**: Goma EVA de baja densidad con gran suavidad, ideal para jugadores que buscan un golpeo suave y cómodo.
        - **Eva Pro**: Variante de goma EVA diseñada para un rendimiento equilibrado entre potencia y control, dirigida a jugadores avanzados.
        - **Power Blast Eva**: Goma EVA diseñada para máxima potencia, recomendada para jugadores ofensivos.
        - **Mega Flex Core**: Núcleo muy flexible y elástico, proporciona gran salida de bola y facilidad de manejo.
        - **Black Eva Hr3**: Goma Black EVA con tecnología HR3 de alta recuperación, diseñada para mayor potencia y memoria elástica.
        - **Eva Soft Low Density**: EVA blanda de baja densidad, enfocada en suavidad, control y comodidad.
        - **Eva Soft Performance**: Variante de EVA blanda optimizada para un rendimiento superior en confort y manejo.
        - **Eva Pro High Density**: Núcleo EVA de alta densidad con tecnología Pro para jugadores que buscan potencia y durabilidad.
        - **Eva High Memory**: Núcleo EVA con memoria de alta recuperación para golpes potentes y rápidos.
        - **Eva, Polietileno**: Combinación de EVA y polietileno, equilibrio entre firmeza y absorción de vibraciones.
        - **Eva Pro 50**: Goma EVA específica con densidad de 50, diseñada para un equilibrio entre control y potencia.
        - **Eva Pro, Multieva**: Combina tecnologías EVA Pro y Multieva para versatilidad avanzada.
        - **Black Eva, Dual Density**: Combinación de Black EVA con tecnología de doble densidad, optimiza control y potencia.
        - **Eva Soft 30**: Goma EVA blanda con densidad de 30, proporciona gran suavidad y control.
        - **Sc White Eva**: Variante especial de goma EVA blanca para suavidad y durabilidad.
        - **Dual Density**: Tecnología que utiliza dos densidades de goma para adaptar potencia y confort en diferentes situaciones de golpeo.
        - **Black Eva Hr9**: Variante Black EVA con tecnología HR9, potencia y memoria mejoradas.
        - **Eva 3xply**: EVA con construcción de tres capas para equilibrio de rendimiento, durabilidad y salida de bola.
        - **Comfort Foam**: Espuma diseñada para máximo confort, alta absorción de vibraciones y manejo fácil.
        - **Eva Pro Touch**: Goma EVA Pro optimizada para un tacto más firme y preciso.
        - **Black Eva, Soft Eva**: Combinación de Black EVA y Soft EVA para balance de potencia y suavidad en golpeos controlados.

    - **Cara**: La cara de una pala de pádel es la superficie plana y exterior que entra en contacto con la pelota. Es uno de los componentes más importantes de la pala, ya que influye directamente en las características del golpe, como la potencia, el control y la precisión. La cara está construida con materiales como fibra de vidrio, carbono, grafeno o combinaciones de estos, que proporcionan distintas propiedades en términos de rigidez, flexibilidad y absorción de vibraciones. La elección del material de la cara afecta la durabilidad y el rendimiento de la pala.
        - **Fibra De Vidrio**: Material ligero y flexible que proporciona un buen control y absorción de vibraciones. Las palas con fibra de vidrio suelen ser más cómodas y manejables.
        - **Carbono 3k**: Carbono tejido con 3.000 filamentos por hilo, ofrece un buen equilibrio entre potencia, control y durabilidad. Ideal para jugadores intermedios y avanzados.
        - **Carbono**: Material robusto y resistente que proporciona alta rigidez y potencia en los golpes. Las palas de carbono son conocidas por su durabilidad y rendimiento en altas exigencias.
        - **Carbono 12k**: Carbono tejido con 12.000 filamentos, más denso y rígido que el carbono 3k. Ofrece una mayor potencia, pero puede ser menos cómodo y absorbente en golpes suaves.
        - **Carbono 18k**: Carbono de mayor densidad con 18.000 filamentos, proporcionando mayor potencia y resistencia, especialmente útil para jugadores avanzados que buscan control y rigidez.
        - **Carbono 24k**: Carbono de alta densidad con 24.000 filamentos, diseñado para un rendimiento máximo en potencia. Es menos flexible, lo que puede ser ideal para jugadores de alto nivel que buscan control total.
        - **Carbono, Fibra De Vidrio**: Combinación de carbono y fibra de vidrio para ofrecer un equilibrio entre potencia, control y confort. Ideal para jugadores que buscan versatilidad en sus palas.
        - **Carbono 15k**: Carbono con 15.000 filamentos, se encuentra entre el carbono 12k y el carbono 18k en cuanto a rigidez y resistencia, proporcionando un buen equilibrio de características.
        - **Fibrix**: Material innovador que combina fibras de carbono y otros elementos para ofrecer mayor flexibilidad y durabilidad, además de un buen rendimiento en potencia.
        - **Grafeno**: Material extremadamente resistente y ligero, conocido por su capacidad de distribución uniforme de la energía, proporcionando más potencia y control sin perder flexibilidad.
        - **Aluminio + Carbono**: Combinación de aluminio y carbono, que proporciona una mayor ligereza, durabilidad y rigidez. Se busca mayor control y potencia sin perder manejabilidad.
        - **Carbono 6k**: Carbono con 6.000 filamentos, una opción de densidad media que ofrece una combinación de rigidez, durabilidad y confort.
        - **Glaphite**: Material compuesto de carbono y grafeno, creado para ofrecer una gran rigidez y resistencia al desgaste, a la vez que mejora la transferencia de energía.
        - **Carbono 16k**: Carbono con 16.000 filamentos, ideal para quienes buscan una pala con mayor control, resistencia y mayor capacidad de respuesta en golpes fuertes.
        - **Tricarbon**: Combinación de tres tipos de carbono con una estructura especial para mejorar el rendimiento en potencia y control, aumentando la durabilidad y la respuesta en el golpeo.
        - **Carbon Flex**: Tecnología de carbono que proporciona mayor flexibilidad en la cara de la pala, lo que se traduce en un mejor control y comodidad en el golpeo.
        - **Carbono 21k**: Carbono con 21.000 filamentos, diseñado para ofrecer una pala rígida y potente, ideal para jugadores agresivos que necesitan un rendimiento máximo en potencia.
        - **Carbono + Grafeno**: Combinación de carbono y grafeno, buscando aprovechar las propiedades de ambos materiales para una pala de alta potencia y control, con una gran resistencia al desgaste.
        - **Carbono 3k, Basalto**: Combinación de carbono 3k con basalto, un material que mejora la absorción de vibraciones y proporciona un golpe más suave, a la vez que mantiene la rigidez.
        - **Carbono 12k, Fibra De Vidrio**: Combinación de carbono 12k y fibra de vidrio, proporcionando una mezcla de potencia y confort. Aporta una mayor salida de bola sin perder control.
        - **Fibra De Carbono**: Goma de fibra de carbono, generalmente más rígida y resistente, proporciona una gran durabilidad y potencia, aunque puede ser menos flexible que otros materiales.
        - **Carbono 1k**: Carbono con 1.000 filamentos, el más flexible de los carbonos mencionados, ideal para jugadores que buscan más control y confort en el golpeo.
        - **Fibra De Vidrio, Carbono 15k**: Combinación de fibra de vidrio y carbono 15k, ofreciendo un balance entre control, confort y rigidez, ideal para jugadores intermedios.
        - **Fiberflex**: Material de fibra flexible que se adapta mejor al estilo de juego de los jugadores, proporcionando más control y suavidad en el golpeo.
        - **Carbono 12k, Fiberflex**: Combinación de carbono 12k y fiberflex, con un buen balance de rigidez y flexibilidad, optimizando tanto el control como la potencia.
        - **Polietileno**: Material que mejora la salida de bola y la absorción de vibraciones, proporcionando una sensación de confort en los golpes, adecuado para jugadores que buscan comodidad.
        - **Carbono, Fibrix**: Combinación de carbono y Fibrix, buscando balancear rigidez, flexibilidad y durabilidad, proporcionando mayor rendimiento en general.
        - **Policarbonato**: Material plástico y resistente que proporciona una mayor rigidez en la pala, mejorando la potencia y el control, aunque con menos flexibilidad.
    
    - **Jugador profesional**: Si el usuario menciona un jugador específico, proporciona las palas que utiliza. Si se indica el año junto al nombre de la pala, especifica que esa pala la utilizón en ese año; de lo contrario, omítelo. Aquí tienes una lista de jugadores y las palas que utilizan:
        - **Agustín Tapia**:  
            NOX AT10 GENIUS 18K BY AGUSTÍN TAPIA 2023  
            NOX AT PRO CUP COORP 2024  
            NOX AT10 GENIUS 12K BY AGUSTIN TAPIA 2023  
            NOX AT10 GENIUS 18K BLACK BY AGUSTIN TAPIA  
            NOX AT10 GENIUS 12K BY AGUSTIN TAPIA 2025  
            NOX AT10 PRO CUP COMFORT BY AGUSTIN TAPIA 2025  
            NOX AT10 PRO CUP HARD BY AGUSTIN TAPIA 2025  
            NOX AT10 GENIUS ATTACK 18K ALUM BY AGUSTIN TAPIA 2025  
            NOX AT10 GENIUS ATTACK 12K BY AGUSTIN TAPIA 2025  
            NOX AT10 GENIUS 12K AGUSTIN TAPIA 2024  
            NOX AT10 GENIUS 18K AGUSTIN TAPIA 2024  
            NOX PACK AT GENIUS LIMITED EDITION 2024  
            NOX AT10 GENIUS ULTRALIGHT 2023  
            NOX AT10 GENIUS 18K ALUM BY AGUSTIN TAPIA 2025  
        - **Juan Lebrón**:  
            BABOLAT TECHNICAL VERON JUAN LEBRON 2024  
            BABOLAT TECHNICAL VERTUO JUAN LEBRON 2024  
            BABOLAT TECHNICAL VIPER JUAN LEBRON 2024  
            BABOLAT TECHNICAL VIPER JUAN LEBRÓN 2025  
            BABOLAT TECHNICAL VERON JUAN LEBRÓN 2025  
            BABOLAT TECHNICAL VERTUO JUAN LEBRÓN  
            BABOLAT TECHNICAL VIPER LEBRON 2023  
            BABOLAT TECHNICAL VERTUO JUAN LEBRÓN 2025  
            BABOLAT TECHNICAL VERON JUAN LEBRÓN 2025  
        - **Alejandro Galán**:  
            ADIDAS METALBONE 3.3 2024  
            ADIDAS METALBONE HRD+ 2024  
            ADIDAS METALBONE CTRL 3.3 2024  
            ADIDAS METALBONE HRD+ 3.4 2025  
            ADIDAS METALBONE 3.4 2025  
            ADIDAS METALBONE 3.2 2023  
        - **Miguel Lamperti**:  
            NOX AT PRO CUP COORP 2024  
            NOX ML10 PRO CUP COORP 2023  
            NOX ML10 PRO CUP ROUGH SURFACE EDITION 2023  
            NOX ML10 QUANTUM 3K BY MIGUEL LAMPERTI 2025  
            NOX ML10 BAHIA 12K LUXURY SERIES 2024  
            NOX ML10 PRO CUP 3K LUXURY SERIES 2024  
            NOX ML10 SHOTGUN 18K LUXURY SERIES 2024  
        - **Paquito Navarro**:  
            BULLPADEL HACK 03 2024  
            BULLPADEL HACK 04 2025  
            BULLPADEL HACK 03 2023  
            BULLPADEL HACK 04 HYBRID 2025  
        - **Franco Stupa**:  
            SIUX ELECTRA ST3 STUPA PRO  
            SIUX ELECTRA ST3 LITE  
            SIUX ELECTRA ST3 SPECIAL EDITION  
            SIUX ELECTRA ST3 GO  
        - **Marta Marrero Marrero**:  
            BLACK CROWN HURRICANE 2022  
            BLACK CROWN HURRICANE 3.0 MUJER  
            BLACK CROWN HURRICANE PRO 3.0 MUJER  
        - **Sanyo Gutiérrez**:  
            BULLPADEL ELITE W 2024  
            BULLPADEL ELITE W MUJER 2023  
            BULLPADEL ELITE LIGHT FIP  
            BULLPADEL ELITE W 2025 MUJER  
        - **Gemma Triay**:  
            BULLPADEL ELITE W 2024
            BULLPADEL ELITE W MUJER 2023
            BULLPADEL ELITE LIGHT FIP
            BULLPADEL ELITE W 2025 MUJER
        - **Fernando Belasteguín**:  
            WILSON BELA PRO V2  
            WILSON BELA PRO PADEL V2.5  
            WILSON BELA LT V2.5 PADEL  
            WILSON BELA PRO PADEL 2  
        - **Marta Ortega**:  
            ADIDAS ADIPOWER LIGHT 3.3  
            ADIDAS CROSS IT LIGHT 3.4 2025  
            ADIDAS CROSS IT LIGHT 2024  
        - **Martin Di Nenno**:  
            BULLPADEL VERTEX 04 MARTÍN DI NENNO 2024  
            BULLPADEL XPLO 2025  
        - **Lucas Campagnolo**:  
            DROP SHOT EXPLORER PRO 6.0 2024  
            DROP SHOT EXPLORER PRO ATTACK 2024  
        - **Ari Sánchez**:  
            HEAD SPEED MOTION 2023  
            HEAD SPEED MOTION ARI SANCHEZ 2024  
        - **Alejandra Salazar**:  
            BULLPADEL FLOW LIGHT MUJER 2024  
            BULLPADEL FLOW WOMAN 2025 MUJER  
        - **Arturo Coello**:  
            HEAD EXTREME PRO ARTURO COELLO 2024  
            HEAD EXTREME PRO  
        - **Defi Brea Senesi**:  
            BULLPADEL VERTEX 04 2025 MUJER  
        - **Alejandro Ruiz Granados**:  
            ADIDAS ADIPOWER CTRL MTW PRO EDT BY ÁLEX RUIZ  
        - **Juan Tello**:  
            BULLPADEL VERTEX 04 2025  
        - **Federico Chingotto**:  
            BULLPADEL NEURON 2025  
        - **Patty Llaguno**:  
            SIUX TRILOGY II CONTROL PATTY PRO  
        - **Beatriz González**:  
            BULLPADEL PEARL BEA GONZALEZ 2024  
        - **Paula Josmaria Martín**:  
            HEAD EXTREME MOTION PAULA JOSEMARIA 2024  
        - **Miguel Yanguas Díez**:  
            LOK MAXX HYPE 2024  

        Pregunta del usuario: {user_input}
        Responde con claridad y proporciona una explicación detallada si es necesario, combinando lo que sabes y estos ejemplos."""
)

prompt_template_recommendations = PromptTemplate( #! Que no pinte el los datos de la pala, pasarle lo mismo pero que solo me haga las comparativas y la recomendación final.
    input_variables=["user_input", "filters"],
    template="""
    Eres un experto en pádel y especializado en recomendar palas de pádel. Tu tarea es mostrarle al usuario las palas que coincidan con los filtros proporcionados. No inventes datos.

    Estos son los filtros aplicados por el usuario:
    {filters}

    Aquí tienes un resumen de las palas recomendadas:
    {user_input}

    Realiza una comparativa entre las palas seleccionadas, destacando las diferencias clave entre ellas, como el balance, el precio, el tipo de juego, etc. Ayuda al usuario a decidir cuál es la mejor opción para él basándote en estas características. 
    **Comparativa**:
    - Realiza una comparativa destacando las diferencias clave (por ejemplo, precio, balance o tipo de juego, nivel de juego, etc.).

    **Recomendación final**:
    - Basándote en la información proporcionada, proporciona una recomendación final que ayude al usuario a tomar una decisión sobre que pala comprar.
    

    Sé breve, claro, y proporciona solo la información relevante de manera agradable y amistosa. No uses información inventada o suposiciones.
    """
)

procesar_consulta_prompt = PromptTemplate(
    input_variables=["consulta"],
    template="""
Dada la siguiente consulta: "{consulta}", 
Por favor, extrae el/los nombre(s) de la(s) pala(s) y el atributo que se está preguntando. Pueden estar en minúsculas o en mayúsculas.	 
El atributo puede ser cosas como: 'Precio', 'Superficie', 'Balance', 'Marca', 'Color', 'Núcleo', 'Cara', 'Formato', 'Dureza', 'Acabado', 'Forma', 'Sexo', 'Tipo de juego, 'Nivel de juego', 'Jugador profesional', 'Imagen', 'Enlace' y 'Descripción'.
Devuelve el atributo siempre y unicamente con la primera letra en mayúscula.
El nombre de la pala debería incluir la marca, el modelo y puede ser que el año o algún otro detalle como número de serie o algo parecido.
Devuelve unicamente un JSON válido con las claves nombre_pala y atributo.
"""
)

intention_template = PromptTemplate(
    input_variables=["user_input"],
    template="""
El usuario ha introducido la siguiente entrada: "{user_input}".

Tu tarea es identificar la intención de esta entrada y clasificarla en una de las siguientes categorías:
1. 'Saludo': Si el usuario está saludando o iniciando una conversación (ejemplos: "Hola", "Buenos días", "¿Cómo estás?").
2. 'Consulta_tecnica': Si la pregunta es sobre el significado o recomendación de una característica general de las palas o sobre el pádel en general, sin referencia a modelos específicos. Incluye preguntas sobre características en base a otras caracteristicas.
3. 'Consulta_personalizada': Si la pregunta es específica sobre uno o varios modelos de pala de pádel. El usuario desea información específica sobre características o comparación entre modelos concretos.
4. 'Recomendacion': Si el usuario solicita recomendaciones de palas sin especificar modelos concretos. Incluye frases como "quiero una pala recomendada", "recomiéndame una pala", o "que pala me recomiendas".
5. 'Recomendacion_personalizada': Si el usuario nos esta describiendo sus características y preferencias para encontrar una pala de pádel.
6. 'Otro': Si la entrada no corresponde con ninguna de las categorías anteriores.

Ejemplos:
1.  Entrada: "¿Cómo estás?"
    Respuesta: 'Saludo'
2.  Entrada: "Hola"
    Respuesta: 'Saludo'
3.  Entrada: "¿Que significa balance alto en una pala de pádel?"
    Respuesta: 'Consulta_tecnica'
4.  Entrada: "¿Cuáles son los beneficios de una superficie rugosa?" 
    Respuesta: 'Consulta_tecnica'
5.  Entrada: "¿Cuál es el mejor balance para un jugador intermedio?"
    Respuesta: 'Consulta_tecnica'
6.  Entrada: "¿Qué tipo de pala debería usar si juego de defensa?"
    Respuesta: 'Consulta_tecnica'
7.  Entrada: "Soy nivel principiante, ¿qué tipo de dureza me recomiendas?"
    Respuesta: 'Consulta_tecnica'
8.  Entrada: "¿Qué balance recomendarías a un jugador nivel avanzado?"
    Respuesta: 'Consulta_tecnica'
9.  Entrada: "¿Cuál es el balance de la pala SIUX GENESIS POWER 12K?" 
    Respuesta: 'Consulta_personalizada'
10. Entrada: "Compárame las superficies de las palas BULLPADEL SKY POWER y HEAD CALIBRE ROJO, y recomiéndame la mejor para un principiante." 
    Respuesta: 'Consulta_personalizada'
11. Entrada: "¿Que palas me recomiendas?"
    Respuesta: 'Recomendacion'
12. Entrada: "Quiero recibir recomendaciones sobre palas."
    Respuesta: 'Recomendacion'
13. Entrada: "¿Que tiempo hará mañana?"
    Respuesta: 'Otro'
14. Entrada: "Soy un jugador de nivel principiante, quiero una pala de pádel con un balance medio y que sea blanda. ¿Cuál es la mejor opción?"
    Respuesta: 'Recomendacion_personalizada'
15. Entrada: "Hola, soy un jugador de nivel avanzado que le gusta la potencia y el control. Busco una pala con balance alto y forma redonda. ¿Cuál me recomiendas?"
    Respuesta: 'Recomendacion_personalizada'

Por favor, devuelve una de las siguientes palabras: 'Saludo', 'Consulta_tecnica', 'Consulta_personalizada', 'Recomendacion' 'Recomendacion_personalizada' o 'Otro'.
"""
)

greeting_template = PromptTemplate(
    input_variables=["user_input"],
    template="""
Eres un asistente virtual experto en pádel llamado PADELMASTER, encargado de proporcionar información sobre características de palas y recomendar palas de pádel según los gustos, preferencias y características del usuario.

Este es el mensaje que te ha enviado el usuario: {user_input}

Responde de manera educada y amistosa. Puedes incluir expresiones como:
- "¡Hola! ¿En qué puedo ayudarte hoy?"
- "¡Buenos días! ¿Estás buscando alguna pala en particular?"
- "¡Hola, encantado de verte por aquí! ¿Tienes alguna pregunta sobre pádel?"

Después del saludo, muéstrate disponible para ayudar con cualquier consulta relacionada con palas de pádel.
"""
)

recomendation = PromptTemplate(
    input_variables=["mensaje"],
    template="""
El usuario quiere recibir recomendaciones sobre palas de pádel. Aquí su mensaje: "{mensaje}".
Indicale que para poder recibir una mejor recomendación debe proporcionar la mayor cantidad de información posible. 
También coméntale que existen las siguientes caracteristicas de palas de pádel y que si no conoce el significado de alguna puede preguntarte para que le resuelvas las dudas.
Aquí te dejo una lista de las características y sus posibles valores:
- Marca: 'Adidas', 'Akkeron', 'Ares', 'Babolat', 'Black Crown', 'Bullpadel', 'Drop Shot', 'Dunlop', 'Enebe', 'Harlem', 'Head', 'Joma', 'Kombat', 'Kiukma', 'Lok', 'Mystica', 'Nox', 'Royal Padel', 'Salming', 'Siux', 'Softee', 'Star Vie', 'Vairo', 'Varlion', 'Vibor-a', 'Wilson', 'Wingpadel'.
- Precio (en euros)
- Sexo: 'Hombre', 'Mujer' y 'Junior'.
- Forma: 'Diamante', 'Híbrida', 'Lágrima', 'Redonda'.
- Balance: 'Bajo', 'Medio', 'Alto'.
- Dureza: 'Blanda', 'Media', 'Dura'.
- Acabado: 'Arenoso', 'Brillo', 'Brillo-Relieve3D', 'Brillo-Mate', 'Brillo-Arenoso', 'Mate', 'Mate-Arenoso', 'Mate-Relieve3D', 'Relieve 3D', 'Relieve3D-Arenoso', 'Rugosa'.
- Formato: 'Normal', 'Oversize'.
- Superficie: 'Arenosa', 'Rugosa', 'Rugosa-Arenosa', 'Lisa'.
- Núcleo: 'Soft Eva', 'Eva', 'Black Eva', 'Medium Eva', 'Multieva', 'Foam', 'Hard Eva', 'Ultrasoft Eva', 'Polietileno', 'Eva Hr3', 'Supersoft Eva', 'Eva Pro', 'Power Blast Eva', 'Mega Flex Core', 'Black Eva Hr3', 'Eva Soft Low Density', 'Eva Soft Performance', 'Eva Pro High Density', 'Eva High Memory', 'Eva, Polietileno', 'Eva Pro 50', 'Eva Pro, Multieva', 'Black Eva, Dual Density', 'Eva Soft 30', 'Sc White Eva', 'Dual Density', 'Black Eva Hr9', 'Eva 3xply', 'Comfort Foam', 'Eva Pro Touch', 'Black Eva, Soft Eva'.
- Cara: 'Fibra De Vidrio', 'Carbono 3k', 'Carbono', 'Carbono 12k', 'Carbono 18k', 'Carbono 24k', 'Carbono, Fibra De Vidrio', 'Carbono 15k', 'Fibrix', 'Grafeno', 'Aluminio + Carbono', 'Carbono 6k', 'Glaphite', 'Carbono 16k', 'Tricarbon', 'Carbon Flex', 'Carbono 21k', 'Carbono + Grafeno', 'Carbono 3k, Basalto', 'Carbono 12k, Fibra De Vidrio', 'Fibra De Carbono', 'Carbono 1k', 'Fibra De Vidrio, Carbono 15k', 'Fiberflex', 'Carbono 12k, Fiberflex', 'Polietileno', 'Carbono, Fibrix', 'Policarbonato'.
- Nivel de juego: 'Avanzado / Competición', 'Principiante / Intermedio', 'Profesional', 'Avanzado / Competición, Profesional', 'Avanzado / Competición, Principiante / Intermedio', 'Principiante / Intermedio, Profesional'.
- Tipo de juego: 'Control, Potencia', 'Control', 'Potencia', 'Polivalente'.
- Jugador profesional: 'Agustín Tapia', 'Miguel Lamperti', 'Alejandro Galán', 'Paquito Navarro', 'Juan Lebrón', 'Gemma Triay', 'Lucas Campagnolo', 'Franco Stupa', 'Marta Ortega', 'Sanyo Gutiérrez', 'Alejandra Salazar', 'Defi Brea Senesi', 'Fernando Belasteguín', 'Marta Marrero Marrero', 'Mª Pilar Sánchez Alayeto', 'Beatriz González', 'Juan Tello', 'Martin Di Nenno', 'Federico Chingotto', 'Ari Sánchez', 'Pablo Lima', 'Arturo Coello', 'Alejandro Ruiz Granados', 'Agustín Tapia', 'Miguel Lamperti', 'Paula Josmaria Martín', 'Patty Llaguno', 'Patty Llaguno', 'Miguel Yanguas Díez', 'Mª Jose Sánchez Alayeto', 'Seba Nerone', 'Aranzazu Osoro Ulrich'.

Que la respuesta sea amigable y cercana. 
"""
)

conversation_template = PromptTemplate(
    input_variables=["user_input", "conversation"],
    template="""
El usuario ha realizado la siguiente consulta: "{user_input}". ¿Se entiende esta consulta por si sola?
En caso de que la consulta no se entienda por si sola y necesitas contexto, este es el historial de la conversación: {conversation}.
Devuelve la pregunta reformulada usando el histórico de la conversación que te he proporcionado en el caso de que no se entienda la pregunta por si sola.

Ejemplo de conversación 1:
    Entrada: "Hola, como estas?"
    Respuesta: "Hola, como estas?"
    Entrada: "Que implica el balance de una pala en el estilo de juego de pádel?"
    Respuesta: "Que implica el balance de una pala en el estilo de juego de pádel?"
    Entrada: "¿Cuál es el balance de la pala SIUX GENESIS POWER 12K?"
    Respuesta: "¿Cuál es el balance de la pala SIUX GENESIS POWER 12K?"

Ejemplo de conversación 2:
    Entrada: "Buenas tardes"
    Respuesta: "Buenas tardes"
    Entrada: "¿Cuanto cuesta la pala BABOLAT TECHNICAL VIPER 2023?"
    Respuesta: "¿Cuanto cuesta la pala BABOLAT TECHNICAL VIPER 2023?"
    Entrada: "¿Que palas utiliza Agustín Tapia?"
    Respuesta: "¿Que palas utiliza Agustín Tapia?"
"""
)

recomendacion_personalizada_template = PromptTemplate(
    input_variables=["user_input"],
    template="""
El usuario ha proporcionado información sobre sus características y preferencias para encontrar una pala de pádel. Este es su mensaje: "{user_input}".

Necesito que analices el mensaje y extraigas todas las características que se refieren a la pala de pádel. Estas son las características que debes identificar y sus posibles valores:
- Marca: 'Adidas', 'Akkeron', 'Ares', 'Babolat', 'Black Crown', 'Bullpadel', 'Drop Shot', 'Dunlop', 'Enebe', 'Harlem', 'Head', 'Joma', 'Kombat', 'Kiukma', 'Lok', 'Mystica', 'Nox', 'Royal Padel', 'Salming', 'Siux', 'Softee', 'Star Vie', 'Vairo', 'Varlion', 'Vibor-a', 'Wilson', 'Wingpadel'.
- Sexo: 'Hombre', 'Mujer' y 'Junior'.
- Forma: 'Diamante', 'Híbrida', 'Lágrima', 'Redonda'.
- Balance: 'Bajo', 'Medio', 'Alto'.
- Dureza: 'Blanda', 'Media', 'Dura'.
- Acabado: 'Arenoso', 'Brillo', 'Brillo-Relieve3D', 'Brillo-Mate', 'Brillo-Arenoso', 'Mate', 'Mate-Arenoso', 'Mate-Relieve3D', 'Relieve 3D', 'Relieve3D-Arenoso', 'Rugosa'.
- Formato: 'Normal', 'Oversize'.
- Superficie: 'Arenosa', 'Rugosa', 'Rugosa-Arenosa', 'Lisa'.
- Núcleo: 'Soft Eva', 'Eva', 'Black Eva', 'Medium Eva', 'Multieva', 'Foam', 'Hard Eva', 'Ultrasoft Eva', 'Polietileno', 'Eva Hr3', 'Supersoft Eva', 'Eva Pro', 'Power Blast Eva', 'Mega Flex Core', 'Black Eva Hr3', 'Eva Soft Low Density', 'Eva Soft Performance', 'Eva Pro High Density', 'Eva High Memory', 'Eva, Polietileno', 'Eva Pro 50', 'Eva Pro, Multieva', 'Black Eva, Dual Density', 'Eva Soft 30', 'Sc White Eva', 'Dual Density', 'Black Eva Hr9', 'Eva 3xply', 'Comfort Foam', 'Eva Pro Touch', 'Black Eva, Soft Eva'.
- Cara: 'Fibra De Vidrio', 'Carbono 3k', 'Carbono', 'Carbono 12k', 'Carbono 18k', 'Carbono 24k', 'Carbono, Fibra De Vidrio', 'Carbono 15k', 'Fibrix', 'Grafeno', 'Aluminio + Carbono', 'Carbono 6k', 'Glaphite', 'Carbono 16k', 'Tricarbon', 'Carbon Flex', 'Carbono 21k', 'Carbono + Grafeno', 'Carbono 3k, Basalto', 'Carbono 12k, Fibra De Vidrio', 'Fibra De Carbono', 'Carbono 1k', 'Fibra De Vidrio, Carbono 15k', 'Fiberflex', 'Carbono 12k, Fiberflex', 'Polietileno', 'Carbono, Fibrix', 'Policarbonato'.
- Nivel_de_juego: 'Avanzado / Competición', 'Principiante / Intermedio', 'Profesional', 'Avanzado / Competición, Profesional', 'Avanzado / Competición, Principiante / Intermedio', 'Principiante / Intermedio, Profesional'.
- Tipo_de_juego: 'Control, Potencia', 'Control', 'Potencia', 'Polivalente'.
- Jugador_profesional: 'Agustín Tapia', 'Miguel Lamperti', 'Alejandro Galán', 'Paquito Navarro', 'Juan Lebrón', 'Gemma Triay', 'Lucas Campagnolo', 'Franco Stupa', 'Marta Ortega', 'Sanyo Gutiérrez', 'Alejandra Salazar', 'Defi Brea Senesi', 'Fernando Belasteguín', 'Marta Marrero Marrero', 'Mª Pilar Sánchez Alayeto', 'Beatriz González', 'Juan Tello', 'Martin Di Nenno', 'Federico Chingotto', 'Ari Sánchez', 'Pablo Lima', 'Arturo Coello', 'Alejandro Ruiz Granados', 'Agustín Tapia', 'Miguel Lamperti', 'Paula Josmaria Martín', 'Patty Llaguno', 'Patty Llaguno', 'Miguel Yanguas Díez', 'Mª Jose Sánchez Alayeto', 'Seba Nerone', 'Aranzazu Osoro Ulrich'.
- Precio_min: El precio más bajo que ha indicado el usuario. En caso de no mencionarlo, asignar '0.0'.
- Precio_max: El precio más alto que ha indicado el usuario. En caso de no mencionarlo, asignar '500.0'. Si solo se menciona un valor, asignarlo a 'precio_max'.
El rango de precios debe ser separado en dos variables: 'precio_min' (el precio más bajo) y 'precio_max' (el precio más alto).


Por favor, devuelve exclusivamente un **JSON** con todas las caracteristicas mencionadas con la primera letra en mayúscula, nada mas. Si alguna característica no tiene un valor en el mensaje del usuario o no coincide con ninguno de los valores proporcionados, asigna "null" a esa característica. Los nombres de las caracteristicas y sus valores deben ser exactamente iguales a los especificados.
"""
)