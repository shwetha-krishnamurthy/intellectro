import os
import streamlit as st
import query_explanation

def main():
    # Title
    st.title("Intellectro")
    st.write("Get an explanation of any research paper")

    # API Key input (masked)
    # API Key
    api_key = st.text_input("Enter EdenAI API Key (required):", type='password')

    os.environ['EDEN_AI_API_KEY'] = "Bearer " + api_key

    # User input for the research paper's title
    paper_title = st.text_input("Enter the research paper title you want to understand:")

    # Expertise level selection
    expertise_level = st.selectbox("Choose your expertise level on the topic you are searching for", ["No Experience", "I know somethings", "I'm a researcher in this field"])

    # Button for submitting the query
    if st.button('Explain it to me!'):
        if paper_title and api_key:
            # Generating the summary based on the API key, paper title, and expertise level
            explanation = query_explanation.get_query_explanation(paper_title, expertise_level)
            # Displaying the summary
            st.markdown(explanation, unsafe_allow_html=True)
        else:
            st.write("Please enter both an API key and a title for the research paper.")

if __name__ == "__main__":
    main()
