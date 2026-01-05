from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import csv
import math

app = Flask(__name__)
CORS(app)

# -----------------------------
# LOAD LIMITED CITY DATA
# -----------------------------
cities = []

with open("cities.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cities.append({
            "name": row["name"],
            "lat": float(row["latitude"]),
            "lon": float(row["longitude"]),
            "co2": float(row["co2"]),          # optional (city-specific)
            "population": int(row["population"]),
            "zone": row["zone"]
        })

# -----------------------------
# CO2 ESTIMATION FUNCTION
# -----------------------------
def estimate_co2(lat, lon):
    """
    Estimate atmospheric CO2 concentration (ppm)
    using global baseline + geographic proxy.
    """

    # Global average atmospheric CO2 (approx current)
    base_ppm = 420.0

    # Simple geographic/urban proxy
    latitude_factor = (abs(lat) / 90) * 12
    longitude_factor = (abs(lon) / 180) * 6

    co2_ppm = base_ppm + latitude_factor + longitude_factor

    # Zone classification
    if co2_ppm > 430:
        zone = "Red"
    elif co2_ppm > 410:
        zone = "Orange"
    else:
        zone = "Green"

    return round(co2_ppm, 2), zone

# -----------------------------
# ROUTES
# -----------------------------

@app.route("/")
def home():
    return "CO2 Digital Twin Backend Running"

@app.route("/map")
def map_page():
    return render_template("index.html")

@app.route("/cities")
def get_cities():
    return jsonify(cities)

@app.route("/estimate")
def estimate():
    lat = float(request.args.get("lat"))
    lon = float(request.args.get("lon"))

    co2_ppm, zone = estimate_co2(lat, lon)

    return jsonify({
        "latitude": lat,
        "longitude": lon,
        "co2_ppm": co2_ppm,
        "zone": zone,
        "unit": "ppm"
    })

# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run()

