from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# Variables d'environnement
RASPBERRY_URL = os.getenv("RASPBERRY_URL", "https://raspberrypi.tail01ac99.ts.net/reserver")
RASPBERRY_SECRET = os.getenv("RASPBERRY_SECRET")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/reserver")
def reserver_page():
    return render_template("reserver.html")

@app.route("/emporter")
def emporter():
    return render_template("pizza_a_emporter.html")

@app.route("/reserver", methods=["POST"])
def reserver():
    data = request.json

    if data.get("website"):
        return jsonify({"error": "Bot détecté"}), 403

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {RASPBERRY_SECRET}"
    }

    try:
        response = requests.post(RASPBERRY_URL, headers=headers, json=data)
        if response.status_code == 200:
            return jsonify({"success": True})
        else:
            return jsonify({"error": "Erreur Raspberry"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
