import requests

BASE_URL = "http://127.0.0.1:5000/api"

# ------------------- Mission A : Inventory -------------------
conditions = ["Cancer", "Diabetes", "Asthma", "Hypertension", "COVID-19", "Alzheimer"]
countries = ["France", "UK", "USA", "Germany", "Japan", "Australia"]

print("=== Test Inventory par Condition ===")
for condition in conditions:
    r = requests.get(f"{BASE_URL}/inventory", params={"condition": condition, "limit": 10})
    print(f"Condition: {condition} -> Status: {r.status_code}, Nombre de résultats: {len(r.json().get('data', []))}")

print("\n=== Test Inventory par Country ===")
for country in countries:
    r = requests.get(f"{BASE_URL}/inventory", params={"country": country, "limit": 10})
    print(f"Country: {country} -> Status: {r.status_code}, Nombre de résultats: {len(r.json().get('data', []))}")

print("\n=== Test Inventory Condition + Country ===")
for condition in conditions:
    for country in countries:
        r = requests.get(f"{BASE_URL}/inventory", params={"condition": condition, "country": country, "limit": 10})
        print(f"{condition} in {country} -> Status: {r.status_code}, Nombre de résultats: {len(r.json().get('data', []))}")

# ------------------- Mission B : Trial Details -------------------
print("\n=== Test Trial Details ===")
sample_ncts = ["NCT0001", "NCT0002", "NCT0003"]
for nct in sample_ncts:
    r = requests.get(f"{BASE_URL}/trial/{nct}")
    print(f"{nct} -> Status: {r.status_code}, Data Keys: {list(r.json().get('data', {}).keys())}")

# ------------------- Mission C : Targeted Search -------------------
print("\n=== Test Targeted Search ===")
for condition in ["Cancer", "Diabetes"]:
    r = requests.get(f"{BASE_URL}/search", params={"condition": condition, "limit": 5})
    print(f"Search '{condition}' -> Status: {r.status_code}, Nombre de résultats: {len(r.json().get('data', []))}")

# ------------------- Mission D : Trial Arms -------------------
print("\n=== Test Trial Arms ===")
for nct in sample_ncts:
    r = requests.get(f"{BASE_URL}/trial/{nct}/arms")
    print(f"{nct} Arms -> Status: {r.status_code}, Nombre de bras: {len(r.json().get('data', []))}")

# ------------------- Mission E : Trial Locations -------------------
print("\n=== Test Trial Locations ===")
for nct in sample_ncts:
    r = requests.get(f"{BASE_URL}/trial/{nct}/locations")
    print(f"{nct} Locations -> Status: {r.status_code}, Nombre de locations: {len(r.json().get('data', []))}")

# ------------------- Mission F : Trial Sponsors -------------------
print("\n=== Test Trial Sponsors ===")
for nct in sample_ncts:
    r = requests.get(f"{BASE_URL}/trial/{nct}/sponsors")
    print(f"{nct} Sponsors -> Status: {r.status_code}, Nombre de sponsors: {len(r.json().get('data', []))}")
