import requests
import logging

logger = logging.getLogger(__name__)

BASE_URL_STUDY_FIELDS = "https://clinicaltrials.gov/api/query/study_fields"
BASE_URL_FULL_STUDY = "https://clinicaltrials.gov/api/query/full_studies"

FIELDS_INVENTORY = [
    "NCTId", "BriefTitle", "Condition", "InterventionName",
    "OverallStatus", "StartDate", "CompletionDate",
    "LocationCountry", "LocationCity", "LocationFacility"
]

class ClinicalTrialsService:

    @staticmethod
    def get_inventory(limit=50, country=None, condition=None):
        if not country and not condition:
            return []

        expr_parts = []
        if country:
            expr_parts.append(f'AREA[LocationCountry]{country}')
        if condition:
            expr_parts.append(f'"{condition}"')
        expr = " AND ".join(expr_parts)

        params = {
            "expr": expr,
            "fields": ",".join(FIELDS_INVENTORY),
            "max_rnk": limit,
            "fmt": "json"
        }

        try:
            logger.info(f"[Inventory] Fetching expr='{expr}'")
            res = requests.get(BASE_URL_STUDY_FIELDS, params=params, timeout=10)
            res.raise_for_status()
            return res.json().get("StudyFieldsResponse", {}).get("StudyFields", [])
        except requests.RequestException as e:
            logger.warning(f"[Inventory] API failed: {e}")
            return []

    @staticmethod
    def get_trial_details(nct_id):
        if not nct_id:
            return []
        params = {"expr": nct_id, "fmt": "json"}
        try:
            res = requests.get(BASE_URL_FULL_STUDY, params=params, timeout=10)
            res.raise_for_status()
            return res.json().get("FullStudiesResponse", {}).get("FullStudies", [])
        except requests.RequestException as e:
            logger.warning(f"[Trial Details] API failed for {nct_id}: {e}")
            return []

    @staticmethod
    def targeted_search(condition, limit=50):
        return ClinicalTrialsService.get_inventory(limit=limit, condition=condition)

    @staticmethod
    def get_trial_arms(nct_id):
        fields = ["NCTId", "ArmGroupDescription", "InterventionName"]
        params = {"expr": nct_id, "fields": ",".join(fields), "fmt": "json"}
        try:
            res = requests.get(BASE_URL_STUDY_FIELDS, params=params, timeout=10)
            res.raise_for_status()
            return res.json().get("StudyFieldsResponse", {}).get("StudyFields", [])
        except requests.RequestException as e:
            logger.warning(f"[Trial Arms] API failed for {nct_id}: {e}")
            return []

    @staticmethod
    def get_trial_locations(nct_id):
        fields = ["NCTId", "LocationFacility", "LocationCity", "LocationCountry", "LocationZip"]
        params = {"expr": nct_id, "fields": ",".join(fields), "fmt": "json"}
        try:
            res = requests.get(BASE_URL_STUDY_FIELDS, params=params, timeout=10)
            res.raise_for_status()
            return res.json().get("StudyFieldsResponse", {}).get("StudyFields", [])
        except requests.RequestException as e:
            logger.warning(f"[Trial Locations] API failed for {nct_id}: {e}")
            return []

    @staticmethod
    def get_trial_sponsors(nct_id):
        fields = [
            "NCTId", "LeadSponsorName", "CollaboratorName",
            "OverallOfficialName", "OverallOfficialRole", "ResponsibleParty"
        ]
        params = {"expr": nct_id, "fields": ",".join(fields), "fmt": "json"}
        try:
            res = requests.get(BASE_URL_STUDY_FIELDS, params=params, timeout=10)
            res.raise_for_status()
            return res.json().get("StudyFieldsResponse", {}).get("StudyFields", [])
        except requests.RequestException as e:
            logger.warning(f"[Trial Sponsors] API failed for {nct_id}: {e}")
            return []
