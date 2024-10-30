import os
import openai
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.mention import mention

st.set_page_config(page_title="News Summarizer Tool", page_icon="", layout="wide")

with st.sidebar:
    st.image('images/White_AI Republic.png')
    openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
    if not (openai.api_key.startswith('sk-') and len(openai.api_key)==51):
        st.warning('Please enter your OpenAI API token!', icon='⚠️')
    else:
        st.success('Proceed to entering your news article!', icon='👉')
    with st.container():
        l, m, r = st.columns((1, 3, 1))
        with l: st.empty()
        with m: st.empty()
        with r: st.empty()

    options = option_menu(
        "Dashboard", 
        ["Home", "About Us", "News Summarizer"],
        icons = ['house', 'info-circle', 'newspaper'],
        menu_icon = "list", 
        default_index = 0,
        styles = {
            "icon": {"color": "#dec960", "font-size": "20px"},
            "nav-link": {"font-size": "17px", "text-align": "left", "margin": "5px", "--hover-color": "#262730"},
            "nav-link-selected": {"background-color": "#262730"}          
        })

# Options : Home
if options == "Home":
    st.title("Welcome to the News Summarizer Tool!")
    st.write("This tool helps you quickly summarize news articles.")
    st.write("Simply paste your article in the 'News Summarizer' section and get a concise summary.")
    st.write("Our AI-powered summarizer extracts key information to save you time!")
   
elif options == "About Us":
    st.title("About Us")
    st.write("# AI Republic News Summarizer")
    st.image('images/Mountain.png')
    st.write("## Empowering readers with quick, accurate news summaries")
    st.markdown("[Connect with us via LinkedIn](https://www.linkedin.com/in/julian-carl-o%C3%B1ate-953520280/)")
    st.write("For more information, visit our website: [www.airepublic.com](https://www.airepublic.com)")
    st.write("\n")

# Options : News Summarizer
elif options == "News Summarizer":
    st.title("News Summarizer")
    
    System_Prompt = """
You are a knowledgeable and concise assistant specialized in summarizing news articles effectively. When the user provides a link, your primary goal is to extract the core message, main points, and significant details from the article to give the user a comprehensive yet succinct understanding. Here’s how to approach each summary:

Identify Key Elements: Focus on answering the core questions of journalism: Who, What, Where, When, Why, and How. Prioritize any background information necessary for the user to fully understand the topic without reading the article themselves.

Main Points Over Details: Stick to essential facts and avoid overly technical or minor details unless they’re critical to the story. Your goal is to capture the article's main themes, crucial developments, and any specific names, dates, or figures that anchor the article's importance.

Stay Objective and Neutral: Summarize without adding any personal interpretation, opinions, or assumptions. Present the information as objectively as possible, mirroring the tone of an impartial journalist. If the article presents different viewpoints, reflect that in a balanced way without indicating a preferred stance.

Be Clear and Concise: Structure your summary to be easily scannable. Aim for brevity, generally two to five sentences, unless the user requests more depth. Avoid complex language and instead use straightforward phrasing to make the summary accessible to all readers.

Adapt for User Requests: If the user asks for more detail, highlights, or specific information (e.g., context or implications), be prepared to expand on these aspects. Remain flexible to provide tailored summaries that meet specific needs without drifting from the article's original intent.

Maintain Accuracy and Integrity: Double-check your summary to ensure it captures the true meaning of the article. Avoid embellishments, inferred conclusions, or any inaccuracies that might misrepresent the facts or tone of the piece.

Always strive to be efficient and respectful of the user’s time, providing a complete picture in a minimal amount of text. Ultimately, your role is to empower the user with clear, valuable information at a glance.
    
    """

    user_message = st.text_area("Paste your news article here:", height=300)
    
    if st.button("Summarize"):
        if user_message:
            struct = [{"role": "system", "content": System_Prompt}]
            struct.append({"role": "user", "content": user_message})
            
            try:
                chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=struct)
                response = chat.choices[0].message.content
                st.subheader("Summary:")
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a news article to summarize.")