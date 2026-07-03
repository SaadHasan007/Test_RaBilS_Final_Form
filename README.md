<p align="center">
  <h1 align="center">🧪 Test RaBilS</h1>
  <p align="center">
    <strong>NLP-Based Automated Test Case Generator for E-Commerce User Stories</strong>
  </p>
  <p align="center">
    <em>Transforming user stories into comprehensive software test cases using Natural Language Processing and Machine Learning</em>
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Backend-green?logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/React-Frontend-61DAFB?logo=react&logoColor=black" alt="React">
  <img src="https://img.shields.io/badge/Vite-Build-646CFF?logo=vite&logoColor=white" alt="Vite">
  <img src="https://img.shields.io/badge/TailwindCSS-Styling-38B2AC?logo=tailwindcss&logoColor=white" alt="TailwindCSS">
  <img src="https://img.shields.io/badge/HuggingFace-Transformers-FFD21E?logo=huggingface&logoColor=black" alt="HuggingFace">
</p>

---

## 📖 About

**Test RaBilS** is a Final Year Project (FYP) that automates the software testing lifecycle by converting agile **user stories** into structured **test cases**. The system leverages a multi-layered NLP pipeline combining rule-based analysis, machine learning models, and large language models (LLMs) to detect ambiguity, generate acceptance criteria, prioritize test cases, and detect duplicate requirements — all through a modern web interface.

> **RaBilS** = **Ra**fi + **Bil**al + **S**aad — the team behind this project ❤️

### 🎯 Problem Statement

In software development, writing comprehensive test cases from user stories is a **time-consuming**, **error-prone**, and **subjective** process. Key challenges include:

- **Ambiguous requirements** that lead to incomplete or incorrect test cases
- **Manual effort** required by QA teams to interpret and convert user stories
- **Inconsistent prioritization** of test cases across team members
- **Duplicate requirements** that go undetected across large backlogs

### 💡 Our Solution

Test RaBilS addresses these challenges through a 5-stage automated pipeline:

```
User Story → Ambiguity Detection → Ambiguity Removal → Test Case Generation → Prioritization
```

---

## ✨ Features

### 🔍 Multi-Level Ambiguity Detection
A **hybrid fusion system** combining rule-based NLP and ML-based classification:

| Level | Type | Technique | Description |
|-------|------|-----------|-------------|
| **1** | Lexical | Rule-based | Detects **vague words** (500+ curated terms) and **polysemous words** using WordNet synsets |
| **2** | Syntactic | Rule-based (spaCy) | Validates user story structure (`As a / I want / So that`) and grammar (subject-verb-object) |
| **3** | Semantic | Sentence Embeddings | Checks **domain relevance** using cosine similarity against an e-commerce dataset (MiniLM-L6-v2) |
| **4** | Pragmatic | Sentence Embeddings | Detects **duplicate/redundant** user stories across the session |
| **5** | ML-Based | Logistic Regression | Multi-label classification for 7 ambiguity types: Actor, Semantic, Scope, Acceptance, Dependency, Priority, Technical |

### 🤖 AI-Powered Ambiguity Removal
- Uses **LLaMA 3.3 70B** (via Groq API) to intelligently rewrite ambiguous user stories
- Preserves original intent while making language precise and measurable
- Returns structured explanations of each fix applied

### ⚡ Automated Test Case Generation
- Fine-tuned **Flan-T5** model converts user stories into Gherkin-style acceptance criteria
- NLP parser extracts structured entities (actor, goal, benefit, preconditions, steps, expected results)
- Generates formatted test cases with auto-incrementing IDs (`TC-001`, `REQ-001`)

### 📊 ML-Based Test Priority Prediction
- **Random Forest Regressor** predicts four quality metrics from user story text:
  - Defect Count, Development Time, Story Points, Customer Satisfaction
- Weighted hybrid formula calculates final priority score → `Very High`, `High`, `Medium`, `Low`

### 🔄 Duplicate Detection
- Sentence-level semantic comparison using **all-MiniLM-L6-v2** embeddings
- Cosine similarity threshold (≥ 0.75) flags redundant requirements

### 📋 Traceability Matrix
- Auto-generated requirements traceability matrix linking test cases to requirements
- Visual mapping of test coverage

### 📤 Export Options
- Export test cases to **CSV** and **PDF** formats
- Includes all fields: Test Case ID, Requirement ID, Test Case, Precondition, Steps, Expected Result, Priority

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                │
│                    React + Vite + TailwindCSS                   │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │UserStory │ │Ambiguity │ │TestCases │ │ Export   │           │
│  │  Input   │ │  Check   │ │ Display  │ │ Buttons  │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
│  ┌──────────┐ ┌──────────┐                                      │
│  │ Status   │ │ Matrix   │                                      │
│  │  Badge   │ │  Panel   │                                      │
│  └──────────┘ └──────────┘                                      │
└──────────────────────────┬──────────────────────────────────────┘
                           │ REST API (axios)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND (Flask)                              │
│                                                                  │
│  ┌─────────────────┐   ┌────────────────────┐                   │
│  │ validator.py     │   │ ambiguityRemover.py│                   │
│  │ (Rule-based +    │   │ (Groq/LLaMA 3.3   │                   │
│  │  ML Ambiguity)   │   │  API Integration)  │                   │
│  └─────────────────┘   └────────────────────┘                   │
│  ┌─────────────────┐   ┌────────────────────┐                   │
│  │ generator.py     │   │ prioritizer.py     │                   │
│  │ (Flan-T5 Model)  │   │ (Random Forest)    │                   │
│  └─────────────────┘   └────────────────────┘                   │
│  ┌─────────────────┐   ┌────────────────────┐                   │
│  │ nlp.py           │   │ dublicateRemover.py│                   │
│  │ (Entity Parser)  │   │ (Semantic Search)  │                   │
│  └─────────────────┘   └────────────────────┘                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ML MODELS                                   │
│  • Flan-T5 (User Story → Acceptance Criteria)                    │
│  • all-MiniLM-L6-v2 (Sentence Embeddings)                       │
│  • Logistic Regression (Ambiguity Classification)                │
│  • Random Forest Regressor (Priority Prediction)                 │
│  • E-Commerce Dataset Embeddings (.pt)                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|-----------|---------|
| **Python 3.10+** | Core backend language |
| **Flask** | REST API server |
| **spaCy** (`en_core_web_sm`) | NLP parsing, POS tagging, dependency parsing |
| **NLTK** (WordNet, Stopwords) | Polysemy detection, lexical analysis |
| **HuggingFace Transformers** | Flan-T5 model for test case generation |
| **Sentence-Transformers** | MiniLM-L6-v2 for semantic similarity |
| **scikit-learn** | Logistic Regression & Random Forest models |
| **PyTorch** | Deep learning inference |
| **Groq API** (LLaMA 3.3 70B) | LLM-powered ambiguity removal |

### Frontend
| Technology | Purpose |
|-----------|---------|
| **React 19** | UI framework |
| **Vite 7** | Build tool & dev server |
| **TailwindCSS 4** | Utility-first CSS styling |
| **Axios** | HTTP client for API calls |
| **jsPDF** | PDF export functionality |

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.10+**
- **Node.js 18+** and **npm**
- **Git**

### 1. Clone the Repository
```bash
git clone https://github.com/SaadHasan007/RaBilS-2.0.git
cd RaBilS-2.0/Test-RaBilS-FYP
```

### 2. Backend Setup
```bash
# Create and activate virtual environment
cd backend
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1

# Install Python dependencies
pip install flask flask-cors transformers torch spacy scikit-learn sentence-transformers nltk groq python-dotenv

# Download spaCy model
python -m spacy download en_core_web_sm

# Download NLTK data
python -c "import nltk; nltk.download('wordnet'); nltk.download('stopwords')"
```

### 3. Configure Environment Variables
Create a `.env` file in the `backend/` directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```
> Get a free API key at [console.groq.com](https://console.groq.com)

### 4. Start the Backend Server
```bash
cd backend
python server.py
```
The Flask server will start on **http://localhost:5000**

### 5. Frontend Setup (New Terminal)
```bash
cd frontend
npm install
npm run dev
```
The Vite dev server will start on **http://localhost:5173**

### 6. Open the App
Navigate to **http://localhost:5173** in your browser 🎉

---

## 📁 Project Structure

```
Test-RaBilS-FYP/
├── backend/
│   ├── .env                          # API keys (GROQ_API_KEY)
│   ├── server.py                     # Flask REST API server
│   ├── modules/
│   │   ├── validator.py              # Multi-level ambiguity detection (rule + ML)
│   │   ├── ambiguityRemover.py       # LLM-powered ambiguity removal (Groq/LLaMA)
│   │   ├── generator.py              # Flan-T5 test case generation
│   │   ├── prioritizer.py            # Random Forest priority prediction
│   │   ├── nlp.py                    # User story & acceptance criteria parser
│   │   └── dublicateRemover.py       # Semantic duplicate detection
│   └── models/
│       ├── flan-t5-us-to-ac-v1/      # Fine-tuned Flan-T5 model
│       ├── all-MiniLM-L6-v2/         # Sentence embedding model
│       ├── logistic_regression_model/ # Ambiguity classification model
│       ├── priority_model/           # Priority prediction model
│       └── userstory_dataset_embeddings.pt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                   # Main application component
│   │   ├── components/
│   │   │   ├── UserStoryInput.jsx    # Text input for user stories
│   │   │   ├── AmbiguityCheck.jsx    # Ambiguity analysis results display
│   │   │   ├── TestCasesDisplay.jsx  # Test case table view
│   │   │   ├── MatrixPanel.jsx       # Traceability matrix
│   │   │   ├── ExportButtons.jsx     # CSV & PDF export
│   │   │   └── StatusBadge.jsx       # Processing status indicator
│   │   └── services/
│   │       └── api.js                # Axios API client
│   └── package.json
│
└── README.md
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/ambiguityReport` | Analyze user story for ambiguities (hybrid rule + ML) |
| `POST` | `/api/ambiguityRemove` | Remove ambiguities using LLM (Groq/LLaMA 3.3) |
| `POST` | `/api/generate` | Generate test cases from user story |
| `POST` | `/api/dublicates` | Check for duplicate user stories |
| `GET` | `/api/testcase_list` | Retrieve all generated test cases |
| `DELETE` | `/api/testcase_list` | Clear all test cases and reset IDs |

---

## 📸 How It Works

1. **Enter a User Story** — Type an agile user story in the format: *"As a [role], I want [goal], so that [benefit]."*
2. **Check Ambiguity** — The system runs 5-level analysis (lexical, syntactic, semantic, pragmatic, ML) and generates a detailed report
3. **Auto-Fix Ambiguity** — LLaMA 3.3 70B rewrites the story to eliminate detected issues
4. **Generate Test Cases** — The cleaned story is processed by Flan-T5 to produce acceptance criteria, which are then structured into test cases with preconditions, steps, and expected results
5. **View & Export** — Review test cases in a table, inspect the traceability matrix, and export to CSV or PDF

---

## 👥 Team

| Name | Role |
|------|------|
| **Saad** | Full-Stack Development, System Integration |
| **Rafi** | NLP & ML Model Development |
| **Bilal** | Research & Testing |

---

## 📜 License

This project is developed as a **Final Year Project (FYP)** for academic purposes.

---

<p align="center">
  Made with ❤️ by <strong>Saad, Rafi & Bilal</strong>
</p>
