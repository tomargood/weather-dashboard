from flask import Flask, render_template
from pathlib import Path
from rich import print_json
import requests
import json
from datetime import datetime


app = Flask(__name__)

AIRPORT = "KSKA"
API_KEY_PATH = Path("API_keys/avwxkeys.txt")
URL = f"https://avwx.rest/api/metar/{AIRPORT}?remove=true"
URL1 = f"https://avwx.rest/api/station/{AIRPORT}"
URL2 = f"https://avwx.rest/api/taf/{AIRPORT}"


app.config["API_KEY"] = API_KEY_PATH.read_text().strip()
token = app.config["API_KEY"]
headers = {
    "Authorization": f"Bearer {token}",   # Or "TOKEN <token>"
    "Accept": "application/json"
}

# # Get METAR API info
response = requests.get(URL, headers=headers, timeout=10)
response.raise_for_status()
data = response.json()



# # Get Airport Name/Info
response1 = requests.get(URL1, headers=headers, timeout=10)
response1.raise_for_status()
data1 = response1.json()

# Get TAF
response2 = requests.get(URL2, headers=headers, timeout=10)
response2.raise_for_status()
data2 = response2.json()

# setting variables from json responsse
# TODO i need to find a way to just run the api call to airport info once per airport change.
Arpt = data["station"]
FlightRules = data["flight_rules"]
ArptName = data1["name"]
Vis = data["visibility"]["repr"]
Cig = data["clouds"]
px = data["altimeter"]["value"]
temp = data["temperature"]["value"]
dewpt = data["dewpoint"]["value"]
wind = data["wind_speed"]["value"]
gust = data["wind_gust"]
winddir = data["wind_direction"]["value"]
wxcodes = data["wx_codes"]
pa = data["pressure_altitude"]
da = data["density_altitude"]
aarowdir = str(winddir)+"deg"
cloudlayers = [layer["repr"] for layer in Cig]
wxcode = [code["repr"] for code in wxcodes]
maincode = wxcodes[0]["value"]
ts = data["time"]["dt"]
dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
updatetime = dt.strftime("%Y-%m-%d %H:%M:%S %Z")
tafdict = data2["forecast"]

tafraw = [line["sanitized"] for line in tafdict]



@app.route("/")
def home():
    return render_template("page.html", tafraw = tafraw, time = updatetime, aarowdir = aarowdir, rules=FlightRules, arpt = Arpt, ArptName = ArptName, vis=Vis, cig=cloudlayers, px=px, temp=temp, dewpt=dewpt, wind=wind, gust=gust, winddir=winddir, wxcode=wxcode, pa=pa, da=da, obs = maincode)

if __name__ == "__main__":
    app.run(debug=True)