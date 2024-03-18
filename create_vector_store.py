import io
import os
import json
import PyPDF2
import requests
from pinecone import Pinecone, ServerlessSpec
import arxiv_url

NUM_RESULTS = 100

def get_embedding(texts):
    url = "https://api.edenai.run/v2/text/embeddings"

    payload = {
        "providers": "openai",
        "texts": texts,
        "response_as_dict": True,
        "attributes_as_list": False,
        "show_original_response": False
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": os.environ['EDEN_AI_API_KEY']
    }

    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    return result["openai"]["items"][0]["embedding"]

def construct_embedding_dict(query):
    # Convert multi-page PDFs to text
    
    papers = arxiv_url.get_papers_from_arXiv(query, NUM_RESULTS)
    print("Retrieved papers from arXiv")

    documents = []
    count = 0
    for paper in papers:
        count += 1
        print("Collecting data from PDFs")
        # r = requests.get(paper["link"])
        # pdf_file = io.BytesIO(r.content)
        # pdfReader = PyPDF2.PdfReader(pdf_file)
        # count = len(pdfReader.pages)
        # texts = []
        # for i in range(count):
        #     page = pdfReader.pages[i]
        #     texts.append(page.extract_text())
        texts = [paper["summary"]]
            
        embedding = get_embedding(texts)
        documents.append({"id": f"paper{count}",
                            "title": paper["title"], 
                            "authors": paper["authors"],
                            "embedding": embedding,
                            "link": paper["link"]})

    return documents, len(documents[0]["embedding"])

def create_pinecone_index(documents, embedding_dimension):
    pc = Pinecone(
        api_key=os.environ['PINECONE_API_KEY']
    )

    # Name your index
    index_name = 'research-papers'

    pc.delete_index(name = index_name)

    # Check if the index exists
    if index_name not in pc.list_indexes():
        # Create the index if it doesn't exist
        pc.create_index(name=index_name, 
                        dimension=embedding_dimension,
                        metric='euclidean',
                        spec=ServerlessSpec(
                            cloud='aws',
                            region='us-west-2'
                        ))
        
    # Connect to your index
    index = pc.Index(name=index_name)

    # Index documents
    for doc in documents:
        index.upsert(vectors=[(doc['link'], doc['embedding'])], 
                     metadata={'title': doc['title'], 'authors': doc['authors'], 'link': doc['link']})

    print("Indexing complete.")

def main():
    documents, embedding_dimension = construct_embedding_dict("Large Language Models")
    create_pinecone_index(documents, embedding_dimension)

if __name__ == "__main__":
    main()
