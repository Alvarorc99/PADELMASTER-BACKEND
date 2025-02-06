"""File to define the schemas"""

from pydantic import BaseModel, Field

class IntentionOutput(BaseModel):

    Greeting: bool = Field(default=False, description="Si se trata de una saludo")
    Technical_query: bool = Field(default=False, description="Si el usuario pregunta sobre características generales de las palas de pádel o conceptos técnicos relacionados (como balance, dureza, acabado, superficie, etc.)")
    Personalized_query: bool = Field(default=False, description="Si el usuario pregunta sobre una pala específica mencionando su nombre (por ejemplo '¿Cuánto cuesta la BULLPADEL HACK 03?')")
    Recommendation: bool = Field(default=False, description="Si el usuario pide una recomendación general de palas sin especificar preferencias ni características.")
    Personalized_recommendation: bool = Field(default=False, description="Si el usuario solicita una recomendación y menciona características o preferencias.")
    Other: bool = Field(default=False, description="Si la entrada no es un saludo y no corresponde con una consulta relacionada con el pádel.")

class QuestionOutput(BaseModel):
    Question: str = Field(default=False, description="Pregunta original del usuario reformulada en caso necesario.") 