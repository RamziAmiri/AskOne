#!/bin/bash

# Couleurs pour les messages
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "Création de l'environnement virtuel Python..."
python3 -m venv .venv

echo "Activation de l'environnement virtuel..."
source .venv/bin/activate

echo "Installation des dépendances..."
pip install -r requirements.txt

echo -e "${GREEN}Installation terminée avec succès !${NC}"
echo "Pour activer l'environnement virtuel, utilisez : source .venv/bin/activate" 