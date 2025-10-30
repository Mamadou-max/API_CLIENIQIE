from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Base, ClinicalTrial, TrialDetails, TargetedSearch, TrialArms, TrialLocation, TrialSponsor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)
CORS(app)

# DB setup
engine = create_engine("sqlite:///clinical_trials.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

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
        query = session.query(ClinicalTrial)

        if condition:
            query = query.filter(func.json_extract(ClinicalTrial.conditions, '$[0]') == condition)

        if country:
            query = query.filter(func.json_extract(ClinicalTrial.locations, '$[0].country') == country)

        if status_filter:
            query = query.filter(ClinicalTrial.status == status_filter)

        trials = query.limit(limit).all()

        data = []
        for t in trials:
            data.append({
                "NCTId": t.nct_id,
                "Title": t.title,
                "Condition": t.conditions[0] if t.conditions else "N/A",
                "Interventions": t.interventions,
                "Status": t.status,
                "StartDate": str(t.start_date),
                "CompletionDate": str(t.completion_date),
                "Locations": t.locations
            })

        return jsonify({"status": "success", "data": data})
    except Exception as e:
        logger.error(f"[Inventory] Erreur: {e}")
        return jsonify({"status": "error", "data": []})

# ------------------- Mission B : Détails d'un essai -------------------
@app.route("/api/trial/<string:nct_id>", methods=["GET"])
def get_trial_details(nct_id):
    try:
        trial = session.query(TrialDetails).filter_by(nct_id=nct_id).first()
        if not trial:
            return jsonify({"status": "error", "message": f"Essai {nct_id} introuvable"}), 404

        return jsonify({"status": "success", "data": trial.full_data})
    except Exception as e:
        logger.error(f"[Trial Details] Erreur pour {nct_id}: {e}")
        return jsonify({"status": "error", "data": {}})

# ------------------- Mission C : Recherche ciblée -------------------
@app.route("/api/search", methods=["GET"])
def targeted_search():
    condition = request.args.get("condition", "").strip()
    limit = max(1, request.args.get("limit", 50, type=int))
    if not condition:
        return jsonify({"status": "error", "message": "Le paramètre 'condition' est requis"}), 400
    try:
        trials = session.query(ClinicalTrial).filter(
            func.json_extract(ClinicalTrial.conditions, '$[0]') == condition
        ).limit(limit).all()

        data = [{
            "NCTId": t.nct_id,
            "Title": t.title,
            "Condition": t.conditions[0] if t.conditions else "N/A",
            "Interventions": t.interventions,
            "Status": t.status,
            "StartDate": str(t.start_date),
            "CompletionDate": str(t.completion_date),
            "Locations": t.locations
        } for t in trials]

        return jsonify({"status": "success", "data": data})
    except Exception as e:
        logger.error(f"[Targeted Search] Erreur pour '{condition}': {e}")
        return jsonify({"status": "error", "data": []})

# ------------------- Mission D : Bras / Interventions -------------------
@app.route("/api/trial/<string:nct_id>/arms", methods=["GET"])
def get_trial_arms(nct_id):
    try:
        trial_arms = session.query(TrialArms).filter_by(nct_id=nct_id).first()
        data = trial_arms.arms if trial_arms else [{"ArmGroupDescription": "N/A", "InterventionName": "N/A"}]
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        logger.error(f"[Trial Arms] Erreur pour {nct_id}: {e}")
        return jsonify({"status": "error", "data": []})

# ------------------- Mission E : Localisations -------------------
@app.route("/api/trial/<string:nct_id>/locations", methods=["GET"])
def get_trial_locations(nct_id):
    try:
        locations = session.query(TrialLocation).filter_by(nct_id=nct_id).all()
        data = [{
            "Facility": l.facility or "N/A",
            "City": l.city or "N/A",
            "Country": l.country or "N/A",
            "Zip": l.zip_code or "N/A",
            "Latitude": l.latitude or "N/A",
            "Longitude": l.longitude or "N/A"
        } for l in locations] or [{"Facility": "N/A", "City": "N/A", "Country": "N/A"}]

        return jsonify({"status": "success", "data": data})
    except Exception as e:
        logger.error(f"[Trial Locations] Erreur pour {nct_id}: {e}")
        return jsonify({"status": "error", "data": []})

# ------------------- Mission F : Sponsors -------------------
@app.route("/api/trial/<string:nct_id>/sponsors", methods=["GET"])
def get_trial_sponsors(nct_id):
    try:
        sponsors = session.query(TrialSponsor).filter_by(nct_id=nct_id).all()
        data = [{
            "LeadSponsor": s.lead_sponsor or "N/A",
            "Collaborators": s.collaborators or [],
            "Contacts": s.contacts or []
        } for s in sponsors] or [{"LeadSponsor": "N/A", "Collaborators": [], "Contacts": []}]
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        logger.error(f"[Trial Sponsors] Erreur pour {nct_id}: {e}")
        return jsonify({"status": "error", "data": []})

# ------------------- Run Flask -------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
