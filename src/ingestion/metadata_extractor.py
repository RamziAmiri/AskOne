"""
Module d'extraction et de traitement des métadonnées SAP Business One.
"""

import json
from pathlib import Path
from typing import Dict, List

from src.config import JSON_DIR

class MetadataExtractor:
    """Classe responsable de l'extraction et du traitement des métadonnées SAP."""
    
    def __init__(self):
        self.metadata_path = JSON_DIR / "sap_metadata.json"
    
    def load_metadata(self) -> Dict:
        """Charge les métadonnées depuis le fichier JSON."""
        with open(self.metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def process_metadata(self, metadata: Dict) -> List[Dict]:
        """Traite les métadonnées pour la vectorisation."""
        # TODO: Implémenter le traitement des métadonnées
        pass 