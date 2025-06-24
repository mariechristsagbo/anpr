#!/usr/bin/env python3
"""
Script d'initialisation de la base de données ANPR
Créé les tables et insère les données initiales
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au path Python
sys.path.append(str(Path(__file__).parent))

from database import engine, SessionLocal
from models import Base, User, Camera, Vehicle
from models.user import UserRole
from passlib.context import CryptContext

# Configuration du hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_tables():
    """Créé toutes les tables de la base de données"""
    print("🔧 Création des tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées avec succès!")

def create_admin_user():
    """Créé un utilisateur administrateur par défaut"""
    print("👤 Création de l'utilisateur administrateur...")
    
    db = SessionLocal()
    try:
        # Vérifier si l'admin existe déjà
        admin = db.query(User).filter(User.email == "admin@anpr.bj").first()
        if admin:
            print("⚠️  L'utilisateur administrateur existe déjà")
            return
        
        # Créer l'utilisateur admin
        admin_user = User(
            email="admin@anpr.bj",
            hashed_password=pwd_context.hash("admin123"),
            first_name="Administrateur",
            last_name="Système",
            role=UserRole.ADMIN,
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        print("✅ Utilisateur administrateur créé!")
        print("   Email: admin@anpr.bj")
        print("   Mot de passe: admin123")
        print("   ⚠️  Changez ce mot de passe en production!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'admin: {e}")
        db.rollback()
    finally:
        db.close()

def create_sample_cameras():
    """Créé quelques caméras d'exemple"""
    print("📹 Création des caméras d'exemple...")
    
    sample_cameras = [
        {
            "name": "Caméra Porte d'Entrée",
            "location_name": "Porte principale",
            "latitude": 6.5244,
            "longitude": 2.6042,
            "address": "Cotonou, Bénin",
            "camera_type": "fixed",
            "status": "online",
            "stream_url": "rtsp://camera1.local:554/stream1"
        },
        {
            "name": "Caméra Parking",
            "location_name": "Zone de parking",
            "latitude": 6.5245,
            "longitude": 2.6043,
            "address": "Cotonou, Bénin",
            "camera_type": "fixed",
            "status": "online",
            "stream_url": "rtsp://camera2.local:554/stream1"
        },
        {
            "name": "Caméra Mobile 1",
            "location_name": "Patrouille mobile",
            "latitude": 6.5246,
            "longitude": 2.6044,
            "address": "Cotonou, Bénin",
            "camera_type": "mobile",
            "status": "online",
            "stream_url": "rtsp://mobile1.local:554/stream1"
        }
    ]
    
    db = SessionLocal()
    try:
        for camera_data in sample_cameras:
            # Vérifier si la caméra existe déjà
            existing = db.query(Camera).filter(Camera.name == camera_data["name"]).first()
            if existing:
                continue
                
            camera = Camera(**camera_data)
            db.add(camera)
        
        db.commit()
        print(f"✅ {len(sample_cameras)} caméras d'exemple créées!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des caméras: {e}")
        db.rollback()
    finally:
        db.close()

def create_sample_vehicles():
    """Créé quelques véhicules d'exemple"""
    print("🚗 Création des véhicules d'exemple...")
    
    sample_vehicles = [
        {
            "plate_number": "AB-123-CD",
            "brand": "Toyota",
            "model": "Corolla",
            "color": "Blanc",
            "vehicle_type": "car",
            "year": 2020
        },
        {
            "plate_number": "XY-789-ZW",
            "brand": "Honda",
            "model": "Civic",
            "color": "Noir",
            "vehicle_type": "car",
            "year": 2019
        },
        {
            "plate_number": "ST-456-UV",
            "brand": "Yamaha",
            "model": "YBR 125",
            "color": "Rouge",
            "vehicle_type": "motorcycle",
            "year": 2021
        }
    ]
    
    db = SessionLocal()
    try:
        for vehicle_data in sample_vehicles:
            # Vérifier si le véhicule existe déjà
            existing = db.query(Vehicle).filter(Vehicle.plate_number == vehicle_data["plate_number"]).first()
            if existing:
                continue
                
            vehicle = Vehicle(**vehicle_data)
            db.add(vehicle)
        
        db.commit()
        print(f"✅ {len(sample_vehicles)} véhicules d'exemple créés!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des véhicules: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Fonction principale d'initialisation"""
    print("🚀 Initialisation de la base de données ANPR")
    print("=" * 50)
    
    try:
        # Créer les tables
        create_tables()
        
        # Créer les données initiales
        create_admin_user()
        create_sample_cameras()
        create_sample_vehicles()
        
        print("\n🎉 Initialisation terminée avec succès!")
        print("\n📋 Prochaines étapes:")
        print("1. Configurez votre fichier .env avec les bonnes valeurs")
        print("2. Lancez l'API: python api.py")
        print("3. Accédez à l'interface: http://localhost:3000")
        print("4. Connectez-vous avec admin@anpr.bj / admin123")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de l'initialisation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 