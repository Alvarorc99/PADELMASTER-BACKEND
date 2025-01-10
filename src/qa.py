from langchain_aws import ChatBedrock
from config.config import *
from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate(
    input_variables=["user_input"],
    template="""Responde con lo que sepas y no inventes información."""
)

llm = ChatBedrock(model_id=LLM_MODEL_NAME, client=client)

consulta = "¿Que es un sistema RAG?"

prompt = prompt_template.format(user_input=consulta)
respuesta = llm.invoke(prompt)

print("Respuesta del modelo:")
print(respuesta)
