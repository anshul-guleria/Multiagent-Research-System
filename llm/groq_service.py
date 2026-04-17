from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def Groq(model="llama-3.1-8b-instant", temperature=0.2):
    return ChatGroq(model=model, temperature=temperature)
