# Group 16 — Project Report

## Title
**AI Governance Documentation & Model Card Generation Platform**

## Problem statement
AI systems can be technically accurate while still lacking documentation about intended use, limitations, data provenance, privacy, fairness, security and monitoring. Teams need a repeatable way to collect this information and identify documentation gaps before deployment.

## Proposed solution
Governance-Ai is a web-based documentation assistant. Users enter model and dataset information and can optionally upload a CSV. The platform profiles the dataset, checks governance evidence, calculates a documentation completeness score, identifies gaps, classifies the governance review as Low/Medium/High, and generates reusable documentation.

## Objectives
- Standardize AI/ML governance documentation.
- Make missing governance evidence visible.
- Generate Model Cards and Dataset Datasheets.
- Provide a simple governance risk review.
- Profile uploaded datasets for basic quality indicators.
- Export results for project documentation and review.

## Modules

### 1. Metadata collection
Collects model identity, purpose, users, intended use, limitations, dataset information, metrics, privacy, fairness, security and monitoring notes.

### 2. Dataset profiler
Reads an optional CSV and calculates rows, columns, missing values, duplicates, data types, unique counts and numeric ranges.

### 3. Governance engine
Runs configurable documentation checks and creates recommendations for missing evidence. It also identifies descriptions that indicate potentially high-impact domains and asks for additional human review.

### 4. Documentation generator
Creates structured Model Card and Dataset Datasheet content.

### 5. Governance report
Produces an executive summary, governance assessment, recommended actions and dataset profile.

### 6. Export module
Provides JSON, Markdown and PDF outputs.

## Technology stack
- Python
- Streamlit
- Pandas
- FPDF2
- GitHub

## Workflow
1. User provides model information.
2. User optionally uploads a dataset.
3. Dataset profiler analyzes the CSV.
4. Governance engine checks documentation.
5. Completeness and risk are calculated.
6. Recommendations are displayed.
7. Governance documents are generated.
8. User downloads the results.

## Example use case
A student-performance prediction model is documented using model metadata and a sample dataset. Governance-Ai identifies whether evidence exists for privacy, fairness, security, monitoring and performance. The team can then improve missing documentation before presenting the model.

## Expected outcome
The project demonstrates how governance can be integrated into an ML workflow instead of being treated as documentation added at the end. The prototype creates a repeatable and auditable checklist-based process.

## Limitations
The current system does not independently prove fairness, privacy compliance, security, model accuracy or legal compliance. It checks whether relevant documentation/evidence has been supplied and highlights areas for human review.

## Future enhancements
- LLM-assisted explanations and document drafting
- Fairness metrics such as demographic parity and equalized odds
- Evaluation-result uploads
- Database and version history
- Authentication and role-based access
- Standards-specific governance templates
