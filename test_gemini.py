import json
import urllib.request
import urllib.error

API_KEY = "AIzaSyDvam3ohesx6LdqW6-x-p_rP9QfhpZCLxg"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

payload = {
    "contents": [{"parts": [{"text": "Hello, how are you?"}]}],
    "generationConfig": {
        "temperature": 0.7,
        "maxOutputTokens": 100,
    }
}

req = urllib.request.Request(
    URL,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST"
)

try:
    with urllib.request.urlopen(req) as response:
        print("Success!")
        print(json.loads(response.read()))
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print(e.read().decode("utf-8"))
except Exception as e:
    print(f"Error: {e}")
