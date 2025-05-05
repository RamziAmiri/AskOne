"""
Application Streamlit pour la recherche sémantique dans les métadonnées SAP.
"""

import streamlit as st
from pathlib import Path
import os
import sys

# Ajouter le répertoire racine au PYTHONPATH
root_path = str(Path(__file__).parent.parent.parent)
if root_path not in sys.path:
    sys.path.append(root_path)

from src.streamlit.pages.search_metadata import main as search_main

# Configuration de la page
st.set_page_config(
    page_title="AskOne - Recherche SAP",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre de l'application
st.title("🔍 AskOne - Recherche SAP")

# Menu de navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choisissez une page :",
    ["Accueil", "Recherche de Métadonnées"]
)

# Pages
if page == "Accueil":
    st.markdown("""
    ## Bienvenue dans AskOne
    
    Cette application vous permet de rechercher des informations dans les métadonnées SAP
    de manière sémantique, en utilisant le langage naturel.
    
    ### Fonctionnalités :
    
    - **Recherche de Métadonnées** : Trouvez les colonnes et tables SAP en utilisant
      des termes en langage naturel (ex: "client", "date", "montant")
    
    ### Comment utiliser l'application ?
    
    1. Sélectionnez "Recherche de Métadonnées" dans le menu de gauche
    2. Entrez votre recherche dans le champ prévu
    3. Explorez les résultats et leurs détails
    
    ### À propos
    
    Cette application utilise :
    - Streamlit pour l'interface utilisateur
    - SentenceTransformers pour la recherche sémantique
    - FAISS pour l'indexation des vecteurs
    """)

elif page == "Recherche de Métadonnées":
    search_main() 