<div align="center">

# WatWatch - AI-Powered Recommendations using Senscritique

![Build](https://img.shields.io/badge/build-passing-brightgreen?style=for-the-badge) 
![Status](https://img.shields.io/badge/status-operational-brightgreen?style=for-the-badge)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

*AI-powered recommendation engine for SensCritique - Get personalized suggestions based on your tastes*

<img src="https://i.ibb.co/Bknb727/watwatch.png" alt="WatWatch screenshot" width="800"/>

</div>

---

## 📋 About

WatWatch est un moteur de recommandation ultra-puissant qui analyse votre collection SensCritique et génère des suggestions personnalisées en utilisant les modèles OpenAI les plus avancés. Le système récupère l'intégralité de votre collection de manière asynchrone et fournit des recommandations précises et pertinentes.

### ✨ Features

- 🔄 **Récupération Asynchrone Complète** - Récupère l'intégralité de votre collection SensCritique via pagination concurrente
- 🤖 **IA de Pointe** - Utilise OpenAI (GPT-4.1, GPT-5.1) pour des suggestions ultra-pertinentes
- 🎯 **Système Anti-Doublons Avancé** - Filtrage intelligent multi-niveaux garantissant des suggestions 100% inédites :
  - Normalisation stricte des titres (accents, ponctuation, casse)
  - Suppression automatique des années et versions entre parenthèses
  - Détection des suites, prequels et remakes
  - Détection de similarité par préfixe (80%+ de correspondance)
  - Vérification d'inclusion de sous-chaînes
  - **Retry automatique** : jusqu'à 10 tentatives pour atteindre exactement N suggestions valides
- 📊 **Double Visualisation Interactive** - Deux graphiques Bokeh :
  - Graphique 1 : Classement par score IA
  - Graphique 2 : Classement par moyenne (Score IA + Note SC)
- 💾 **Export Excel** - Sauvegarde des recommandations avec métadonnées complètes
- 🎯 **Filtrage par Catégorie** - Sélection précise (Films, Séries, Jeux, BD, Livres, etc.)
- 🌐 **Notes Globales** - Récupération automatique des notes SensCritique pour chaque suggestion
- 🎨 **Interface Moderne** - GUI sombre et élégante avec PySide6
- 📈 **Suivi en Temps Réel** - Barre de progression et logs détaillés
- 🔒 **Configuration Sécurisée** - Gestion des clés API via variables d'environnement

## ⚙️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- OpenAI API key

### Setup

#### Step 1: Clone the Repository

```bash
git clone https://github.com/Brobicho/WatWatch.git
cd WatWatch
```

#### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 3: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

Add your OpenAI API key to the `.env` file:

```env
OPENAI_API_KEY=sk-proj-your-api-key-here
```

## 🚀 Usage

### Basic Usage

```bash
python run.py
```

### Running in Background

```bash
# Using nohup
nohup python run.py > default.log 2>&1 &

# Using screen
screen -S WatWatch
python run.py
# Press Ctrl+A, then D to detach

## 🚀 Usage
1. **Entrez votre nom d'utilisateur SensCritique** dans le champ prévu
2. **Choisissez le nombre de suggestions** souhaité (1-50)
3. **Sélectionnez le modèle OpenAI** (gpt-4.1-mini recommandé pour la rapidité)
4. **Sélectionnez les catégories** à considérer (Films, Séries, Jeux, etc.)
5. **(Optionnel)** Choisissez l'emplacement du fichier Excel de sortie
6. **Cliquez sur "Rechercher"** pour lancer le processus

L'application va :
- Récupérer votre collection SensCritique complète de manière asynchrone
- Générer des recommandations IA ultra-personnalisées
- **Éliminer tous les doublons** avec un système de filtrage multi-niveaux
- **Relancer automatiquement** l'IA si des doublons sont détectés (jusqu'à 10 fois)
- Récupérer les notes globales pour chaque suggestion
- Afficher les résultats dans deux graphiques Bokeh interactifs
- Sauvegarder les résultats en Excel (si configuré)

## 🔥 Le Système Anti-Doublons

### Pourquoi c'est révolutionnaire ?

Le système garantit **zéro doublon** grâce à :

1. **Normalisation Aggressive**
   ```
   "Heat (1995)" → "heat"
   "Old Boy (Version Coréenne)" → "oldboy"
   "Inside Man 2" → "insideman2"
   ```

2. **Détection d'Inclusion**
   - Si "insideman" ⊂ "insideman2" → Rejeté
   - Si "matrix" ⊂ "thematrix" → Rejeté
## 📊 Understanding the Output

### Status Messages

Pendant l'exécution, vous verrez des mises à jour en temps réel :

```
Récupération de la collection SensCritique...
✓ 1247 œuvres récupérées

Recherche de suggestions...
Tentative 1: 4 doublons filtrés, 6 ajoutés (6/10)
Tentative 2: 2 doublons filtrés, 3 ajoutés (9/10)
Tentative 3: 0 doublon filtré, 1 ajouté (10/10)
✓ 10 suggestions trouvées (100% uniques)

Récupération des notes SensCritique...
✓ Notes récupérées

Sauvegarde du fichier Excel...
✓ Fichier sauvegardé : /path/to/file.xlsx

✅ Terminé ! Affichage des résultats...
```

### Visualisation Interactive

Deux graphiques Bokeh sont affichés :

**Graphique 1 - Classement par Score IA**
- **X-axis**: Titres suggérés (triés par score IA décroissant)
- **Y-axis**: Score de confiance IA (0-100)
- **Tooltips**: Titre, Score IA, Note SC Globale

**Graphique 2 - Classement par Moyenne**
- **X-axis**: Titres suggérés (triés par moyenne décroissante)
- **Y-axis**: Moyenne = (Score IA + Note SC × 10) / 2
- **Tooltips**: Titre, Score IA, Note SC Globale, Moyenne
5. **(Optional)** Choose an output Excel file location
6. **Click "Rechercher"** to start the recommendation process

The application will:
- Fetch your complete SensCritique collection asynchronously
- Generate AI-powered recommendations
- Retrieve global ratings for each suggestion
- Display results in an interactive Bokeh chart
- Save results to Excel (if configured)

## ⚙️ Configuration

### Environment Variables (.env)

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-proj-...` | ✅ |


## 📊 Understanding the Output

### Status Messages

During execution, you'll see progress updates like:

```
Récupération de la collection SensCritique...
✓ 1247 œuvres récupérées

Recherche de suggestions...
✓ 10 suggestions trouvées

Récupération des notes SensCritique...
✓ Notes récupérées

Sauvegarde du fichier Excel...
✓ Fichier sauvegardé : /path/to/file.xlsx

✅ Terminé ! Affichage des résultats...
```

### Visualization

The interactive chart displays:
- **X-axis**: Suggested titles
- **Y-axis**: AI confidence scores (0-100)
- **Tooltips**: Title, AI score, and global SensCritique rating

### Excel Export

The exported file contains:
- **Titre**: Work title
- **Catégorie**: Media category
- **Score IA**: AI recommendation score
- **Note SC Globale**: Global SensCritique rating
- **Raison**: Why it was recommended

### Status Indicators

- ✓ Task completed successfully
- ❌ Error occurred
- ⏳ Processing in progress