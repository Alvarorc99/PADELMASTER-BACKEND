"""File to define the schemes"""

from pydantic import BaseModel, Field

class IntentionOutput(BaseModel):

    Greeting: bool = Field(default=False, description="Si se trata de una saludo")
    Technical_query: bool = Field(default=False, description="Si se trata de una consulta técnica sobre caracteristicas generales de las palas (como balance, dureza, acabado, superficie, etc.)")
    Personalized_query: bool = Field(default=False, description="Si se trata de una consulta sobre una pala en concreto(por ejemplo '¿Cuánto cuesta la BULLPADEL HACK 03?')")
    Recommendation: bool = Field(default=False, description="Si el usuario quiere recibir recomendaciones sobre palas.")
    Personalized_recommendation: bool = Field(default=False, description="Si el usuario quiere recibir recomendaciones sobre palas en función de sus características y preferencias.")
    Other: bool = Field(default=False, description="Si está excesivamente claro que no se trata de una consulta relacionada con el pádel o no es un saludo")

class QuestionOutput(BaseModel):
    Question: str = Field(default=False, description="Pregunta original del usuario reformulada en caso necesario.") 