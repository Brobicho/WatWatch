<div align="center">

# WatWatch - AI-Powered Recommendations using Senscritique

![Build](https://img.shields.io/badge/build-passing-brightgreen?style=for-the-badge) 
![Status](https://img.shields.io/badge/status-operational-brightgreen?style=for-the-badge)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

*AI-powered recommendation engine for SensCritique - Get personalized suggestions based on your tastes*

<img src="https://i.ibb.co/Q7LkRfzX/Capture-d-cran-du-2025-12-11-09-31-39.png" alt="WatWatch screenshot" width="800"/>

</div>

---

## 📋 About

Watwatch is an intelligent recommendation tool that analyzes your SensCritique collection and generates personalized suggestions using OpenAI's latest models. It fetches your complete collection asynchronously and provides tailored recommendations across multiple media categories.

### ✨ Features

- 🔄 **Async Collection Fetching** - Retrieves your entire SensCritique collection using concurrent pagination
- 🤖 **AI-Powered Recommendations** - Leverages OpenAI (GPT-4.1, GPT-5.1) for intelligent suggestions
- 📊 **Interactive Visualization** - Chart displaying recommendations with scores
- 💾 **Excel Export** - Save recommendations with metadata to Excel files
- 🎯 **Category Filtering** - Choose specific categories (Films, Series, Games, etc.)
- 🌐 **Global Ratings** - Automatically fetches SensCritique global ratings for suggestions
- 🎨 **Modern GUI** - Clean, dark-themed interface built with PySide6
- 📈 **Progress Tracking** - Real-time progress bar and status updates
- 🔒 **Secure Configuration** - Environment variable-based API key management

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

### Launch the Application

```bash
python3 run.py
```

### Using the GUI

1. **Enter your SensCritique username** in the username field
2. **Choose the number of suggestions** you want (1-50)
3. **Select the OpenAI model** (gpt-4.1-mini recommended for speed)
4. **Select categories** to consider (Films, Series, Games, etc.)
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