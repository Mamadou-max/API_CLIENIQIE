from pydantic_settings import BaseSettings
from pydantic import Field
import secrets


class Settings(BaseSettings):
    #  URL de base de l'API ClinicalTrials.gov
    CT_GOV_BASE_URL: str = Field(
        default="https://clinicaltrials.gov/api/v2/studes",
        description="Base URL pour ClinicalTrials.gov API"
    )

    #  URL de la base de données (ex: postgresql://user:pass@localhost:5432/dbname)
    DATABASE_URL: str = Field(
        default="postgresql://user:password@localhost:5432/dbname",
        description="Chaîne de connexion à la base de données"
    )

    #  Clé API pour le géocodage (peut être None si pas utilisée)
    GEOCODING_API_KEY: str | None = Field(
        default=None,
        description="AIzaSyDZjakPMwx9Wz7UdpvzmuInuCximOGfKGI"
    )

    #  Variables de configuration Flask
    FLASK_ENV: str = Field(default="development", description="Mode Flask (dev/prod)")
    FLASK_DEBUG: bool = Field(default=True, description="Activer le mode debug Flask")
    SECRET_KEY: str = Field(
        default_factory=lambda: secrets.token_hex(32),
        description="Clé secrète Flask pour sécuriser les sessions"
    )

    class Config:
        env_file = ".env"
        case_sensitive = False  # Accepte FLASK_ENV ou flask_env
        extra = "ignore"        # Ignore les variables en trop dans .env


#  Charger les paramètres
settings = Settings()

# (Optionnel) Debug : afficher les valeurs chargées au démarrage
if settings.FLASK_DEBUG:
    print(" Configuration chargée :")
    print(f"CT_GOV_BASE_URL = {settings.CT_GOV_BASE_URL}")
    print(f"DATABASE_URL    = {settings.DATABASE_URL}")
    print(f"GEOCODING_API_KEY défini ? {'' if settings.GEOCODING_API_KEY else ''}")
    print(f"FLASK_ENV       = {settings.FLASK_ENV}")
    print(f"FLASK_DEBUG     = {settings.FLASK_DEBUG}")
    print(f"SECRET_KEY défini ? {'' if settings.SECRET_KEY else ''}")
