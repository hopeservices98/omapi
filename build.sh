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
python manage.py migrate --noinput

echo "✅ Build terminé avec succès!"