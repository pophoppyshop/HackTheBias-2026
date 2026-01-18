import requests

url = "https://hackthebias-2026.onrender.com/items/"

data = {
    "Title": "Breaking News!",
    "Content": "Aliens have landed in New York City."
}

response = requests.post(url, json=data)

print("Status code:", response.status_code)
print("Response text:", response.text)

# Only try JSON if status code is 200
if response.status_code == 200:
    print(response.json())
