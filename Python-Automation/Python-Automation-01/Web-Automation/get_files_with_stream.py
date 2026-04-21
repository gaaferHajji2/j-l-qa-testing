import requests

response = requests.get('https://arxiv.org/pdf/2501.00173', stream=True)
assert response.status_code >= 200 and response.status_code < 300
with open('file-01.pdf', 'wb') as f:
    for chunk in response.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)