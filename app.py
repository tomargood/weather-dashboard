from flask import Flask, render_template
from pathlib import Path
from rich import print_json
import requests
import json

app = Flask(__name__)

API_KEY_PATH = Path("API_keys/avwxkeys.txt")
URL = "https://avwx.rest/api/metar/KSKA?remove=true"
URL1 = "https://avwx.rest/api/station/KSKA"


app.config["API_KEY"] = API_KEY_PATH.read_text().strip()
token = app.config["API_KEY"]
headers = {
    "Authorization": f"Bearer {token}",   # Or "TOKEN <token>"
    "Accept": "application/json"
}

response = requests.get(URL, headers=headers, timeout=10)
response.raise_for_status()
data = response.json()
FlightRules = data["flight_rules"]
Arpt = data["station"]

response1 = requests.get(URL1, headers=headers, timeout=10)
response1.raise_for_status()
data1 = response1.json()
ArptName = data1["name"]





@app.route("/")
def home():
    return render_template("page.html", rules=FlightRules, arpt = Arpt, ArptName = ArptName)

if __name__ == "__main__":
    app.run(debug=True)