import os
from langchain_groq import ChatGroq


llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        model_kwargs={
            "top_p": 1
        },
        api_key=os.getenv('GROQ_API_KEY')
)