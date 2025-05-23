from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# Variables d'environnement
RASPBERRY_URL = os.getenv("RASPBERRY_URL", "https://raspberrypi.tail01ac99.ts.net/reserver")
RASPBERRY_SECRET = os.getenv("RASPBERRY_SECRET")


from flask import request, redirect

@app.before_request
def redirect_to_custom_domain():
    if request.host != "www.lasalentina.fr":
        return redirect(f"https://www.lasalentina.fr{request.full_path}", code=301)
    
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/api/reserver", methods=["POST"])
def api_reserver():
    try:
        data = request.get_json()
        print("✅ Réservation reçue :", data)

        # Traitement ici (ex : MQTT, email...)
        return jsonify({"message": "Réservation enregistrée", "success": True}), 200

    except Exception as e:
        print("❌ Erreur lors de la réservation :", e)
        return jsonify({"message": "Erreur interne", "success": False}), 500

@app.route("/emporter")
def emporter():
    return render_template("pizza_a_emporter.html")
@app.route("/reserver", methods=["GET", "POST"])
def reserver():
    if request.method == "GET":
        return render_template("reserver.html")

    try:
        data = request.get_json(force=True)
        print("✅ Données reçues :", data)

        if data.get("website"):
            print("❌ BOT détecté - champ caché rempli")
            return jsonify({"error": "Bot détecté"}), 403

        # Vérifie les variables d'environnement
        print("🔐 Clé reçue :", os.getenv("RASPBERRY_SECRET"))
        print("🌐 URL Raspberry :", os.getenv("RASPBERRY_URL"))

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('RASPBERRY_SECRET')}"
        }

        response = requests.post(os.getenv("RASPBERRY_URL"), headers=headers, json=data)
        print("🔄 Réponse Raspberry :", response.status_code, response.text)

        if response.status_code == 200:
            return jsonify({"success": True})
        else:
            return jsonify({"error": "Erreur Raspberry"}), 500

    except Exception as e:
        print("❗ Exception attrapée :", str(e))
        return jsonify({"error": f"Erreur serveur : {str(e)}"}), 500

