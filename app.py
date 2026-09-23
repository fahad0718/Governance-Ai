import io
import json
from datetime import datetime, timezone

import pandas as pd
import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="Governance-Ai", page_icon="🛡️", layout="wide")

DEFAULT_FIELDS = {
    "Model Name": "Student Performance Predictor",
    "Model Version": "1.0",
    "Purpose": "Predict student academic performance from historical features.",
    "Model Type": "Classification",
    "Training Algorithm": "Random Forest",
    "Intended Users": "Teachers, academic analysts, and institutional administrators.",
    "Intended Use": "Early academic support and analysis; not a sole basis for high-impact decisions.",
    "Limitations": "Performance depends on data quality and may not generalize to new populations.",
    "Training Dataset": "Student performance dataset",
    "Data Source": "Institutional / public educational data",
    "Records": "1000",
    "Features": "Attendance, study hours, previous score, assignment completion",
    "Metrics": "Accuracy: 0.89; Precision: 0.87; Recall: 0.86; F1: 0.86",
    "Privacy Review": "No direct identifiers retained in the demonstration dataset.",
    "Fairness Evaluation": "Subgroup performance should be evaluated before deployment.",
    "Security Notes": "Protect training data and restrict access to generated reports.",
    "Monitoring Plan": "Review model performance and data drift periodically.",
}

GOVERNANCE_RULES = [
    ("Purpose & intended use", "Purpose and Intended Use", "Document the problem, intended users, benefits, and prohibited uses."),
    ("Model limitations", "Limitations", "Describe known limitations, failure modes, assumptions, and out-of-scope use."),
    ("Data provenance", "Data Source", "Document where the data came from, how it was collected, and its provenance."),
    ("Privacy", "Privacy Review", "Document personal-data handling, retention, consent/legal basis, anonymization, and access controls."),
    ("Fairness", "Fairness Evaluation", "Evaluate relevant subgroup performance and document the fairness methodology."),
    ("Security", "Security Notes", "Document access controls, threats, abuse cases, model/data protection, and mitigations."),
    ("Monitoring", "Monitoring Plan", "Define post-deployment monitoring, drift checks, incident handling, and retraining criteria."),
    ("Performance metrics", "Metrics", "Report appropriate evaluation metrics, test conditions, baseline, and validation data."),
]


def profile_dataset(df):
    numeric = df.select_dtypes(include="number")
    profile = {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_cells": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_rate": round(float(df.isna().mean().mean() * 100), 2),
        "numeric_columns": list(numeric.columns.astype(str)),
        "categorical_columns": [str(c) for c in df.columns if c not in numeric.columns],
        "columns": [],
    }
    for col in df.columns:
        s = df[col]
        item = {
            "name": str(col),
            "dtype": str(s.dtype),
            "missing": int(s.isna().sum()),
            "unique": int(s.nunique(dropna=True)),
        }
        if pd.api.types.is_numeric_dtype(s):
            item["min"] = float(s.min()) if not s.dropna().empty else None
            item["max"] = float(s.max()) if not s.dropna().empty else None
        profile["columns"].append(item)
    return profile


def risk_check(data):
    checks = []
    for area, field, action in GOVERNANCE_RULES:
        ok = bool(str(data.get(field, "")).strip())
        checks.append({
            "Area": area,
            "Status": "Complete" if ok else "Gap",
            "Recommendation": "" if ok else action,
        })

    purpose = str(data.get("Purpose", "")).lower()
    high_impact_terms = [
        "medical", "healthcare", "credit", "loan", "hiring", "employment",
        "admission", "insurance", "criminal", "legal", "welfare",
    ]
    if any(term in purpose for term in high_impact_terms):
        checks.append({
            "Area": "High-impact domain",
            "Status": "Review",
            "Recommendation": "Use domain-specific validation, documented human oversight, impact assessment, and additional governance controls before deployment.",
        })
    return checks


def risk_level(checks):
    gaps = sum(c["Status"] == "Gap" for c in checks)
    reviews = sum(c["Status"] == "Review" for c in checks)
    if reviews or gaps >= 5:
        return "High"
    if gaps >= 2:
        return "Medium"
    return "Low"


def score(checks):
    return round(sum(c["Status"] == "Complete" for c in checks) / len(checks) * 100)


def model_card(data, checks):
    return {
        "model_details": {
            "name": data["Model Name"],
            "version": data["Model Version"],
            "type": data["Model Type"],
            "algorithm": data["Training Algorithm"],
        },
        "intended_use": {
            "purpose": data["Purpose"],
            "users": data["Intended Users"],
            "use": data["Intended Use"],
        },
        "performance": data["Metrics"],
        "limitations": data["Limitations"],
        "data": {
            "dataset": data["Training Dataset"],
            "source": data["Data Source"],
            "records": data["Records"],
            "features": data["Features"],
        },
        "governance": {
            "privacy": data["Privacy Review"],
            "fairness": data["Fairness Evaluation"],
            "security": data["Security Notes"],
            "monitoring": data["Monitoring Plan"],
        },
        "governance_gaps": [c for c in checks if c["Status"] != "Complete"],
    }


def dataset_datasheet(data, profile=None):
    result = {
        "dataset_name": data["Training Dataset"],
        "source": data["Data Source"],
        "records": data["Records"],
        "features": data["Features"],
        "intended_use": data["Intended Use"],
        "privacy": data["Privacy Review"],
        "limitations": data["Limitations"],
        "fairness_notes": data["Fairness Evaluation"],
    }
    if profile:
        result["uploaded_dataset_profile"] = profile
    return result


def governance_markdown(data, checks, profile=None):
    risk = risk_level(checks)
    completeness = score(checks)
    gaps = [c for c in checks if c["Status"] != "Complete"]
    lines = [
        "# AI Governance Report",
        "",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Model:** {data['Model Name']}  ",
        f"**Version:** {data['Model Version']}",
        "",
        "## Executive summary",
        f"- Documentation completeness: **{completeness}%**",
        f"- Governance risk level: **{risk}**",
        f"- Governance items requiring attention: **{len(gaps)}**",
        "",
        "## Model overview",
        f"- **Purpose:** {data['Purpose']}",
        f"- **Type:** {data['Model Type']}",
        f"- **Algorithm:** {data['Training Algorithm']}",
        f"- **Intended users:** {data['Intended Users']}",
        f"- **Intended use:** {data['Intended Use']}",
        f"- **Limitations:** {data['Limitations']}",
        "",
        "## Dataset overview",
        f"- **Dataset:** {data['Training Dataset']}",
        f"- **Source:** {data['Data Source']}",
        f"- **Records:** {data['Records']}",
        f"- **Features:** {data['Features']}",
        "",
        "## Governance assessment",
        "",
        "| Area | Status |",
        "|---|---|",
    ]
    for c in checks:
        lines.append(f"| {c['Area']} | {c['Status']} |")
    lines += ["", "## Recommended actions", ""]
    if gaps:
        for c in gaps:
            lines.append(f"1. **{c['Area']}** — {c['Recommendation']}")
    else:
        lines.append("No documentation gaps were identified by the configured checks.")
    if profile:
        lines += [
            "",
            "## Uploaded dataset profile",
            f"- Rows: **{profile['rows']:,}**",
            f"- Columns: **{profile['columns']:,}**",
            f"- Missing cells: **{profile['missing_cells']:,}** ({profile['missing_rate']}% average cell missingness)",
            f"- Duplicate rows: **{profile['duplicate_rows']:,}**",
        ]
    lines += [
        "",
        "## Human review note",
        "This report is a governance documentation aid. It does not certify legal or regulatory compliance and should be reviewed by appropriate human stakeholders before deployment.",
    ]
    return "\n".join(lines)


def pdf_report(data, checks, profile=None):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "AI Governance Report", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, f"Model: {data['Model Name']} | Version: {data['Model Version']}", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, f"Documentation completeness: {score(checks)}%")
    pdf.multi_cell(0, 6, f"Overall governance risk: {risk_level(checks)}")
    pdf.ln(4)

    for key in ["Purpose", "Model Type", "Training Algorithm", "Intended Users", "Intended Use", "Limitations", "Training Dataset", "Data Source", "Records", "Features", "Metrics"]:
        pdf.set_font("Helvetica", "B", 10)
        pdf.multi_cell(0, 6, key)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, str(data[key]))
        pdf.ln(1)

    if profile:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 15)
        pdf.cell(0, 9, "Dataset Profile", ln=True)
        pdf.set_font("Helvetica", "", 10)
        for k, v in [
            ("Rows", f"{profile['rows']:,}"),
            ("Columns", f"{profile['columns']:,}"),
            ("Missing cells", f"{profile['missing_cells']:,}"),
            ("Average missingness", f"{profile['missing_rate']}%"),
            ("Duplicate rows", f"{profile['duplicate_rows']:,}"),
        ]:
            pdf.multi_cell(0, 6, f"{k}: {v}")

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(0, 9, "Governance Assessment", ln=True)
    pdf.ln(3)
    for c in checks:
        pdf.set_font("Helvetica", "B", 10)
        pdf.multi_cell(0, 6, f"{c['Area']}: {c['Status']}")
        if c["Recommendation"]:
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 6, c["Recommendation"])
        pdf.ln(2)
    return bytes(pdf.output())


st.title("🛡️ Governance-Ai")
st.caption("AI Governance Documentation & Model Card Generation Platform — Group 16")

with st.sidebar:
    st.header("Project")
    st.write("**Group 16**")
    st.write("Vaarun Saini • Fahad Maksud Khan • Aryan Khalkho")
    st.divider()
    st.header("Dataset")
    uploaded = st.file_uploader("Upload a CSV dataset (optional)", type=["csv"])
    demo = st.button("Load demo dataset", use_container_width=True)

if demo:
    demo_df = pd.DataFrame({
        "attendance": [82, 91, 67, 75, 88, 95, 61, 79],
        "study_hours": [5, 8, 2, 4, 6, 9, 1, 5],
        "previous_score": [72, 88, 55, 64, 81, 92, 49, 70],
        "assignment_completion": [0.9, 1.0, 0.6, 0.8, 0.95, 1.0, 0.5, 0.85],
        "performance": [1, 1, 0, 1, 1, 1, 0, 1],
    })
    st.session_state["demo_df"] = demo_df

df = None
if uploaded:
    try:
        df = pd.read_csv(uploaded)
    except Exception as exc:
        st.error(f"Could not read the CSV: {exc}")
elif "demo_df" in st.session_state:
    df = st.session_state["demo_df"]

profile = None
if df is not None:
    profile = profile_dataset(df)
    rows, columns = profile['rows'], profile['columns']
    st.success("Dataset loaded: " + str(rows) + " rows x " + str(columns) + " columns")
    a, b, c, d = st.columns(4)
    a.metric("Rows", f"{profile['rows']:,}")
    b.metric("Columns", f"{profile['columns']:,}")
    c.metric("Missing cells", f"{profile['missing_cells']:,}")
    d.metric("Duplicate rows", f"{profile['duplicate_rows']:,}")
    with st.expander("Preview dataset"):
        st.dataframe(df.head(10), use_container_width=True, hide_index=True)
    with st.expander("Column profile"):
        st.dataframe(pd.DataFrame(profile["columns"]), use_container_width=True, hide_index=True)

st.subheader("1. Model & dataset information")
cols = st.columns(2)
data = {}
for i, (key, default) in enumerate(DEFAULT_FIELDS.items()):
    with cols[i % 2]:
        data[key] = st.text_area(key, value=default, height=70 if len(default) > 80 else 55)

if profile:
    data["Records"] = str(profile["rows"])
    data["Features"] = ", ".join(df.columns.astype(str))

if st.button("Generate Governance Package", type="primary", use_container_width=True):
    checks = risk_check(data)
    card = model_card(data, checks)
    datasheet = dataset_datasheet(data, profile)
    package = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model_card": card,
        "dataset_datasheet": datasheet,
        "governance_checks": checks,
        "governance_risk": risk_level(checks),
        "documentation_completeness": score(checks),
        "dataset_profile": profile,
    }
    st.session_state["package"] = package
    st.session_state["checks"] = checks
    st.session_state["card"] = card
    st.session_state["datasheet"] = datasheet
    st.session_state["data"] = data
    st.session_state["profile"] = profile

if "package" in st.session_state:
    package = st.session_state["package"]
    checks = st.session_state["checks"]
    data = st.session_state["data"]
    profile = st.session_state["profile"]

    st.divider()
    st.subheader("2. Governance dashboard")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Documentation completeness", f"{score(checks)}%")
    c2.metric("Governance gaps", sum(x["Status"] != "Complete" for x in checks))
    c3.metric("Checks performed", len(checks))
    c4.metric("Overall risk", risk_level(checks))

    st.dataframe(pd.DataFrame(checks), use_container_width=True, hide_index=True)

    st.subheader("3. Recommended actions")
    for row in checks:
        if row["Status"] != "Complete":
            st.warning(f"**{row['Area']} — {row['Status']}**: {row['Recommendation']}")
    if all(row["Status"] == "Complete" for row in checks):
        st.success("All configured governance documentation checks are complete.")

    st.subheader("4. Generated governance documents")
    tab1, tab2, tab3, tab4 = st.tabs(["Model Card", "Dataset Datasheet", "Governance Report", "Exports"])

    with tab1:
        st.json(st.session_state["card"])
    with tab2:
        st.json(st.session_state["datasheet"])
    with tab3:
        report = governance_markdown(data, checks, profile)
        st.markdown(report)
    with tab4:
        report = governance_markdown(data, checks, profile)
        full_package = json.dumps(package, indent=2, default=str)
        st.download_button("Download JSON package", full_package, "governance_package.json", "application/json")
        st.download_button("Download Model Card", json.dumps(st.session_state["card"], indent=2), "model_card.json", "application/json")
        st.download_button("Download Dataset Datasheet", json.dumps(st.session_state["datasheet"], indent=2), "dataset_datasheet.json", "application/json")
        st.download_button("Download Governance Report (Markdown)", report, "ai_governance_report.md", "text/markdown")
        st.download_button("Download Governance Report (PDF)", pdf_report(data, checks, profile), "ai_governance_report.pdf", "application/pdf")

st.divider()
st.info("Academic prototype only: generated assessments support documentation and human review; they do not certify regulatory compliance.")
