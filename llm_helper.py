from dotenv import load_dotenv
from langchain_groq import ChatGroq
import streamlit as st
import os

load_dotenv()
llm= ChatGroq(groq_api_key=st.secrets("GROQ_API_KEY"), model_name="llama-3.1-8b-instant")

if __name__ == "__main__":
    response = llm.invoke("What are the two main ingredients for samosa?")
    print(response.content)