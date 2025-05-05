# SAP Business One SQL Generator

Application Streamlit permettant de générer des requêtes SQL pour SAP Business One à partir du langage naturel.

## Fonctionnalités

- Extraction et traitement des métadonnées SAP Business One
- Analyse des requêtes en langage naturel
- Recherche vectorielle dans les métadonnées
- Génération de requêtes SQL via LLM
- Interface utilisateur intuitive avec Streamlit

## Structure du projet

```
.
├── src/
│   ├── ingestion/         # Extraction des métadonnées
│   ├── nlp/              # Analyse des requêtes
│   ├── search/           # Recherche vectorielle
│   ├── generation/       # Génération SQL
│   ├── interface/        # Interface Streamlit
│   └── config.py         # Configuration centrale
├── tests/                # Tests unitaires
├── data/
│   ├── json/            # Métadonnées JSON
│   ├── index/           # Index FAISS
│   └── tmp/             # Fichiers temporaires
├── requirements.txt     # Dépendances
└── README.md           # Documentation
```

## Installation

1. Clonez le dépôt :
```bash
git clone [URL_DU_REPO]
cd sap-sql-generator
```

2. Créez un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

1. Lancez l'application Streamlit :
```bash
streamlit run src/interface/app.py
```

2. Ouvrez votre navigateur à l'adresse indiquée (généralement http://localhost:8501)

3. Entrez votre requête en langage naturel et cliquez sur "Générer la requête SQL"

## Tests

Pour exécuter les tests unitaires :
```bash
pytest tests/
```

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## Licence

MIT 