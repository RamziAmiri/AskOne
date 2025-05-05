"""
Page Streamlit pour tester la recherche sémantique dans les métadonnées SAP.
"""

import streamlit as st
from pathlib import Path
import sys
import os

# Ajouter le répertoire racine au PYTHONPATH
root_path = str(Path(__file__).parent.parent.parent.parent)
if root_path not in sys.path:
    sys.path.append(root_path)

from src.ingestion.metadata_searcher import MetadataSearcher

def main():
    """Fonction principale de la page de recherche."""
    # Titre de la page
    st.title("🔍 Recherche de Métadonnées SAP")

    # Initialisation du chercheur
    @st.cache_resource
    def init_searcher():
        """Initialise le chercheur de métadonnées."""
        index_path = Path("data/index/sap_metadata.index")
        mapping_path = Path("data/index/sap_metadata_mapping.json")
        
        # Vérification des fichiers
        if not index_path.exists():
            st.error(f"Le fichier d'index n'existe pas : {index_path}")
            return None
        if not mapping_path.exists():
            st.error(f"Le fichier de mapping n'existe pas : {mapping_path}")
            return None
            
        st.info(f"Chargement de l'index depuis : {index_path}")
        st.info(f"Chargement du mapping depuis : {mapping_path}")
        
        return MetadataSearcher(index_path, mapping_path)

    try:
        searcher = init_searcher()
        if searcher is None:
            st.stop()
    except Exception as e:
        st.error(f"Erreur lors de l'initialisation du chercheur : {str(e)}")
        st.stop()

    # Interface de recherche
    st.markdown("""
    ### Comment utiliser cette page ?
    1. Entrez un terme de recherche dans le champ ci-dessous (ex: "client", "date", "montant")
    2. Le système recherchera les colonnes dont la description correspond le mieux à votre recherche
    3. Les résultats sont triés par pertinence (score de similarité)
    """)

    # Champ de recherche
    query = st.text_input(
        "Entrez votre recherche :",
        placeholder="Ex: client, date, montant...",
        help="Le système recherchera les colonnes dont la description correspond le mieux à votre recherche."
    )

    # Nombre de résultats
    k = st.slider(
        "Nombre de résultats à afficher :",
        min_value=1,
        max_value=20,
        value=5,
        help="Choisissez le nombre de résultats à afficher."
    )

    # Bouton de recherche
    if st.button("Rechercher", type="primary"):
        if not query:
            st.warning("Veuillez entrer un terme de recherche.")
        else:
            with st.spinner("Recherche en cours..."):
                try:
                    # Recherche des résultats
                    st.info(f"Recherche de '{query}' avec k={k}")
                    results = searcher.search(query, k)
                    
                    if not results:
                        st.info("Aucun résultat trouvé pour votre recherche.")
                    else:
                        # Affichage des résultats
                        st.markdown(f"### Résultats pour '{query}'")
                        
                        for i, result in enumerate(results, 1):
                            with st.expander(f"Résultat {i} (Score: {result['score']:.2f})"):
                                st.markdown(f"**Table:** {result['table_name']}")
                                st.markdown(f"**Colonne:** {result['column_name']}")
                                st.markdown(f"**Description:** {result['description']}")
                                st.markdown(f"**Type SQL:** {result['sql_type']}")
                                st.markdown(f"**Catégorie:** {result['category']}")
                                
                                # Affichage des relations
                                if result['relations']:
                                    st.markdown("**Relations:**")
                                    for rel in result['relations']:
                                        st.markdown(f"- {rel}")
                                
                                # Affichage des valeurs possibles
                                if result['possible_values']:
                                    st.markdown("**Valeurs possibles:**")
                                    for val in result['possible_values']:
                                        st.markdown(f"- {val}")
                                
                                # Affichage de la valeur par défaut
                                if result['default_value']:
                                    st.markdown(f"**Valeur par défaut:** {result['default_value']}")
                                
                                # Indicateur de clé primaire
                                if result['is_primary_key']:
                                    st.markdown(":key: **Clé primaire**")
                    
                except Exception as e:
                    st.error(f"Erreur lors de la recherche : {str(e)}")

    # Section d'aide
    with st.expander("ℹ️ Aide"):
        st.markdown("""
        ### Comment fonctionne la recherche ?
        
        La recherche utilise un modèle de langage (SentenceTransformer) pour comprendre le sens de votre requête
        et trouver les colonnes dont la description correspond le mieux.
        
        #### Conseils pour une meilleure recherche :
        - Utilisez des termes simples et descriptifs
        - Essayez différents synonymes si vous ne trouvez pas ce que vous cherchez
        - Le score de similarité indique à quel point le résultat correspond à votre recherche (1.0 = parfait)
        
        #### Exemples de recherches :
        - "client" : trouvera les colonnes liées aux clients
        - "date" : trouvera les colonnes de type date
        - "montant" : trouvera les colonnes contenant des montants
        - "adresse" : trouvera les colonnes d'adresse
        """) 