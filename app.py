from flask import Flask, render_template, request
from pathlib import Path
from rich import print_json
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY_PATH = Path("API_keys/avwxkeys.txt")
app.config["API_KEY"] = API_KEY_PATH.read_text().strip()
token = app.config["API_KEY"]

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

def get_weather_data(airport):
    """Fetch weather data for specified airport"""
    # URLs with dynamic airport
    url_metar = f"https://avwx.rest/api/metar/{airport}?remove=true"
    url_station = f"https://avwx.rest/api/station/{airport}"
    url_taf = f"https://avwx.rest/api/taf/{airport}"
    
    # Get METAR API info
    try:
        response = requests.get(url_metar, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        print("\n=== METAR RESPONSE ===")
        print_json(data=data)
    except requests.exceptions.RequestException as e:
        print(f"\n=== METAR ERROR for {airport} ===")
        print(f"Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response text: {e.response.text}")
        return {"error": f"Could not retrieve METAR data for {airport}. The airport code may be invalid or the METAR service is unavailable."}
    
    # Get Airport Name/Info
    try:
        response1 = requests.get(url_station, headers=headers, timeout=10)
        response1.raise_for_status()
        data1 = response1.json()
        print("\n=== STATION RESPONSE ===")
        print_json(data=data1)
        arpt_name = data1["name"]
        
        # Get coordinates for nearby search
        latitude = data1.get("latitude")
        longitude = data1.get("longitude")
    except requests.exceptions.RequestException:
        arpt_name = airport  # Fallback to airport code
        latitude = None
        longitude = None
    
    # Get TAF (not all airports have TAF)
    try:
        response2 = requests.get(url_taf, headers=headers, timeout=10)
        response2.raise_for_status()
        data2 = response2.json()
        print("\n=== TAF RESPONSE ===")
        print_json(data=data2)
        tafdict = data2["forecast"]
        tafraw = [line["sanitized"] for line in tafdict]
    except (requests.exceptions.RequestException, KeyError):
        # No TAF available for this airport
        tafraw = ["TAF not available for this airport"]
    
    # Setting variables from json response
    arpt = data["station"]
    flight_rules = data["flight_rules"]
    vis = data["visibility"]["repr"]
    cig = data["clouds"]  # This is the array of cloud layer objects
    px = data["altimeter"]["value"]
    temp = data["temperature"]["value"]
    dewpt = data["dewpoint"]["value"]
    wind = data["wind_speed"]["value"]
    gust = data["wind_gust"]
    winddir = data["wind_direction"]["value"]
    pa = data["pressure_altitude"]
    da = data["density_altitude"]
    
    # Gather cloud layers into array for display
    cloudlayers = [layer["repr"] for layer in cig]
    
    # Aarow logic, must be reciprocal though, since wind is from that direction, not to
    if winddir >= 180:
        aarowdir = str(winddir-180) + "deg"
    else: 
        aarowdir = str(winddir+180) + "deg"
    
    # Weather observation code logic
    wxcodes = data["wx_codes"]
    wxcode = [code["repr"] for code in wxcodes]
    maincode = wxcodes[0]["value"] if wxcodes else None
    
    # Check if sky is truly clear (no wx codes and check ceiling)
    if maincode is None or maincode == "":
        # Check cloud altitudes - altitude is in hundreds of feet
        has_low_clouds = False
        for layer in cig:
            if layer.get("altitude") is not None and layer["altitude"] < 100:
                has_low_clouds = True
                break
        
        if has_low_clouds:
            maincode = "CLOUDY"
        else:
            maincode = "SKY CLEAR"

    # Update Time Logic
    ts = data["time"]["dt"]
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    updatetime = dt.strftime("%Y-%m-%d %H:%M:%S %Z")
    
    return {
        "tafraw": tafraw,
        "time": updatetime,
        "aarowdir": aarowdir,
        "rules": flight_rules,
        "arpt": arpt,
        "ArptName": arpt_name,
        "vis": vis,
        "cig": cloudlayers,
        "px": px,
        "temp": temp,
        "dewpt": dewpt,
        "wind": wind,
        "gust": gust,
        "winddir": winddir,
        "wxcode": wxcode,
        "pa": pa,
        "da": da,
        "obs": maincode,
    }

@app.route("/")
def home():
    # Get airport from query parameter, default to KSKA
    airport = request.args.get('airport', 'KSKA').upper()
    
    weather_data = get_weather_data(airport)
    
    # Check if data was returned
    if weather_data is None:
        return f"<h1>Error</h1><p>Could not fetch weather data for {airport}</p><p></p>", 500
    
    # Check if there's an error
    if "error" in weather_data:
        return f"<h1>Error</h1><p>{weather_data['error']}</p><p><a href='/'>Try another airport</a></p>", 404
    
    return render_template("page.html", **weather_data)

if __name__ == "__main__":
    app.run(debug=True)