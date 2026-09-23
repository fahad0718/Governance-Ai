# User Guide

## Requirements
- Python 3.10+ recommended
- Internet is not required after dependencies are installed

## Installation
python -m venv .venv

Windows:
`.venv\\Scripts\\activate`

macOS/Linux:
`source .venv/bin/activate`

Then:
`pip install -r requirements.txt`
`streamlit run app.py`

## Using the application
### Step 1 — Dataset
Use **Load demo dataset** for the prepared example, or upload a CSV.

### Step 2 — Metadata
Review the model name, version, purpose, model type, algorithm, users, intended use, limitations, dataset source, metrics, privacy, fairness, security, and monitoring information.

### Step 3 — Generate
Click **Generate Governance Package**.

### Step 4 — Review
Check the completeness percentage, governance gaps, number of checks, risk level, and recommendations.

### Step 5 — Export
Use the Exports tab to download JSON, Model Card, Dataset Datasheet, Markdown, and PDF artifacts.

## Troubleshooting
- If a CSV cannot be read, verify it is a valid comma-separated file.
- If dependencies are missing, run `pip install -r requirements.txt`.
- If Streamlit is unavailable, activate the virtual environment and reinstall requirements.