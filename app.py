from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

RASPBERRY_URL = "https://raspberrypi.tail01ac99.ts.net/reserver"
RASPBERRY_TOKEN = os.getenv("RASPBERRY_SECRET")  # stocké dans Render

@app.route("/reserver", methods=["POST"])
def reserver():
    data = request.json

    # Vérification anti-spam : champ invisible "website"
    if data.get("website"):  # rempli ? → bot
        return jsonify({"error": "Bot détecté"}), 403

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {RASPBERRY_TOKEN}"
    }

    try:
        response = requests.post(RASPBERRY_URL, headers=headers, json=data)
        if response.status_code == 200:
            return jsonify({"success": True})
        else:
            return jsonify({"error": "Erreur Raspberry"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
