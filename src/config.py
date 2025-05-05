"""
Configuration centrale de l'application.
Contient tous les paramètres et chemins nécessaires au fonctionnement de l'application.
"""

import os
from pathlib import Path

# Chemins des dossiers
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
JSON_DIR = DATA_DIR / "json"
INDEX_DIR = DATA_DIR / "index"
TMP_DIR = DATA_DIR / "tmp"

# Configuration FAISS
FAISS_INDEX_NAME = "sap_metadata"
FAISS_INDEX_PATH = INDEX_DIR / f"{FAISS_INDEX_NAME}.index"

# Configuration LLM
LLM_MODEL_PATH = "path/to/local/llm/model"
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 1000

# Configuration Streamlit
STREAMLIT_TITLE = "SAP Business One SQL Generator"
STREAMLIT_DESCRIPTION = "Générez des requêtes SQL pour SAP Business One à partir du langage naturel" 