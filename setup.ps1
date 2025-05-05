# Couleurs pour les messages
$Green = [System.ConsoleColor]::Green
$Red = [System.ConsoleColor]::Red
$Default = [System.ConsoleColor]::Gray

# Fonction pour afficher les messages d'erreur
function Write-Error {
    param($Message)
    Write-Host $Message -ForegroundColor $Red
}

# Fonction pour vérifier si une commande existe
function Test-Command {
    param($Command)
    try {
        $null = Get-Command $Command -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

# Vérification des prérequis
Write-Host "Vérification des prérequis..." -ForegroundColor $Default

# Vérifier si Python est installé
if (-not (Test-Command "python")) {
    Write-Error "Python n'est pas installé. Veuillez installer Python 3.9 ou supérieur."
    exit 1
}

# Vérifier si pip est à jour
Write-Host "Mise à jour de pip..." -ForegroundColor $Default
python -m pip install --upgrade pip

# Création de l'environnement virtuel
Write-Host "Création de l'environnement virtuel Python..." -ForegroundColor $Default
python -m venv .venv

# Activation de l'environnement
Write-Host "Activation de l'environnement virtuel..." -ForegroundColor $Default
.\.venv\Scripts\Activate.ps1

# Installation des dépendances
Write-Host "Installation des dépendances..." -ForegroundColor $Default

# Installation des dépendances système pour blis
Write-Host "Installation des dépendances système pour blis..." -ForegroundColor $Default
try {
    # Installation des dépendances une par une pour mieux gérer les erreurs
    pip install numpy
    pip install tqdm
    pip install streamlit
    pip install faiss-cpu
    pip install sentence-transformers
    pip install pytest
    
    # Installation de spacy avec gestion des erreurs
    try {
        pip install spacy
    } catch {
        Write-Host "Tentative d'installation de spacy avec des options alternatives..." -ForegroundColor $Default
        pip install spacy --no-binary spacy
    }
    
    # Installation de ollama si nécessaire
    try {
        pip install ollama
    } catch {
        Write-Host "Ollama n'est pas disponible ou n'est pas nécessaire pour votre système." -ForegroundColor $Default
    }
    
    Write-Host "Installation terminée avec succès !" -ForegroundColor $Green
    Write-Host "Pour activer l'environnement virtuel, utilisez : .\.venv\Scripts\Activate.ps1" -ForegroundColor $Default
} catch {
    Write-Error "Une erreur est survenue lors de l'installation des dépendances :"
    Write-Error $_.Exception.Message
    exit 1
} 