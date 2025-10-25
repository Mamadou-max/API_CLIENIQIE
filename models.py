from sqlalchemy import Column, Integer, String, JSON, DateTime, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# Modèle pour l'inventaire global (Mission A)
class ClinicalTrial(Base):
    __tablename__ = "clinical_trials"
    id = Column(Integer, primary_key=True, index=True)
    nct_id = Column(String(20), unique=True, index=True)
    title = Column(String(500))
    conditions = Column(JSON)  # Liste de conditions
    interventions = Column(JSON)  # Liste d'interventions
    status = Column(String(50))
    start_date = Column(Date)
    completion_date = Column(Date)
    locations = Column(JSON)  # Liste de localisations
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Modèle pour les détails complets (Mission B)
class TrialDetails(Base):
    __tablename__ = "trial_details"
    id = Column(Integer, primary_key=True, index=True)
    nct_id = Column(String(20), unique=True, index=True)
    full_data = Column(JSON)  # Toutes les données détaillées
    eligibility_criteria = Column(JSON)  # Critères d'éligibilité
    arms = Column(JSON)  # Bras d'essai
    created_at = Column(DateTime, default=datetime.utcnow)

# Modèle pour les recherches ciblées (Mission C)
class TargetedSearch(Base):
    __tablename__ = "targeted_searches"
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String(255))  # Mot-clé de recherche (ex: "diabetes")
    results = Column(JSON)  # Résultats de la recherche
    created_at = Column(DateTime, default=datetime.utcnow)

# Modèle pour les bras/interventions (Mission D)
class TrialArms(Base):
    __tablename__ = "trial_arms"
    id = Column(Integer, primary_key=True, index=True)
    nct_id = Column(String(20), index=True)
    arms = Column(JSON)  # Détails des bras d'essai
    created_at = Column(DateTime, default=datetime.utcnow)

# Modèle pour les localisations (Mission E)
class TrialLocation(Base):
    __tablename__ = "trial_locations"
    id = Column(Integer, primary_key=True, index=True)
    nct_id = Column(String(20), index=True)
    facility = Column(String(255))
    city = Column(String(100))
    country = Column(String(100))
    zip_code = Column(String(20))
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

# Modèle pour les sponsors (Mission F)
class TrialSponsor(Base):
    __tablename__ = "trial_sponsors"
    id = Column(Integer, primary_key=True, index=True)
    nct_id = Column(String(20), index=True)
    lead_sponsor = Column(String(255))
    collaborators = Column(JSON)  # Liste de collaborateurs
    contacts = Column(JSON)  # Liste de contacts
    created_at = Column(DateTime, default=datetime.utcnow)
