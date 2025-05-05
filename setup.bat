@echo off
echo Création de l'environnement virtuel Python...
python -m venv .venv

echo Activation de l'environnement virtuel...
call .\.venv\Scripts\activate.bat

echo Installation des dépendances...
pip install -r requirements.txt

echo Installation terminée avec succès !
echo Pour activer l'environnement virtuel, utilisez : .\.venv\Scripts\activate.bat 