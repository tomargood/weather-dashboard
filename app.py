from flask import Flask, render_template
from pathlib import Path
from rich import print_json
import requests
import json

app = Flask(__name__)

API_KEY_PATH = Path("API_keys/avwxkeys.txt")
URL = "https://avwx.rest/api/metar/KSKA?remove=true"


app.config["API_KEY"] = API_KEY_PATH.read_text().strip()
token = app.config["API_KEY"]
headers = {
    "Authorization": f"Bearer {token}",   # Or "TOKEN <token>"
    "Accept": "application/json"
}

response = requests.get(URL, headers=headers, timeout=10)
response.raise_for_status()
data = response.json()
print_json(json.dumps(data))









# @app.route("/")
# def home():
#     return render_template("page.html")

# if __name__ == "__main__":
#     app.run(debug=True)