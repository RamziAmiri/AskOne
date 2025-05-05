"""
Script d'exécution pour le traitement des métadonnées SAP.
"""

import sys
from pathlib import Path

# Ajout du répertoire racine au PYTHONPATH
root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))

from src.config import JSON_DIR, INDEX_DIR
from src.ingestion.metadata_processor import MetadataProcessor

def main():
    """Point d'entrée principal pour le traitement des métadonnées."""
    # Création des dossiers nécessaires
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    
    # Initialisation du processeur
    processor = MetadataProcessor(JSON_DIR)
    
    # Traitement des métadonnées
    print("Traitement des métadonnées...")
    processor.process_metadata()
    
    # Sauvegarde des résultats
    print("Sauvegarde de l'index et du mapping...")
    index_path = INDEX_DIR / "sap_metadata.index"
    mapping_path = INDEX_DIR / "sap_metadata_mapping.json"
    processor.save_index(index_path, mapping_path)
    
    print(f"Index FAISS sauvegardé dans : {index_path}")
    print(f"Mapping des métadonnées sauvegardé dans : {mapping_path}")

if __name__ == "__main__":
    main() 