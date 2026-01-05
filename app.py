from flask import Flask, jsonify,render_template
from flask_cors import CORS
import csv

app = Flask(__name__)
CORS(app)

cities_data = {}

# Load CSV
with open("cities.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    print("CSV columns:", reader.fieldnames)  # debug

    for row in reader:
        if not row.get("name"):
            continue

        city_name = row["name"].strip().lower()

        cities_data[city_name] = {
            "name": row["name"],
            "latitude": float(row["latitude"]),
            "longitude": float(row["longitude"]),
            "co2": row.get("co2", "N/A")
        }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/cities")
def get_cities():
    cities = []
    with open("cities.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cities.append(row)
    return jsonify(cities)

@app.route("/api/city/<name>")
def get_city(name):
    key = name.lower()
    if key in cities_data:
        return jsonify(cities_data[key])
    return jsonify({"error": "City not found"}), 404

if __name__ == "__main__":
    app.run()
