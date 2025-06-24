#!/bin/bash

# Script de configuration PostgreSQL pour ANPR Bénin
# Ce script configure la base de données PostgreSQL pour le projet ANPR

set -e

# Utilisateur administrateur PostgreSQL (adapté pour macOS)
PG_ADMIN_USER="$(whoami)"

echo "🚀 Configuration PostgreSQL pour ANPR Bénin"
echo "=============================================="

# Variables de configuration
DB_NAME="anpr_db"
DB_USER="anpr_user"
DB_PASSWORD="anpr_password"
DB_HOST="localhost"
DB_PORT="5432"

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Vérifier si PostgreSQL est installé
check_postgres() {
    if ! command -v psql &> /dev/null; then
        print_error "PostgreSQL n'est pas installé!"
        echo "Installez PostgreSQL avec:"
        echo "  Ubuntu/Debian: sudo apt-get install postgresql postgresql-contrib"
        echo "  macOS: brew install postgresql"
        echo "  CentOS/RHEL: sudo yum install postgresql postgresql-server"
        exit 1
    fi
    print_status "PostgreSQL est installé"
}

# Vérifier si le service PostgreSQL est en cours d'exécution
check_postgres_service() {
    if ! pg_isready -h $DB_HOST -p $DB_PORT &> /dev/null; then
        print_error "Le service PostgreSQL n'est pas en cours d'exécution!"
        echo "Démarrez PostgreSQL avec:"
        echo "  Ubuntu/Debian: sudo systemctl start postgresql"
        echo "  macOS: brew services start postgresql"
        echo "  CentOS/RHEL: sudo systemctl start postgresql"
        exit 1
    fi
    print_status "Service PostgreSQL en cours d'exécution"
}

# Créer l'utilisateur de base de données
create_db_user() {
    echo "Création de l'utilisateur de base de données..."
    
    # Vérifier si l'utilisateur existe déjà
    if psql -h $DB_HOST -p $DB_PORT -U "$PG_ADMIN_USER" -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1; then
        print_warning "L'utilisateur $DB_USER existe déjà"
    else
        psql -h $DB_HOST -p $DB_PORT -U "$PG_ADMIN_USER" -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
        print_status "Utilisateur $DB_USER créé"
    fi
}

# Créer la base de données
create_database() {
    echo "Création de la base de données..."
    
    # Vérifier si la base de données existe déjà
    if psql -h $DB_HOST -p $DB_PORT -U "$PG_ADMIN_USER" -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
        print_warning "La base de données $DB_NAME existe déjà"
    else
        psql -h $DB_HOST -p $DB_PORT -U "$PG_ADMIN_USER" -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
        print_status "Base de données $DB_NAME créée"
    fi
}

# Accorder les privilèges
grant_privileges() {
    echo "Configuration des privilèges..."
    
    psql -h $DB_HOST -p $DB_PORT -U "$PG_ADMIN_USER" -d $DB_NAME -c "
        GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
        GRANT ALL ON SCHEMA public TO $DB_USER;
        GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_USER;
        GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $DB_USER;
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $DB_USER;
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $DB_USER;
    "
    print_status "Privilèges configurés"
}

# Tester la connexion
test_connection() {
    echo "Test de connexion à la base de données..."
    
    if psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT version();" &> /dev/null; then
        print_status "Connexion à la base de données réussie"
    else
        print_error "Échec de la connexion à la base de données"
        exit 1
    fi
}

# Créer le fichier .env
create_env_file() {
    echo "Création du fichier .env..."
    
    if [ -f ".env" ]; then
        print_warning "Le fichier .env existe déjà"
    else
        cp env.example .env
        print_status "Fichier .env créé à partir de env.example"
        print_warning "Modifiez le fichier .env avec vos paramètres de production"
    fi
}

# Fonction principale
main() {
    echo "Vérification des prérequis..."
    check_postgres
    check_postgres_service
    
    echo ""
    echo "Configuration de la base de données..."
    create_db_user
    create_database
    grant_privileges
    
    echo ""
    echo "Tests de configuration..."
    test_connection
    
    echo ""
    echo "Configuration des fichiers..."
    create_env_file
    
    echo ""
    print_status "Configuration PostgreSQL terminée avec succès!"
    echo ""
    echo "📋 Prochaines étapes:"
    echo "1. Modifiez le fichier .env si nécessaire"
    echo "2. Installez les dépendances Python: pip install -r requirements.txt"
    echo "3. Initialisez la base de données: python init_db.py"
    echo "4. Lancez l'API: python api.py"
    echo ""
    echo "🔗 URL de connexion: postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME"
}

# Exécuter la fonction principale
main "$@" 