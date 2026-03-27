import json
import urllib.request
import urllib.error

API_KEY = "AIzaSyDvam3ohesx6LdqW6-x-p_rP9QfhpZCLxg"
URL = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

try:
    with urllib.request.urlopen(URL) as response:
        models = json.loads(response.read())
        for model in models.get("models", []):
            print(model.get("name"))
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print(e.read().decode("utf-8"))
except Exception as e:
    print(f"Error: {e}")
