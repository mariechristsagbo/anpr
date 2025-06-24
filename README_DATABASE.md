# 🗄️ Base de Données ANPR Bénin

Ce document explique la configuration et l'utilisation de la base de données PostgreSQL pour le système ANPR (Automatic Number Plate Recognition) du Bénin.

## 📋 Table des Matières

- [Architecture de la Base de Données](#architecture-de-la-base-de-données)
- [Installation et Configuration](#installation-et-configuration)
- [Modèles de Données](#modèles-de-données)
- [Migrations](#migrations)
- [Utilisation](#utilisation)
- [Sauvegarde et Restauration](#sauvegarde-et-restauration)

## 🏗️ Architecture de la Base de Données

### Technologies Utilisées

- **PostgreSQL 12+** : Base de données principale
- **SQLAlchemy 2.0+** : ORM Python
- **Alembic** : Gestion des migrations
- **psycopg2** : Driver PostgreSQL pour Python

### Avantages de PostgreSQL pour ANPR

✅ **Performance** : Excellent pour les requêtes complexes sur l'historique
✅ **Géospatial** : Support PostGIS pour la géolocalisation
✅ **JSON** : Stockage flexible des métadonnées
✅ **Concurrence** : Gestion robuste des accès simultanés
✅ **Fiabilité** : ACID compliance pour la sécurité des données

## 🚀 Installation et Configuration

### 1. Prérequis

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql

# CentOS/RHEL
sudo yum install postgresql postgresql-server
```

### 2. Configuration Automatique

```bash
# Rendre le script exécutable
chmod +x setup_postgres.sh

# Exécuter la configuration
./setup_postgres.sh
```

### 3. Configuration Manuelle

Si vous préférez configurer manuellement :

```sql
-- Se connecter à PostgreSQL
sudo -u postgres psql

-- Créer l'utilisateur
CREATE USER anpr_user WITH PASSWORD 'anpr_password';

-- Créer la base de données
CREATE DATABASE anpr_db OWNER anpr_user;

-- Accorder les privilèges
GRANT ALL PRIVILEGES ON DATABASE anpr_db TO anpr_user;
\q
```

### 4. Configuration de l'Environnement

```bash
# Copier le fichier d'exemple
cp env.example .env

# Modifier les paramètres dans .env
nano .env
```

Variables importantes dans `.env` :
```env
DATABASE_URL=postgresql://anpr_user:anpr_password@localhost:5432/anpr_db
SECRET_KEY=your-secret-key-here
DEBUG=true
```

### 5. Installation des Dépendances

```bash
pip install -r requirements.txt
```

### 6. Initialisation de la Base de Données

```bash
python init_db.py
```

## 📊 Modèles de Données

### Structure des Tables

#### 1. **users** - Utilisateurs du système
```sql
- id (PK)
- email (unique)
- hashed_password
- first_name, last_name
- role (admin, operator, viewer)
- is_active, last_login
- created_at, updated_at
```

#### 2. **vehicles** - Véhicules enregistrés
```sql
- id (PK)
- plate_number (unique)
- brand, model, color, vehicle_type
- year, country
- is_stolen, stolen_reported_at
- metadata (JSON)
- created_at, updated_at
```

#### 3. **cameras** - Caméras de surveillance
```sql
- id (PK)
- name, location_name
- latitude, longitude, address
- camera_type (fixed, mobile, ptz)
- status (online, offline, error)
- stream_url, rtsp_url
- settings (JSON)
- created_at, updated_at
```

#### 4. **detections** - Détections de plaques
```sql
- id (PK)
- plate_number
- confidence, detection_confidence, recognition_confidence
- ocr_text, bounding_box, recognition_polygon
- image_path, image_data
- processing_time
- vehicle_type, vehicle_color, vehicle_brand, vehicle_model
- metadata (JSON)
- vehicle_id (FK), camera_id (FK), created_by_id (FK)
- detected_at, created_at, updated_at
```

#### 5. **alerts** - Alertes système
```sql
- id (PK)
- type, severity, status
- title, message, details (JSON)
- acknowledged_at, resolved_at
- detection_id (FK), vehicle_id (FK), camera_id (FK)
- created_by_id (FK), acknowledged_by_id (FK), resolved_by_id (FK)
- created_at, updated_at
```

#### 6. **stolen_vehicles** - Véhicules volés
```sql
- id (PK)
- plate_number, report_number (unique)
- stolen_date, stolen_location
- stolen_location_lat, stolen_location_lng
- description, police_station
- contact_person, contact_phone, contact_email
- is_active, recovered_date, recovered_location
- vehicle_id (FK), reported_by_id (FK), recovered_by_id (FK)
- created_at, updated_at
```

### Relations entre les Tables

```mermaid
erDiagram
    users ||--o{ detections : "created_by"
    users ||--o{ alerts : "created_by"
    users ||--o{ stolen_vehicles : "reported_by"
    
    vehicles ||--o{ detections : "vehicle"
    vehicles ||--|| stolen_vehicles : "stolen_record"
    
    cameras ||--o{ detections : "camera"
    
    detections ||--o{ alerts : "detection"
```

## 🔄 Migrations

### Initialisation d'Alembic

```bash
# Initialiser Alembic (déjà fait)
alembic init alembic
```

### Créer une Migration

```bash
# Générer une migration automatique
alembic revision --autogenerate -m "Description de la migration"

# Appliquer les migrations
alembic upgrade head
```

### Commandes Utiles

```bash
# Voir l'état des migrations
alembic current

# Voir l'historique des migrations
alembic history

# Revenir à une version précédente
alembic downgrade -1

# Appliquer jusqu'à une version spécifique
alembic upgrade 0003
```

## 💻 Utilisation

### Connexion à la Base de Données

```python
from database import get_db, SessionLocal

# Utilisation avec FastAPI
def some_endpoint(db: Session = Depends(get_db)):
    # Utiliser la session db
    pass

# Utilisation directe
db = SessionLocal()
try:
    # Opérations sur la base de données
    pass
finally:
    db.close()
```

### Exemples de Requêtes

#### Récupérer les détections récentes
```python
from models import Detection
from sqlalchemy import desc

detections = db.query(Detection)\
    .order_by(desc(Detection.detected_at))\
    .limit(10)\
    .all()
```

#### Rechercher un véhicule volé
```python
from models import Vehicle

stolen_vehicle = db.query(Vehicle)\
    .filter(Vehicle.plate_number == plate_number)\
    .filter(Vehicle.is_stolen == True)\
    .first()
```

#### Statistiques des détections
```python
from sqlalchemy import func
from datetime import datetime, timedelta

# Détections du dernier jour
yesterday = datetime.now() - timedelta(days=1)
daily_detections = db.query(func.count(Detection.id))\
    .filter(Detection.detected_at >= yesterday)\
    .scalar()
```

## 💾 Sauvegarde et Restauration

### Sauvegarde

```bash
# Sauvegarde complète
pg_dump -h localhost -U anpr_user -d anpr_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Sauvegarde compressée
pg_dump -h localhost -U anpr_user -d anpr_db | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Sauvegarde des données uniquement (sans schéma)
pg_dump -h localhost -U anpr_user -d anpr_db --data-only > data_backup.sql
```

### Restauration

```bash
# Restaurer une sauvegarde
psql -h localhost -U anpr_user -d anpr_db < backup_20241201_120000.sql

# Restaurer une sauvegarde compressée
gunzip -c backup_20241201_120000.sql.gz | psql -h localhost -U anpr_user -d anpr_db
```

### Script de Sauvegarde Automatique

```bash
#!/bin/bash
# backup_anpr.sh

BACKUP_DIR="/var/backups/anpr"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/anpr_backup_$DATE.sql.gz"

mkdir -p $BACKUP_DIR

pg_dump -h localhost -U anpr_user -d anpr_db | gzip > $BACKUP_FILE

# Garder seulement les 7 derniers jours
find $BACKUP_DIR -name "anpr_backup_*.sql.gz" -mtime +7 -delete

echo "Sauvegarde créée: $BACKUP_FILE"
```

## 🔧 Maintenance

### Optimisation des Performances

```sql
-- Créer des index pour améliorer les performances
CREATE INDEX idx_detections_plate_number ON detections(plate_number);
CREATE INDEX idx_detections_detected_at ON detections(detected_at);
CREATE INDEX idx_detections_camera_id ON detections(camera_id);
CREATE INDEX idx_vehicles_plate_number ON vehicles(plate_number);
CREATE INDEX idx_alerts_created_at ON alerts(created_at);
CREATE INDEX idx_alerts_status ON alerts(status);
```

### Nettoyage des Données

```sql
-- Supprimer les détections anciennes (plus de 1 an)
DELETE FROM detections 
WHERE detected_at < NOW() - INTERVAL '1 year';

-- Archiver les alertes résolues (plus de 6 mois)
DELETE FROM alerts 
WHERE status = 'resolved' 
AND resolved_at < NOW() - INTERVAL '6 months';
```

### Monitoring

```sql
-- Vérifier la taille des tables
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    correlation
FROM pg_stats 
WHERE tablename IN ('detections', 'vehicles', 'alerts');

-- Vérifier les connexions actives
SELECT 
    datname,
    usename,
    application_name,
    client_addr,
    state,
    query_start
FROM pg_stat_activity 
WHERE datname = 'anpr_db';
```

## 🚨 Dépannage

### Problèmes Courants

#### 1. Erreur de Connexion
```bash
# Vérifier que PostgreSQL est en cours d'exécution
sudo systemctl status postgresql

# Vérifier la configuration
sudo -u postgres psql -c "SHOW listen_addresses;"
```

#### 2. Erreur de Permissions
```sql
-- Vérifier les permissions de l'utilisateur
SELECT rolname, rolsuper, rolinherit, rolcreaterole, rolcreatedb 
FROM pg_roles 
WHERE rolname = 'anpr_user';
```

#### 3. Erreur de Migration
```bash
# Vérifier l'état des migrations
alembic current

# Forcer une migration
alembic stamp head
```

## 📞 Support

Pour toute question ou problème :

1. Vérifiez les logs PostgreSQL : `/var/log/postgresql/`
2. Consultez la documentation officielle PostgreSQL
3. Ouvrez une issue sur le repository du projet

---

**Note** : Cette configuration est optimisée pour un environnement de développement. Pour la production, assurez-vous de :
- Changer les mots de passe par défaut
- Configurer SSL/TLS
- Mettre en place des sauvegardes automatiques
- Configurer la surveillance et les alertes
- Optimiser les paramètres PostgreSQL selon votre charge 