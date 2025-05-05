"""
Tests unitaires pour le module QueryAnalyzer.
"""

import pytest
from src.nlp.query_analyzer import QueryAnalyzer

@pytest.fixture
def analyzer():
    return QueryAnalyzer()

def test_preprocess_query(analyzer):
    """Test du prétraitement des requêtes."""
    query = "  Afficher les clients   avec des commandes  "
    processed = analyzer.preprocess_query(query)
    assert isinstance(processed, str)
    # TODO: Ajouter des assertions spécifiques

def test_extract_entities(analyzer):
    """Test de l'extraction d'entités."""
    query = "Afficher les commandes des clients VIP du mois dernier"
    entities = analyzer.extract_entities(query)
    assert isinstance(entities, dict)
    # TODO: Ajouter des assertions spécifiques

def test_analyze_intent(analyzer):
    """Test de l'analyse d'intention."""
    query = "Combien de commandes ont été passées ce mois-ci ?"
    intent = analyzer.analyze_intent(query)
    assert isinstance(intent, str)
    # TODO: Ajouter des assertions spécifiques 