import requests
import os

url = 'http://127.0.0.1:5000/convert'
file_path = './file_path.pdf' # Change this to the path of the PDF file you want to convert

if not os.path.exists(file_path):
    print(f"File {file_path} does not exist.")
    exit(1)

with open(file_path, 'rb') as f:
    files = {'file': f}
    response = requests.post(url, files=files)

if response.status_code == 200:
    print("Request was successful.")
    print("Response JSON:")
    print(response.json())
else:
    print(f"Request failed with status code {response.status_code}")
    print("Response JSON:")
    print(response.json())