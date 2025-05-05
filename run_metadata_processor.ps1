# Configuration de l'environnement
$env:PYTHONPATH = $PSScriptRoot

# Activation de l'environnement virtuel
.\.venv\Scripts\Activate.ps1

# Exécution du script
python src/ingestion/process_metadata.py

# Désactivation de l'environnement virtuel
deactivate 