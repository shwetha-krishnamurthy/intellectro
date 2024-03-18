import os
import streamlit as st
import arxiv_url
from search_research_paper import get_summary, search_papers


def main():
    # Title
    st.title("Intellectro")
    st.write("Simplifying Literature Review")

    # API Key input (masked)
    # API Key
    eden_ai_api_key = st.text_input("Enter EdenAI API Key (required; Click here to create one: https://www.edenai.co/):", type='password')
    
    # pinecone_api_key = st.text_input("Enter Pinecone API Key (required):", type='password')

    os.environ['EDEN_AI_API_KEY'] = "Bearer " + eden_ai_api_key
    # os.environ['PINECONE_API_KEY'] = pinecone_api_key

    # User input for the research paper's title
    # paper_title = st.text_input("Enter the area of research you want to understand:")

    # Expertise level selection
    # expertise_level = st.selectbox("Choose your expertise level on the topic you are searching for", ["No Experience", "I know somethings", "I'm a researcher in this field"])

    # Button for submitting the query
    # if st.button('Proceed'):
    if eden_ai_api_key: # and pinecone_api_key:
        # Generating the summary based on the API key, paper title, and expertise level
        # explanation = query_explanation.get_query_explanation(paper_title, expertise_level)
        # explanation = get_summary(search_papers(paper_title))

        # Displaying the summary
        # st.markdown(explanation, unsafe_allow_html=True)
        
        # Define a key for the expander to uniquely identify them in the session state
        expander_key = 0
        query = st.text_input("Enter your search query:")
        if query:
            results = search_papers(query)
            paper_results_dict = []
            for result in results:
                paper = arxiv_url.get_paper_metadata_from_url(result["id"])
                paper_results_dict.append(paper)

            for paper in paper_results_dict:
                expander_key += 1
                with st.expander(paper["title"]): #, key=f"exp_{expander_key}"):
                    st.write(paper["summary"])
                    # Use a link instead of a button for "View More" to work around the issue
                    paper_details_key = f"details_{paper['link']}"
                    if paper_details_key not in st.session_state:
                        st.session_state[paper_details_key] = False
                    
                    # Check if the "View More" link was clicked for this paper
                    if st.session_state[paper_details_key]:
                        # # Show details and a button to collapse the details
                        if st.button("Show Less", key=f"less_{expander_key}"):
                            st.session_state[paper_details_key] = False
                    else:
                        # Show a link to view more details
                        if st.button("View More", key=f"more_{expander_key}"):
                            st.session_state[paper_details_key] = True
                            # Show details
                            explanation = get_summary(paper["link"])
                            # Displaying the summary
                            st.markdown(explanation, unsafe_allow_html=True)


    else:
        st.write("Please enter the EdenAI API key.")

if __name__ == "__main__":
    main()
