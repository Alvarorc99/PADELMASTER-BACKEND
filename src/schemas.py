from pydantic import BaseModel, Field

class IntentionOutput(BaseModel):

    Saludo: bool = Field(default=False, description="Si se trata de una saludo")
    Consulta_tecnica: bool = Field(default=False, description="Si se trata de una consulta técnica sobre caracteristicas generales de las palas (como balance, dureza, acabado, superficie, etc.)")
    Consulta_personalizada: bool = Field(default=False, description="Si se trata de una consulta personalizada sobre una o varias palas en concreto")
    Otro: bool = Field(default=False, description="Si está excesivamente claro que no se trata de una consulta relacionada con el pádel o no es un saludo")