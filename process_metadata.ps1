# Script PowerShell pour traiter les métadonnées et générer l'index FAISS

# Activer l'environnement virtuel
.\.venv\Scripts\Activate.ps1

# Exécuter le script de traitement des métadonnées
python src/ingestion/process_metadata.py

# Désactiver l'environnement virtuel
deactivate 