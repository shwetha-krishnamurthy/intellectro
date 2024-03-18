import requests
import xml.etree.ElementTree as ET

def get_papers_from_arXiv(query, n):
    # URL for the arXiv API query
    url = "http://export.arxiv.org/api/query?search_query=all:"+query.replace(" ", "+").lower()+"&start=0&max_results="+str(n)

    # Make the GET request to arXiv API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        print("Call was successful")
        # Parse the XML response
        root = ET.fromstring(response.content)

        # Initialize an empty list to store paper details
        papers = []

        # Namespace to parse the XML properly
        namespace = {'arxiv': 'http://www.w3.org/2005/Atom'}

        # Iterate over each entry (paper) in the response
        for entry in root.findall('arxiv:entry', namespace):
            # Extract paper details
            paper_dict = {
                'title': entry.find('arxiv:title', namespace).text.strip(),
                'summary': entry.find('arxiv:summary', namespace).text.strip(),
                'published': entry.find('arxiv:published', namespace).text.strip(),
                'authors': [author.find('arxiv:name', namespace).text for author in entry.findall('arxiv:author', namespace)],
                'link': entry.find('arxiv:link[@title="pdf"]', namespace).attrib['href'] if entry.find('arxiv:link[@title="pdf"]', namespace) is not None else None
            }
            # Add the paper dictionary to the list
            papers.append(paper_dict)
    else:
        print(f"Failed to fetch data: {response.status_code}")
        papers = []

    # Print the result or do further processing
    return(papers)


if __name__ == "__main__":
    get_papers_from_arXiv("quantum computing", 1)
