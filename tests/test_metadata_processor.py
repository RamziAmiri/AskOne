"""Tests pour le module de traitement des métadonnées."""

import pytest
from pathlib import Path
import json
import numpy as np
import faiss
from src.ingestion.metadata_processor import MetadataProcessor, ColumnMetadata

@pytest.fixture
def json_dir(tmp_path):
    """Crée un dossier temporaire pour les fichiers JSON."""
    json_dir = tmp_path / "json"
    json_dir.mkdir(exist_ok=True)
    return json_dir

@pytest.fixture
def processor(json_dir):
    """Crée un processeur de métadonnées avec un dossier temporaire."""
    return MetadataProcessor(json_dir)

@pytest.fixture
def sample_json_file(json_dir):
    """Crée un fichier JSON de test."""
    data = {
        "TableName": "TEST",
        "Category": "Test",
        "Description": "Test Table",
        "PrimaryKeys": ["TestCol"],
        "Fields": [
            {
                "Field": "TestCol",
                "Description": "Test Description",
                "Related": "",
                "DefaultValue": "",
                "ValidValues": "",
                "SqlType": "NVARCHAR",
                "SqlSize": 10,
                "IsNullable": False,
                "IsPrimaryKey": True,
                "IsIdentity": False
            }
        ]
    }
    
    file_path = json_dir / "TEST.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    
    return file_path

def test_init(processor):
    """Test l'initialisation du processeur."""
    assert processor.json_dir.exists()
    assert processor.model is not None
    assert processor.vector_index is None
    assert processor.metadata_mapping == {}

def test_load_json_files(processor, sample_json_file):
    """Test le chargement des fichiers JSON."""
    files = processor.load_json_files()
    assert len(files) == 1
    assert files[0]["TableName"] == "TEST"

def test_extract_column_metadata(processor):
    """Test l'extraction des métadonnées des colonnes."""
    table_data = {
        "TableName": "TEST",
        "Category": "Test",
        "Description": "Test Table",
        "PrimaryKeys": ["TestCol"],
        "Fields": [
            {
                "Field": "TestCol",
                "Description": "Test Description",
                "Related": "",
                "DefaultValue": "",
                "ValidValues": "",
                "SqlType": "NVARCHAR",
                "SqlSize": 10,
                "IsNullable": False,
                "IsPrimaryKey": True,
                "IsIdentity": False
            }
        ]
    }

    columns = processor.extract_column_metadata(table_data)
    assert len(columns) == 1
    assert columns[0].table_name == "TEST"
    assert columns[0].column_name == "TestCol"
    assert columns[0].description == "Test Description"
    assert columns[0].sql_type == "NVARCHAR"
    assert columns[0].is_primary_key is True

def test_create_text_representation(processor):
    """Test la création de la représentation textuelle."""
    column = ColumnMetadata(
        table_name="TEST",
        column_name="TestCol",
        description="Test Description",
        sql_type="NVARCHAR",
        relations=[],
        possible_values=[],
        default_value="",
        category="Test",
        is_primary_key=True
    )
    
    text = processor.create_text_representation(column)
    assert text == "TestCol: Test Description (table TEST)"

def test_create_embeddings(processor):
    """Test la création des embeddings."""
    texts = ["Test text 1", "Test text 2"]
    embeddings = processor.create_embeddings(texts)
    assert isinstance(embeddings, np.ndarray)
    assert embeddings.shape[0] == 2

def test_process_metadata(processor, sample_json_file):
    """Test le traitement complet des métadonnées."""
    index, mapping = processor.process_metadata()
    assert isinstance(index, faiss.IndexFlatL2)
    assert isinstance(mapping, dict)
    assert len(mapping) > 0

def test_save_index(processor, json_dir, tmp_path):
    """Test la sauvegarde de l'index et du mapping."""
    # Création d'un fichier JSON de test
    data = {
        "TableName": "TEST",
        "Category": "Test",
        "Description": "Test Table",
        "PrimaryKeys": ["TestCol"],
        "Fields": [
            {
                "Field": "TestCol",
                "Description": "Test Description",
                "Related": "",
                "DefaultValue": "",
                "ValidValues": "",
                "SqlType": "NVARCHAR",
                "SqlSize": 10,
                "IsNullable": False,
                "IsPrimaryKey": True,
                "IsIdentity": False
            }
        ]
    }
    
    file_path = json_dir / "TEST.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    
    # Traitement des métadonnées
    processor.process_metadata()
    
    # Sauvegarde de l'index et du mapping
    index_path = tmp_path / "index.faiss"
    mapping_path = tmp_path / "mapping.json"
    processor.save_index(index_path, mapping_path)
    
    # Vérification des fichiers sauvegardés
    assert index_path.exists()
    assert mapping_path.exists()
    
    # Vérification du contenu du mapping
    with open(mapping_path, 'r', encoding='utf-8') as f:
        saved_mapping = json.load(f)
    assert len(saved_mapping) > 0 