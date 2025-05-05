"""
Module de traitement et d'indexation des métadonnées SAP.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from dataclasses import dataclass
from tqdm import tqdm

@dataclass
class ColumnMetadata:
    """Classe pour stocker les métadonnées d'une colonne."""
    table_name: str
    column_name: str
    description: str
    sql_type: str
    relations: List[str]
    possible_values: List[str]
    default_value: str
    category: str
    is_primary_key: bool

class MetadataProcessor:
    """Classe responsable du traitement et de l'indexation des métadonnées."""
    
    def __init__(self, json_dir: Path, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialise le processeur de métadonnées.
        
        Args:
            json_dir: Chemin vers le dossier contenant les fichiers JSON
            model_name: Nom du modèle SentenceTransformer à utiliser
        """
        self.json_dir = Path(json_dir)
        if not self.json_dir.exists():
            raise FileNotFoundError(f"Le dossier {json_dir} n'existe pas")
        self.model = SentenceTransformer(model_name)
        self.vector_index = None
        self.metadata_mapping = {}
        
    def load_json_files(self) -> List[Dict]:
        """Charge tous les fichiers JSON du dossier."""
        metadata_files = []
        json_files = list(self.json_dir.glob("*.json"))
        
        if not json_files:
            raise FileNotFoundError(f"Aucun fichier JSON trouvé dans {self.json_dir}")
            
        print(f"Trouvé {len(json_files)} fichiers JSON")
        for json_file in json_files:
            print(f"Traitement de {json_file.name}...")
            with open(json_file, 'r', encoding='utf-8') as f:
                metadata_files.append(json.load(f))
        return metadata_files
    
    def extract_column_metadata(self, table_data: Dict) -> List[ColumnMetadata]:
        """Extrait les métadonnées des colonnes d'une table."""
        columns = []
        table_name = table_data.get("TableName", "")
        
        if not table_name:
            print(f"Avertissement: Table sans nom trouvée dans {table_data}")
            return columns
            
        for field in table_data.get("Fields", []):
            # Convertir la relation en liste si c'est une chaîne
            relations = [field.get("Related", "")] if field.get("Related") else []
            
            # Convertir les valeurs valides en liste si c'est une chaîne
            possible_values = [field.get("ValidValues", "")] if field.get("ValidValues") else []
            
            col_metadata = ColumnMetadata(
                table_name=table_name,
                column_name=field.get("Field", ""),
                description=field.get("Description", ""),
                sql_type=field.get("SqlType", ""),
                relations=relations,
                possible_values=possible_values,
                default_value=field.get("DefaultValue", ""),
                category=table_data.get("Category", ""),
                is_primary_key=field.get("IsPrimaryKey", False)
            )
            columns.append(col_metadata)
        
        return columns
    
    def create_text_representation(self, column: ColumnMetadata) -> str:
        """Crée la représentation textuelle d'une colonne."""
        return f"{column.column_name}: {column.description} (table {column.table_name})"
    
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """Convertit les textes en embeddings."""
        if not texts:
            raise ValueError("Aucun texte à encoder")
        print(f"Création des embeddings pour {len(texts)} textes...")
        return self.model.encode(texts, show_progress_bar=True)
    
    def build_faiss_index(self, embeddings: np.ndarray):
        """Construit l'index FAISS."""
        if embeddings.size == 0:
            raise ValueError("Aucun embedding à indexer")
            
        dimension = embeddings.shape[1]
        print(f"Création de l'index FAISS avec dimension {dimension}...")
        self.vector_index = faiss.IndexFlatL2(dimension)
        self.vector_index.add(embeddings)
        print(f"Index créé avec {self.vector_index.ntotal} vecteurs")
    
    def process_metadata(self) -> Tuple[faiss.Index, Dict]:
        """
        Traite tous les fichiers JSON et construit l'index FAISS.
        
        Returns:
            Tuple contenant l'index FAISS et le mapping des métadonnées
        """
        # Chargement des fichiers
        metadata_files = self.load_json_files()
        
        # Extraction des métadonnées
        all_columns = []
        for table_data in metadata_files:
            columns = self.extract_column_metadata(table_data)
            if columns:
                all_columns.extend(columns)
        
        if not all_columns:
            raise ValueError("Aucune colonne trouvée dans les fichiers JSON")
            
        print(f"Trouvé {len(all_columns)} colonnes au total")
        
        # Création des représentations textuelles
        texts = [self.create_text_representation(col) for col in all_columns]
        
        # Génération des embeddings
        embeddings = self.create_embeddings(texts)
        
        # Construction de l'index FAISS
        self.build_faiss_index(embeddings)
        
        # Création du mapping
        self.metadata_mapping = {
            i: {
                "table_name": col.table_name,
                "column_name": col.column_name,
                "description": col.description,
                "sql_type": col.sql_type,
                "relations": col.relations,
                "possible_values": col.possible_values,
                "default_value": col.default_value,
                "category": col.category,
                "is_primary_key": col.is_primary_key
            }
            for i, col in enumerate(all_columns)
        }
        
        return self.vector_index, self.metadata_mapping
    
    def save_index(self, index_path: Path, mapping_path: Path):
        """Sauvegarde l'index FAISS et le mapping sur disque."""
        if self.vector_index is None:
            raise ValueError("Aucun index à sauvegarder")
            
        # Sauvegarde de l'index FAISS
        print(f"Sauvegarde de l'index dans {index_path}...")
        faiss.write_index(self.vector_index, str(index_path))
        
        # Sauvegarde du mapping
        print(f"Sauvegarde du mapping dans {mapping_path}...")
        with open(mapping_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata_mapping, f, ensure_ascii=False, indent=2) 