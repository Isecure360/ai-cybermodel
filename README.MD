# 🛡️ Phishing Detection System

An end-to-end, production-ready machine learning system for detecting phishing URLs using feature engineering, ensemble models, automated pipelines, and an interactive dashboard.

---

## 🚀 Overview

This system automatically:

* Ingests new datasets dropped into `data/raw/`
* Extracts and engineers URL-based features
* Trains multiple ML models
* Evaluates performance using precision, recall, and F1-score
* Builds ensemble models from top performers
* Saves and versions the best models
* Serves predictions via API
* Provides a Streamlit dashboard for interaction

---

## 🧠 Architecture

```text
data/raw → ingestion → feature engineering → training → evaluation → 
top models → ensemble → registry → API → UI dashboard
```

---

## 📂 Project Structure

```text
phishing-detector/
│
├── app/                      # FastAPI backend
│   ├── services/
│   │   ├── predictor.py
│   │   ├── model_loader.py
│   │   └── feature_engineering.py
│
├── src/                      # ML pipeline
│   ├── pipelines/
│   │   └── training_pipeline.py
│   ├── data/
│   ├── features/
│   ├── models/
│   │   ├── model_catalog.py
│   │   ├── ensemble.py
│   │   ├── performance.py
│   │   ├── save_results.py
│   │   ├── registry.py
│   │   └── split.py
│
├── ui/                       # Streamlit dashboard
│   ├── app.py
│   ├── utils.py
│   ├── components/
│   ├── assets/
│   └── data/
│
├── data/
│   └── raw/                  # Drop new datasets here
│
├── models/                   # Saved models + registry
│   └── registry.json
│
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repo

```bash
git clone <repo-url>
cd phishing-detector
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🧪 Running the System

### 🔹 Run Training Pipeline

```bash
python -m src.pipelines.training_pipeline
```

This will:

* Load all datasets from `data/raw/`
* Train multiple models
* Evaluate them
* Build an ensemble
* Save top 2 models
* Promote the best model to registry

---

### 🔹 Run API (FastAPI)

```bash
uvicorn app.main:app --reload
```

API Endpoints:

* `POST /api/v1/predict`
* `GET /api/v1/metadata`

---

### 🔹 Run UI Dashboard

```bash
cd ui
streamlit run app.py
```

---

## 🧬 How the ML System Works

### 📥 Data Ingestion

* Automatically reads all datasets in `data/raw/`
* Handles different schemas
* Detects URL column dynamically

### 🧱 Feature Engineering

* Extracts features from URLs
* Aligns all datasets to a unified feature schema

### 🤖 Model Training

* Multiple models trained (from `model_catalog.py`)
* Metrics computed:

  * Precision
  * Recall
  * F1 Score

### 🧠 Ensemble Learning

* Top 2 models selected
* Combined into an ensemble model

### 💾 Model Versioning

Each saved model includes:

* Model file (`model.pkl`)
* Feature schema (`features.pkl`)
* Metrics (`metrics.json`)
* Confusion matrix
* Classification report

Naming format:

```text
modelname_results_YYYYMMDD_HHMMSS/
```

---

## 🏆 Model Registry

The best model is promoted to:

```json
models/registry.json
```

Used by the API for live predictions.

---

## 🔮 Prediction Flow

```text
User → UI → API → Model Loader → Feature Extraction → Prediction → Response
```

---

## 🎨 UI Features

* 🔗 Single URL prediction
* 📁 Batch upload (CSV/Excel)
* 📊 Probability visualization
* 📜 Prediction history
* 🤖 Model metadata display
* 📈 Dashboard (metrics + charts)

---

## 📊 Metrics Used

* Precision
* Recall
* F1 Score (primary metric)
* Confusion Matrix
* Classification Report

---

## 🧩 Extending the System

### Add a New Model

Edit:

```text
src/models/model_catalog.py
```

---

### Add New Features

Edit:

```text
app/services/feature_engineering.py
```

---

### Modify Training Logic

Edit:

```text
src/pipelines/training_pipeline.py
```

---

### Improve UI

Edit:

```text
ui/components/
ui/assets/styles.css
```

---

## 🧠 Advanced Features (Planned / In Progress)

* Ensemble blending (multi-model voting)
* Drift detection (data distribution monitoring)
* Experiment tracking
* Model performance dashboard
* Real-time streaming predictions

---

## 🤝 Contribution Guide

### 🔹 Before Contributing

* Pull latest changes
* Create a new branch:

```bash
git checkout -b feature/your-feature-name
```

---

### 🔹 Code Standards

* Modular code (no monoliths)
* Reusable components
* Clear function naming
* Add docstrings

---

### 🔹 Commit Style

```text
feat: add new model
fix: resolve prediction bug
refactor: improve pipeline structure
```

---

### 🔹 Pull Request Checklist

* [ ] Code runs without errors
* [ ] Tested locally
* [ ] No hardcoded paths
* [ ] Follows project structure

---

## ⚠️ Important Notes

* Ensure `registry.json` exists before running predictions
* Ensure backend is running before launching UI
* Dataset must contain at least one URL column

---

## 💡 Philosophy

This is not just a model.
It’s a **self-evolving ML system** designed for:

* Scalability
* Automation
* Continuous improvement

---

## 👨‍💻 Author

Built as a scalable ML system for real-world phishing detection.

* Badges (build, version, license)

Just say the word 
