"""
Module de recherche sémantique dans les métadonnées SAP.
"""

from pathlib import Path
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetadataSearcher:
    """Classe pour la recherche sémantique dans les métadonnées SAP."""
    
    def __init__(self, index_path: Path, mapping_path: Path):
        """Initialise le chercheur avec l'index FAISS et le mapping des métadonnées.
        
        Args:
            index_path: Chemin vers le fichier d'index FAISS
            mapping_path: Chemin vers le fichier de mapping des métadonnées
        """
        logger.info(f"Initialisation du chercheur avec index={index_path}, mapping={mapping_path}")
        
        # Chargement du modèle
        logger.info("Chargement du modèle SentenceTransformer...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Chargement de l'index FAISS
        logger.info(f"Chargement de l'index FAISS depuis {index_path}...")
        self.index = faiss.read_index(str(index_path))
        
        # Chargement du mapping
        logger.info(f"Chargement du mapping depuis {mapping_path}...")
        with open(mapping_path, 'r', encoding='utf-8') as f:
            self.metadata_mapping = json.load(f)
            
        logger.info(f"Index chargé avec {self.index.ntotal} vecteurs")
        logger.info(f"Mapping chargé avec {len(self.metadata_mapping)} entrées")
    
    def search(self, query: str, k: int = 5) -> list:
        """Recherche les métadonnées les plus pertinentes pour une requête.
        
        Args:
            query: Requête de recherche en langage naturel
            k: Nombre de résultats à retourner
            
        Returns:
            Liste des résultats avec leurs scores et métadonnées
        """
        logger.info(f"Recherche de '{query}' avec k={k}")
        
        # Génération de l'embedding pour la requête
        query_embedding = self.model.encode([query], convert_to_tensor=True)
        query_embedding = query_embedding.cpu().numpy().astype('float32')
        
        # Recherche dans l'index FAISS
        distances, indices = self.index.search(query_embedding, k)
        
        # Récupération des résultats
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            # Convertir l'index en chaîne de caractères pour le mapping
            idx_str = str(idx)
            if idx_str in self.metadata_mapping:
                metadata = self.metadata_mapping[idx_str]
                results.append({
                    'score': float(1 - distance),  # Conversion de la distance en score de similarité
                    'table_name': metadata.get('table_name', ''),
                    'column_name': metadata.get('column_name', ''),
                    'description': metadata.get('description', ''),
                    'sql_type': metadata.get('sql_type', ''),
                    'category': metadata.get('category', ''),
                    'relations': metadata.get('relations', []),
                    'possible_values': metadata.get('possible_values', []),
                    'default_value': metadata.get('default_value', ''),
                    'is_primary_key': metadata.get('is_primary_key', False)
                })
                logger.info(f"Résultat {i+1}: {metadata.get('table_name')}.{metadata.get('column_name')} (score: {1 - distance:.2f})")
            else:
                logger.warning(f"Index {idx_str} non trouvé dans le mapping")
        
        return results
    
    def format_result(self, result: Dict) -> str:
        """
        Formate un résultat de recherche pour l'affichage.
        
        Args:
            result: Résultat de recherche à formater
            
        Returns:
            Chaîne formatée pour l'affichage
        """
        return (
            f"Table: {result['table_name']}\n"
            f"Colonne: {result['column_name']}\n"
            f"Description: {result['description']}\n"
            f"Type SQL: {result['sql_type']}\n"
            f"Catégorie: {result['category']}\n"
            f"Score de similarité: {result['score']:.2f}\n"
            f"Clé primaire: {'Oui' if result['is_primary_key'] else 'Non'}\n"
            f"Relations: {', '.join(result['relations']) if result['relations'] else 'Aucune'}\n"
            f"Valeurs possibles: {', '.join(result['possible_values']) if result['possible_values'] else 'Aucune'}\n"
            f"Valeur par défaut: {result['default_value'] or 'Aucune'}\n"
        ) 