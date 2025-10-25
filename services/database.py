# services/database.py
from sqlalchemy import create_engine, Column, String, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///clinical_trials.db"

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# ------------------- Models -------------------
class ClinicalTrial(Base):
    __tablename__ = "clinical_trials"
    id = Column(Integer, primary_key=True, index=True)
    NCTId = Column(String, unique=True, index=True)
    data = Column(JSON)

# ------------------- Initialization -------------------
def init_db():
    Base.metadata.create_all(bind=engine)

# ------------------- Save Functions -------------------
def save_clinical_trial(trial):
    if not trial or "NCTId" not in trial:
        return
    existing = session.query(ClinicalTrial).filter_by(NCTId=trial["NCTId"]).first()
    if existing:
        existing.data = trial
    else:
        session.add(ClinicalTrial(NCTId=trial["NCTId"], data=trial))
    session.commit()

def save_trial_details(details):
    save_clinical_trial(details)

def save_targeted_search(condition, trials):
    for t in trials:
        save_clinical_trial(t)

def save_trial_arms(nct_id, arms):
    trial = session.query(ClinicalTrial).filter_by(NCTId=nct_id).first()
    if trial:
        trial.data["Arms"] = arms
        session.commit()

def save_trial_locations(locations):
    for loc in locations:
        trial = session.query(ClinicalTrial).filter_by(NCTId=loc.get("nct_id")).first()
        if trial:
            trial.data["Locations"] = loc
            session.commit()

def save_trial_sponsors(nct_id, sponsors):
    trial = session.query(ClinicalTrial).filter_by(NCTId=nct_id).first()
    if trial:
        trial.data["Sponsors"] = sponsors
        session.commit()
