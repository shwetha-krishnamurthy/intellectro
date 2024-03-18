import os
import json
import requests
import create_vector_store
import arxiv_url
from pinecone import Pinecone


def search_papers(query):
    pc = Pinecone(
        api_key=os.environ['PINECONE_API_KEY']
    )
    index = pc.Index(name='research-papers')
    query_embedding = create_vector_store.get_embedding([query])
    search_results = index.query(vector=query_embedding, 
                                 top_k = 5,
                                 include_metadata=True)
    return search_results["matches"]

def get_summary(paper_id):
    paper_full_text = arxiv_url.get_data_from_api(paper_id)

    headers = {"Authorization": f"{os.environ['EDEN_AI_API_KEY']}"}

    url = "https://api.edenai.run/v2/text/chat"
    payload = {
        "providers": "openai",
        "text": f"Provide me with the summary, assumptions, and the methodology described in this paper: {paper_full_text}",
        "chatbot_global_action": """
        Act as a researcher.
        You will receive research papers in text format in the query.
        You need to identify the title, authors, and the published date from the text provided.
        Display the title, the authors, and the from the provided text as a heading.
        Your answer needs to contain 4 parts:
            1. The problem: Summarize the problem being addressed in the paper.
            2. Assumptions: Summarize the assumptions taken in the paper.
            3. Methodology: Summarize the Research methodology.
            4. Results: Summarize the results of the paper.
        You need to part in bold and it should look like a subtitle.
        You need to provide all your answers in markdown formatting.
        You got this! You can do it!
        """,
        "previous_history": [],
        "temperature": 0.2,
        "max_tokens": 2000,
        "fallback_providers": "cohere"
    }

    response = requests.post(url, json=payload, headers=headers)

    result = json.loads(response.text)
    # print(result)
    return result["openai"]["generated_text"]

def main():
    get_summary(search_papers("Large Language Models"))

if __name__ == "__main__":
    main()
