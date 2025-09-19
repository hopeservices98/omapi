#!/usr/bin/env bash
# Script de build pour Render

set -o errexit  # Exit en cas d'erreur

# Installer les dépendances
echo "📦 Installation des dépendances Python..."
pip install -r requirements.txt

# Installer gunicorn et whitenoise spécifiquement
echo "🔧 Installation de Gunicorn et WhiteNoise..."
pip install gunicorn whitenoise

# Collecter les fichiers statiques
echo "📂 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear

# Appliquer les migrations de base de données
echo "🗄️ Application des migrations..."
python manage.py showmigrations
python manage.py migrate --noinput --verbosity=2

# Vérifier que les migrations ont été appliquées
echo "🔍 Vérification des migrations..."
python manage.py showmigrations | grep "\[X\]" | wc -l

echo "✅ Build terminé avec succès!"