import io
import PyPDF2
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, parse_qs

def get_data_from_api(api_url):
  r = requests.get(api_url)
  f = io.BytesIO(r.content)
  
  reader = PyPDF2.PdfReader(f) 
  count = len(reader.pages)
  
  contents = reader._get_page(0).extract_text()

  for i in range(count):
    contents += reader._get_page(i).extract_text()

  return contents


def get_papers_from_arXiv(query, n):
    # URL for the arXiv API query
    url = "http://export.arxiv.org/api/query?search_query=all:"+query.replace(" ", "+").lower()+"&start=0&max_results="+str(n)

    # Make the GET request to arXiv API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
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


def get_paper_metadata_from_url(url):
    # The URL of the arXiv paper
    paper_url = url

    # Extract the paper ID from the URL
    paper_id = paper_url.split('/')[-1]

    # arXiv API endpoint for querying metadata
    arxiv_api_endpoint = "http://export.arxiv.org/api/query"

    # Parameters for the API request
    params = {
        "id_list": paper_id,
    }

    # Make the API request
    response = requests.get(arxiv_api_endpoint, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Process the response XML to extract metadata (this example just prints the raw XML)
        # Parse the XML response
        root = ET.fromstring(response.content)
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
    else:
        print("Failed to retrieve paper metadata. Status code:", response.status_code)
    
    return paper_dict

if __name__ == "__main__":
    get_paper_metadata_from_url("http://arxiv.org/pdf/2401.13303v1")
