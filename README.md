# Governance-Ai

## AI Governance Documentation & Model Card Generation Platform

A Streamlit-based prototype that takes structured AI/ML model and dataset information and generates:

- Model Cards
- Dataset Datasheets
- Governance gap / risk checks
- Documentation completeness score
- JSON governance package
- PDF governance report

### Project
**Group 16**

### Team
- Vaarun Saini
- Fahad Maksud Khan
- Aryan Khalkho

## Architecture

Model / Dataset Information → Governance Checks → Model Card + Dataset Datasheet → Governance Report

## Run locally

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Demo workflow

1. Enter model and dataset information.
2. Optionally upload a CSV dataset.
3. Click **Generate Governance Package**.
4. Review the completeness score and governance gaps.
5. Download the JSON package and PDF report.

## Scope

This repository is an academic prototype for AI governance documentation. The generated assessment is not legal or regulatory certification and should be reviewed by responsible humans before real-world use.


## Current prototype capabilities

The governance engine checks documentation completeness across purpose, limitations, data provenance, privacy, fairness, security, monitoring, and performance metrics. It also flags models whose stated purpose indicates a potentially high-impact domain for additional human review. The dashboard reports an overall Low/Medium/High risk level and produces recommended actions for identified gaps.
