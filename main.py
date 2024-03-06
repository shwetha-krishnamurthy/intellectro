import os
import streamlit as st
import query_explanation
from search_research_paper import get_summary, search_papers

def main():
    # Title
    st.title("Intellectro")
    st.write("Get an explanation of any research paper")

    # API Key input (masked)
    # API Key
    eden_ai_api_key = st.text_input("Enter EdenAI API Key (required; Click here to create one: https://www.edenai.co/):", type='password')
    
    pinecone_api_key = st.text_input("Enter Pinecone API Key (required):", type='password')

    os.environ['EDEN_AI_API_KEY'] = "Bearer " + eden_ai_api_key
    os.environ['PINECONE_API_KEY'] = pinecone_api_key

    # User input for the research paper's title
    paper_title = st.text_input("Enter the research paper title you want to understand:")

    # Expertise level selection
    # expertise_level = st.selectbox("Choose your expertise level on the topic you are searching for", ["No Experience", "I know somethings", "I'm a researcher in this field"])

    # Button for submitting the query
    if st.button('Explain it to me!'):
        if paper_title and eden_ai_api_key and pinecone_api_key:
            # Generating the summary based on the API key, paper title, and expertise level
            # explanation = query_explanation.get_query_explanation(paper_title, expertise_level)
            explanation = get_summary(search_papers("Large Language Models"))

            # Displaying the summary
            st.markdown(explanation, unsafe_allow_html=True)
        else:
            st.write("Please enter both API keys and a title for the research paper.")

if __name__ == "__main__":
    main()
