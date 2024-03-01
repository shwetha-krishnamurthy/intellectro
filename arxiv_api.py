import io
import PyPDF2
import requests

# Replace with the actual API endpoint URL
api_url = "http://arxiv.org/pdf/2208.00733v1"

def get_data_from_api(api_url):
  r = requests.get(api_url)
  f = io.BytesIO(r.content)
  
  reader = PyPDF2.PdfReader(f) 
  count = len(reader.pages)
  
  contents = reader._get_page(0).extract_text()

  for i in range(1, count):
    contents += reader._get_page(i).extract_text()

  return contents
  