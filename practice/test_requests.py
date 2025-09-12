# test_requests.py
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

response = requests.get(url)

print("Status Code:", response.status_code)

if response.status_code == 200:
    data = response.json()
    print("✅ Success! Here is the title:")
    print("Title:", data["title"])
else:
    print("❌ Failed with status:", response.status_code)
