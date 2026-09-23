# System Architecture

## Overview
Governance-Ai is a Streamlit-based governance documentation platform. It accepts model metadata and an optional CSV dataset, evaluates documentation evidence, profiles the dataset, and generates governance artifacts.

## Architecture

User / CSV
  ↓
Model & Dataset Metadata
  ↓
Dataset Profiler + Governance Rules Engine
  ↓
Completeness + Risk + Governance Gaps
  ↓
Model Card + Dataset Datasheet + Governance Report
  ↓
JSON / Markdown / PDF exports

## Components
### 1. Streamlit UI
Collects project metadata, accepts CSV uploads, displays analysis results, and provides downloads.

### 2. Dataset Profiler
Uses Pandas to inspect row count, column count, missing cells, duplicate rows, data types, unique values, and numeric ranges.

### 3. Governance Rules Engine
Checks whether required governance evidence has been supplied for purpose, limitations, provenance, privacy, fairness, security, monitoring, and performance.

### 4. Risk Engine
Converts governance findings into a simple Low/Medium/High review level. A potentially high-impact purpose triggers additional human review.

### 5. Documentation Generator
Transforms collected information into a Model Card, Dataset Datasheet, and Governance Report.

### 6. Export Layer
Allows the generated package to be downloaded as JSON, Markdown, or PDF.

## Data flow
1. User enters model information.
2. Optional CSV is parsed.
3. Dataset profile is generated.
4. Governance checks run against submitted evidence.
5. Completeness and risk are calculated.
6. Documentation artifacts are assembled.
7. Results are displayed and exported.

## Design principles
- Human review remains required.
- Missing evidence is surfaced rather than silently assumed.
- The tool does not claim legal or regulatory certification.
- Dataset profiling is descriptive and does not prove dataset quality.