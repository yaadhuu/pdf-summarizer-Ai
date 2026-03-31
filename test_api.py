import requests
import json
import base64

# Create a dummy PDF with reportlab or just a very simple valid pdf
dummy_pdf_content = b'%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 53 >>\nstream\nBT\n/F1 24 Tf\n100 100 Td\n(This is a test PDF document) Tj\nET\nendstream\nendobj\ntrailer\n<< /Size 5 /Root 1 0 R >>\n%%EOF'

with open("test.pdf", "wb") as f:
    f.write(dummy_pdf_content)

url = "http://127.0.0.1:8000/upload-pdf/"
files = {'file': open("test.pdf", "rb")}
response = requests.post(url, files=files)
print("Upload Response:", response.status_code, response.text)

if response.status_code == 200:
    collection_name = response.json().get("collection_name")
    
    ask_url = f"http://127.0.0.1:8000/ask/?collection_name={collection_name}&question=What is this document?&mode=chat"
    ask_response = requests.post(ask_url)
    print("Ask Response:", ask_response.status_code, ask_response.text)
