# Make sure to install the necessary libraries:
# pip install streamlit langchain langchain_google_genai python-dotenv

# In your .env file, you should have:
# LANGCHAIN_API_KEY="your_langsmith_api_key"
# GOOGLE_API_KEY="your_google_api_key"

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- FIX: Load keys into variables and check if they exist ---
# We retrieve the keys here and can provide a clear error if they're missing.
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

# Set up LangSmith tracking (optional, but good for debugging)
# This prevents the TypeError by ensuring we only set the variable if the key exists.
if langchain_api_key:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = langchain_api_key

## Prompt Template
# This remains the same as it defines the structure of the conversation.
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user queries."),
        ("user", "Question:{question}")
    ]
)

## Streamlit Framework
st.title('Langchain Demo With Google Gemini API')
input_text = st.text_input("Search the topic you want")


# --- Main Application Logic ---
# First, check if the Google API key is available.
if not google_api_key:
    st.error("Google API key is not set. Please add it to your .env file.")
else:
    # --- FIX: Instantiate LLM with the API key directly ---
    # This is a more robust way to handle authentication.
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser

    if input_text:
        # Display a loading spinner while the request is being processed
        with st.spinner('Thinking...'):
            response = chain.invoke({'question': input_text})
            st.write(response)
