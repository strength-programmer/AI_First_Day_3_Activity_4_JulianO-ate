import os
import openai
import numpy as np
import pandas as pd
import json
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from openai.embeddings_utils import get_embedding
import faiss
import streamlit as st
import warnings
from streamlit_option_menu import option_menu
from streamlit_extras.mention import mention

warnings.filterwarnings("ignore")

st.set_page_config(page_title="AI First Chatbot Template", page_icon="", layout="wide")

with st.sidebar :
    openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
    if not (openai.api_key.startswith('sk-') and len(openai.api_key)==164):
        st.warning('Please enter your OpenAI API token!', icon='⚠️')
    else:
        st.success('Proceed to entering your prompt message!', icon='👉')
    with st.container() :
        l, m, r = st.columns((1, 3, 1))
        with l : st.empty()
        with m : st.empty()
        with r : st.empty()

    options = option_menu(
        "Dashboard", 
        ["Home", "About Us", "Model"],
        icons = ['book', 'globe', 'tools'],
        menu_icon = "book", 
        default_index = 0,
        styles = {
            "icon" : {"color" : "#dec960", "font-size" : "20px"},
            "nav-link" : {"font-size" : "17px", "text-align" : "left", "margin" : "5px", "--hover-color" : "#262730"},
            "nav-link-selected" : {"background-color" : "#262730"}          
        })


if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'chat_session' not in st.session_state:
    st.session_state.chat_session = None  # Placeholder for your chat session initialization

# Options : Home
if options == "Home" :

   st.title("This is the Home Page!")
   st.write("Introduce Your Chatbot!")
   st.write("What is their Purpose?")
   st.write("What inspired you to make [Chatbot Name]?")
   
elif options == "About Us" :
     st.title("About Us")
     st.write("# [Name]")
     st.write("## [Title]")
     st.text("Connect with me via Linkedin : [LinkedIn Link]")
     st.text("Other Accounts and Business Contacts")
     st.write("\n")

# Options : Model
elif options == "Model" :
     st.title("This Section is for your Chatbot!")
     st.title('News Summarizer Tool')
     col1, col2, col3 = st.columns([1, 2, 1])

     with col2:
          News_Article = st.text_input("News Article", placeholder="News : ")
          submit_button = st.button("Generate Summary")

     System_Prompt = """
You are a knowledgeable and concise assistant specialized in summarizing news articles effectively. When the user provides a news article, your primary goal is to extract the core message, main points, and significant details to give the user a comprehensive yet succinct understanding. Here's how to approach each summary:

1. Identify Key Elements: Focus on answering the core questions of journalism: Who, What, Where, When, Why, and How. Prioritize any background information necessary for the user to fully understand the topic.

2. Main Points Over Details: Stick to essential facts and avoid overly technical or minor details unless they're critical to the story. Capture the article's main themes, crucial developments, and any specific names, dates, or figures that anchor the article's importance.

3. Stay Objective and Neutral: Summarize without adding personal interpretation, opinions, or assumptions. Present the information objectively, mirroring the tone of an impartial journalist. If the article presents different viewpoints, reflect that in a balanced way.

4. Be Clear and Concise: Structure your summary to be easily scannable. Aim for brevity, generally three to seven sentences, unless more depth is required. Use straightforward phrasing to make the summary accessible to all readers.

5. Maintain Accuracy and Integrity: Ensure your summary captures the true meaning of the article. Avoid embellishments, inferred conclusions, or any inaccuracies that might misrepresent the facts or tone of the piece.

Always strive to be efficient and respectful of the user's time, providing a complete picture in a minimal amount of text. Your role is to empower the user with clear, valuable information at a glance.
"""

     if submit_button and News_Article:
         struct = [{'role': 'system', 'content': System_Prompt}]
         struct.append({'role': 'user', 'content': News_Article})

         chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=struct)
         response = chat.choices[0].message.content

         st.write("Summary:")
         st.write(response)