# Governance-Ai

## AI Governance Documentation & Model Card Generation Platform

**Group 16:** Vaarun Saini, Fahad Maksud Khan, Aryan Khalkho

Governance-Ai is an academic Streamlit platform that turns AI/ML model and dataset information into structured governance documentation and an actionable risk review.

## What the project does

**Input**
- Model name, version, type and training algorithm
- Purpose, intended users and intended use
- Limitations and performance metrics
- Dataset source, records and features
- Privacy, fairness, security and monitoring notes
- Optional CSV dataset

**Processing**
- Documentation completeness scoring
- Governance gap detection
- High-impact-domain review
- Dataset quality profiling
- Risk classification: Low / Medium / High
- Recommended governance actions

**Output**
- Model Card
- Dataset Datasheet
- Governance Assessment
- JSON governance package
- Markdown governance report
- PDF governance report

## Architecture

```
User / CSV
   ↓
Model & Dataset Metadata
   ↓
Dataset Profiler ─────────────┐
   ↓                         │
Governance Rules Engine       │
   ↓                         │
Completeness + Risk + Gaps ←─┘
   ↓
Model Card + Datasheet + Governance Report
   ↓
JSON / Markdown / PDF exports
```

## Governance checks

1. Purpose & intended use
2. Model limitations
3. Data provenance
4. Privacy
5. Fairness
6. Security
7. Monitoring
8. Performance metrics
9. High-impact-domain review when relevant

## Dataset profiling

When a CSV is uploaded, the platform reports:
- row and column count
- missing cells and average missingness
- duplicate rows
- data types
- unique values
- numeric minimum/maximum
- column preview

## Run locally

```bash
python -m venv .venv

# Windows
.venv\\Scripts\\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Demo

1. Open the app.
2. Click **Load demo dataset** or upload a CSV.
3. Review/edit model and governance information.
4. Click **Generate Governance Package**.
5. Review the dashboard and recommended actions.
6. Download JSON, Markdown, and PDF outputs.

## Project structure

```
Governance-Ai/
├── app.py
├── requirements.txt
├── sample_data.csv
├── README.md
├── .gitignore
└── docs/
    ├── PROJECT_REPORT.md
    └── DEMO_GUIDE.md
```

## Limitations

This is a classroom prototype. The rule-based governance assessment is not legal advice, regulatory certification, or a substitute for domain experts, security testing, privacy review, fairness analysis, or human oversight.

## Future scope

- LLM-assisted narrative generation with an optional API key
- More formal fairness metrics by subgroup
- Model evaluation artifact upload
- Versioned governance history
- Role-based access control
- Database storage and audit logs
- Standards-specific checklists
