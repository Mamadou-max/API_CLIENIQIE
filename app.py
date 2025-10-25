from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from services.clinical_trials import ClinicalTrialsService
from services.preprocessor import Preprocessor
from services.database import (
    init_db, save_clinical_trial, save_trial_details,
    save_targeted_search, save_trial_arms,
    save_trial_locations, save_trial_sponsors
)
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
init_db()

@app.route("/")
def home():
    return render_template("index.html")


# ------------------- Mission A : Inventaire -------------------
@app.route("/api/inventory", methods=["GET"])
def get_inventory():
    limit = max(1, request.args.get("limit", 50, type=int))
    country = request.args.get("country", "").strip()
    condition = request.args.get("condition", "").strip()
    status_filter = request.args.get("status", "").strip()

    if not country and not condition:
        return jsonify({"status": "error", "message": "Au moins un filtre 'country' ou 'condition' est requis"}), 400

    try:
        data = ClinicalTrialsService.get_inventory(limit=limit, country=country, condition=condition) or []
        processed_data = Preprocessor.process_inventory(data) or []

        # Normalisation
        normalized = []
        for t in processed_data:
            normalized.append({
                "NCTId": t.get("NCTId", "N/A"),
                "Title": t.get("Title", "N/A"),
                "Condition": t.get("Condition", "N/A"),
                "Interventions": t.get("Interventions", []),
                "Status": t.get("Status", "N/A"),
                "StartDate": t.get("StartDate", "N/A"),
                "CompletionDate": t.get("CompletionDate", "N/A"),
                "City": t.get("City", "N/A"),
                "Country": t.get("Country", "N/A"),
                "Locations": t.get("Locations", [])
            })

        if status_filter:
            normalized = [t for t in normalized if t["Status"].lower() == status_filter.lower()]

        for trial in normalized:
            save_clinical_trial(trial)

        return jsonify({"status": "success", "data": normalized})
    except Exception as e:
        logger.error(f"[Inventory] Erreur: {e}")
        return jsonify({"status": "success", "data": []})


# ------------------- Mission B : Détails d'un essai -------------------
@app.route("/api/trial/<string:nct_id>", methods=["GET"])
def get_trial_details(nct_id):
    nct_id = nct_id.strip()
    if not nct_id:
        return jsonify({"status": "error", "message": "NCT ID requis"}), 400
    try:
        data = ClinicalTrialsService.get_trial_details(nct_id) or []
        processed = Preprocessor.process_details(data) or {}

        defaults = {
            "nct_id": nct_id,
            "Title": "N/A",
            "Condition": "N/A",
            "Status": "N/A",
            "StartDate": "N/A",
            "CompletionDate": "N/A",
            "Interventions": [],
            "Arms": [],
            "Locations": [],
            "Sponsors": []
        }
        defaults.update(processed)
        save_trial_details(defaults)
        return jsonify({"status": "success", "data": defaults})
    except Exception as e:
        logger.error(f"[Trial Details] Erreur pour {nct_id}: {e}")
        return jsonify({"status": "success", "data": {}})


# ------------------- Mission C : Recherche ciblée -------------------
@app.route("/api/search", methods=["GET"])
def targeted_search():
    condition = request.args.get("condition", "").strip()
    limit = max(1, request.args.get("limit", 50, type=int))
    if not condition:
        return jsonify({"status": "error", "message": "Le paramètre 'condition' est requis"}), 400
    try:
        data = ClinicalTrialsService.targeted_search(condition, limit) or []
        processed = Preprocessor.process_targeted_search(data) or []

        normalized = []
        for t in processed:
            normalized.append({
                "NCTId": t.get("NCTId", "N/A"),
                "Title": t.get("Title", "N/A"),
                "Condition": t.get("Condition", "N/A"),
                "Interventions": t.get("Interventions", []),
                "Status": t.get("Status", "N/A"),
                "StartDate": t.get("StartDate", "N/A"),
                "CompletionDate": t.get("CompletionDate", "N/A"),
                "City": t.get("City", "N/A"),
                "Country": t.get("Country", "N/A")
            })

        save_targeted_search(condition, normalized)
        return jsonify({"status": "success", "data": normalized})
    except Exception as e:
        logger.error(f"[Targeted Search] Erreur pour '{condition}': {e}")
        return jsonify({"status": "success", "data": []})


# ------------------- Mission D : Bras / Interventions -------------------
@app.route("/api/trial/<string:nct_id>/arms", methods=["GET"])
def get_trial_arms(nct_id):
    nct_id = nct_id.strip()
    if not nct_id:
        return jsonify({"status": "error", "message": "NCT ID requis"}), 400
    try:
        data = ClinicalTrialsService.get_trial_arms(nct_id) or []
        processed = Preprocessor.process_arms(data) or []

        if not processed:
            processed = [{"ArmGroupDescription": "N/A", "InterventionName": "N/A"}]

        save_trial_arms(nct_id, processed)
        return jsonify({"status": "success", "data": processed})
    except Exception as e:
        logger.error(f"[Trial Arms] Erreur pour {nct_id}: {e}")
        return jsonify({"status": "success", "data": []})


# ------------------- Mission E : Localisations -------------------
@app.route("/api/trial/<string:nct_id>/locations", methods=["GET"])
def get_trial_locations(nct_id):
    nct_id = nct_id.strip()
    if not nct_id:
        return jsonify({"status": "error", "message": "NCT ID requis"}), 400
    try:
        data = ClinicalTrialsService.get_trial_locations(nct_id) or []
        processed = Preprocessor.process_locations(data, nct_id) or []

        if not processed:
            processed = [{"LocationFacility": "N/A", "City": "N/A", "Country": "N/A", "Zip": "N/A"}]

        save_trial_locations(processed)
        return jsonify({"status": "success", "data": processed})
    except Exception as e:
        logger.error(f"[Trial Locations] Erreur pour {nct_id}: {e}")
        return jsonify({"status": "success", "data": []})


# ------------------- Mission F : Sponsors -------------------
@app.route("/api/trial/<string:nct_id>/sponsors", methods=["GET"])
def get_trial_sponsors(nct_id):
    nct_id = nct_id.strip()
    if not nct_id:
        return jsonify({"status": "error", "message": "NCT ID requis"}), 400
    try:
        data = ClinicalTrialsService.get_trial_sponsors(nct_id) or []
        processed = Preprocessor.process_sponsors(data) or []

        if not processed:
            processed = [{"LeadSponsorName": "N/A", "CollaboratorName": [], "ResponsibleParty": "N/A"}]

        save_trial_sponsors(nct_id, processed)
        return jsonify({"status": "success", "data": processed})
    except Exception as e:
        logger.error(f"[Trial Sponsors] Erreur pour {nct_id}: {e}")
        return jsonify({"status": "success", "data": []})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
