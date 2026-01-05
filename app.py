from flask import Flask, jsonify, render_template
from flask_cors import CORS
import csv
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# -----------------------------
# Load city data from CSV
# -----------------------------
CITIES = {}

CSV_FILE = "cities.csv"

if os.path.exists(CSV_FILE):
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            city_name = row["city"].strip().lower()
            CITIES[city_name] = {
                "city": row["city"],
                "lat": float(row["lat"]),
                "lon": float(row["lon"]),
                "co2_ppm": float(row["co2_ppm"]),
                "population": int(row["population"])
            }

# -----------------------------
# Helper: classify CO2 zone
# -----------------------------
def get_zone(ppm):
    if ppm < 400:
        return "green"
    elif 400 <= ppm <= 450:
        return "orange"
    else:
        return "red"

# -----------------------------
# Home route (frontend)
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")

# -----------------------------
# API: get all cities
# -----------------------------
@app.route("/api/cities")
def get_cities():
    output = []
    for city in CITIES.values():
        zone = get_zone(city["co2_ppm"])
        output.append({
            "city": city["city"],
            "lat": city["lat"],
            "lon": city["lon"],
            "co2_ppm": city["co2_ppm"],
            "zone": zone,
            "population": city["population"]
        })
    return jsonify(output)

# -----------------------------
# API: get single city by name
# -----------------------------
@app.route("/api/city/<city_name>")
def get_city(city_name):
    key = city_name.strip().lower()

    if key not in CITIES:
        return jsonify({"error": "City not found"}), 404

    city = CITIES[key]
    zone = get_zone(city["co2_ppm"])

    response = {
        "city": city["city"],
        "latitude": city["lat"],
        "longitude": city["lon"],
        "co2_ppm": city["co2_ppm"],
        "unit": "ppm",
        "zone": zone,
        "population": city["population"],
        "time": datetime.now().strftime("%d-%m-%Y %I:%M %p")
    }

    return jsonify(response)

# -----------------------------
# Run app (Render compatible)
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
