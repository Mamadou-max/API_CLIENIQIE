# services/preprocessor.py

class Preprocessor:

    @staticmethod
    def process_inventory(raw_data):
        """
        Transforme les données brutes d'inventaire en format standard.
        """
        if not raw_data:
            return []

        processed = []
        for item in raw_data:
            processed.append({
                "NCTId": item.get("NCTId", "N/A"),
                "Title": item.get("BriefTitle", "N/A"),
                "Condition": item.get("Condition", ["N/A"])[0] if item.get("Condition") else "N/A",
                "Interventions": item.get("InterventionName", ["N/A"]),
                "Status": item.get("OverallStatus", "N/A"),
                "StartDate": item.get("StartDate", "N/A"),
                "CompletionDate": item.get("CompletionDate", "N/A"),
                "City": item.get("LocationCity", ["N/A"])[0] if item.get("LocationCity") else "N/A",
                "Country": item.get("LocationCountry", ["N/A"])[0] if item.get("LocationCountry") else "N/A",
                "Locations": []  # à remplir via get_trial_locations
            })
        return processed

    @staticmethod
    def process_details(raw_data):
        if not raw_data:
            return {}
        try:
            study = raw_data[0].get("Study", {})
            protocol = study.get("ProtocolSection", {})
            details = {
                "Title": protocol.get("IdentificationModule", {}).get("OfficialTitle", "N/A"),
                "Condition": protocol.get("ConditionsModule", {}).get("ConditionList", {}).get("Condition", ["N/A"]),
                "Status": protocol.get("StatusModule", {}).get("OverallStatus", "N/A"),
                "StartDate": protocol.get("StatusModule", {}).get("StartDateStruct", {}).get("StartDate", "N/A"),
                "CompletionDate": protocol.get("StatusModule", {}).get("CompletionDateStruct", {}).get("CompletionDate", "N/A"),
                "Interventions": protocol.get("ArmsInterventionsModule", {}).get("InterventionList", {}).get("InterventionName", []),
                "Arms": protocol.get("ArmsInterventionsModule", {}).get("ArmGroupList", {}).get("ArmGroupDescription", []),
                "Locations": [],
                "Sponsors": []
            }
            return details
        except Exception:
            return {}

    @staticmethod
    def process_targeted_search(raw_data):
        return Preprocessor.process_inventory(raw_data)

    @staticmethod
    def process_arms(raw_data):
        if not raw_data:
            return []
        processed = []
        for item in raw_data:
            processed.append({
                "ArmGroupDescription": item.get("ArmGroupDescription", "N/A"),
                "InterventionName": item.get("InterventionName", ["N/A"])
            })
        return processed

    @staticmethod
    def process_locations(raw_data, nct_id):
        if not raw_data:
            return []
        processed = []
        for item in raw_data:
            processed.append({
                "nct_id": nct_id,
                "City": item.get("LocationCity", ["N/A"])[0] if item.get("LocationCity") else "N/A",
                "Country": item.get("LocationCountry", ["N/A"])[0] if item.get("LocationCountry") else "N/A",
                "Facility": item.get("LocationFacility", ["N/A"])[0] if item.get("LocationFacility") else "N/A",
                "Zip": item.get("LocationZip", ["N/A"])[0] if item.get("LocationZip") else "N/A",
                "Latitude": item.get("LocationLat", 0.0),
                "Longitude": item.get("LocationLong", 0.0)
            })
        return processed

    @staticmethod
    def process_sponsors(raw_data):
        if not raw_data:
            return []
        processed = []
        for item in raw_data:
            processed.append({
                "LeadSponsorName": item.get("LeadSponsorName", "N/A"),
                "CollaboratorName": item.get("CollaboratorName", []),
                "ResponsibleParty": item.get("ResponsibleParty", "N/A")
            })
        return processed
