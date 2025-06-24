from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration de la base de données
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://anpr_user:anpr_password@localhost:5432/anpr_db"
)

# Création du moteur SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    poolclass=StaticPool,
    pool_pre_ping=True,
    echo=os.getenv("SQL_DEBUG", "false").lower() == "true"
)

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()

# Fonction pour obtenir la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 