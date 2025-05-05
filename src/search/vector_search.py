"""
Module de recherche vectorielle dans l'index FAISS.
"""

import faiss
import numpy as np
from typing import List, Tuple

from src.config import FAISS_INDEX_PATH

class VectorSearch:
    """Classe responsable de la recherche vectorielle dans l'index FAISS."""
    
    def __init__(self):
        self.index = None
        self.load_index()
    
    def load_index(self):
        """Charge l'index FAISS depuis le disque."""
        if FAISS_INDEX_PATH.exists():
            self.index = faiss.read_index(str(FAISS_INDEX_PATH))
    
    def search(self, query_vector: np.ndarray, k: int = 5) -> List[Tuple[int, float]]:
        """Effectue une recherche dans l'index FAISS."""
        if self.index is None:
            raise ValueError("Index FAISS non chargé")
        
        distances, indices = self.index.search(query_vector, k)
        return list(zip(indices[0], distances[0]))
    
    def add_to_index(self, vectors: np.ndarray):
        """Ajoute des vecteurs à l'index FAISS."""
        if self.index is None:
            raise ValueError("Index FAISS non chargé")
        
        self.index.add(vectors)
        faiss.write_index(self.index, str(FAISS_INDEX_PATH)) 