import io
import PyPDF2
import requests

def get_data_from_api(api_url):
  r = requests.get(api_url)
  f = io.BytesIO(r.content)
  
  reader = PyPDF2.PdfReader(f) 
  count = len(reader.pages)
  
  contents = reader._get_page(0).extract_text()

  for i in count:
    contents += reader._get_page(i).extract_text()

  return contents
  