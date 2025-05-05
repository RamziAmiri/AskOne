"""
Interface utilisateur Streamlit pour la génération de requêtes SQL.
"""

import streamlit as st
from src.config import STREAMLIT_TITLE, STREAMLIT_DESCRIPTION
from src.nlp.query_analyzer import QueryAnalyzer
from src.search.vector_search import VectorSearch
from src.generation.sql_generator import SQLGenerator

def main():
    st.set_page_config(
        page_title=STREAMLIT_TITLE,
        page_icon="🔍",
        layout="wide"
    )
    
    st.title(STREAMLIT_TITLE)
    st.write(STREAMLIT_DESCRIPTION)
    
    # Initialisation des composants
    query_analyzer = QueryAnalyzer()
    vector_search = VectorSearch()
    sql_generator = SQLGenerator()
    
    # Interface utilisateur
    user_query = st.text_area(
        "Entrez votre requête en langage naturel:",
        placeholder="Ex: Afficher les clients qui ont commandé plus de 1000€ ce mois-ci"
    )
    
    if st.button("Générer la requête SQL"):
        if user_query:
            # TODO: Implémenter le flux de traitement
            st.write("Requête SQL générée:")
            st.code("SELECT * FROM table", language="sql")
        else:
            st.warning("Veuillez entrer une requête")

if __name__ == "__main__":
    main() 