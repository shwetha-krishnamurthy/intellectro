import os
import json
import requests
import arxiv_url

NUM_RESULTS = 3

def get_query_explanation(query, expertise_level):

    expertise_level_dict = {
        "No Experience": "a 12 year old", 
        "I know somethings": "a university student beginning to learn about this field, but I have some limited background", 
        "I'm a researcher in this field": "a researcher with deep knowledge in this field"
    }

    papers = arxiv_url.get_papers_from_arXiv(query, NUM_RESULTS)

    data = ''
    paper_summary_pairs = ''
    for ct, paper in enumerate(papers):
        data += paper["summary"]
        paper_summary_pairs += f"Paper Title {ct + 1}: {paper["title"]}; Summary: {paper["summary"]}"

    data = data.replace("\n", " ")

    headers = {"Authorization": f"{os.environ["EDEN_AI_API_KEY"]}"}

    url = "https://api.edenai.run/v2/text/chat"
    payload = {
        "providers": "openai",
        "text": f"Explain this to me like I'm {expertise_level_dict[expertise_level]}: {data}",
        "chatbot_global_action": f"""
        Act as a teacher.
        You need to provide detailed individual explanation for each paper-summary pair in the following list: {paper_summary_pairs}.
        You need to format each paper title in bold and it should look like a subtitle and
        denote the paper number it is from the list provided to you.
        You do not need to return the summary of each paper.
        You need to provide all your answers in markdown formatting.
        """,
        "previous_history": [],
        "temperature": 0.4,
        "max_tokens": 2000,
        "fallback_providers": "cohere"
    }

    response = requests.post(url, json=payload, headers=headers)

    result = json.loads(response.text)
    return result["openai"]["generated_text"]
