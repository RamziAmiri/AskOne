"""
Module de génération de requêtes SQL via LLM.
"""

from typing import Dict, List

from src.config import LLM_MODEL_PATH, LLM_TEMPERATURE, LLM_MAX_TOKENS

class SQLGenerator:
    """Classe responsable de la génération de requêtes SQL via LLM."""
    
    def __init__(self):
        # TODO: Initialiser le modèle LLM
        pass
    
    def generate_sql(self, 
                    query: str, 
                    context: Dict[str, List[str]], 
                    metadata: Dict) -> str:
        """
        Génère une requête SQL à partir d'une requête en langage naturel.
        
        Args:
            query: Requête en langage naturel
            context: Contexte extrait de la recherche vectorielle
            metadata: Métadonnées pertinentes
            
        Returns:
            str: Requête SQL générée
        """
        # TODO: Implémenter la génération SQL
        pass
    
    def validate_sql(self, sql: str) -> bool:
        """Valide la syntaxe SQL générée."""
        # TODO: Implémenter la validation SQL
        pass 