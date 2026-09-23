import io
import json
import pandas as pd
import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="AI Governance Platform", page_icon="🛡️", layout="wide")

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
    "Monitoring Plan": "Review model performance and data drift periodically."
}

def risk_check(data: dict):
    checks = []
    rules = [
        ('Purpose & intended use', bool(data.get('Purpose') and data.get('Intended Use')), 'Document the problem, intended users, and prohibited uses.'),
        ('Model limitations', bool(data.get('Limitations')), 'Describe known limitations, failure modes, and out-of-scope use.'),
        ('Data provenance', bool(data.get('Data Source')), 'Document the dataset source, collection process, and provenance.'),
        ('Privacy', bool(data.get('Privacy Review')), 'Document personal-data handling, retention, consent/legal basis, and access controls.'),
        ('Fairness', bool(data.get('Fairness Evaluation')), 'Evaluate relevant subgroup performance and document the methodology.'),
        ('Security', bool(data.get('Security Notes')), 'Document access controls, threats, abuse cases, and security mitigations.'),
        ('Monitoring', bool(data.get('Monitoring Plan')), 'Define post-deployment monitoring, drift checks, and retraining criteria.'),
        ('Performance metrics', bool(data.get('Metrics')), 'Report appropriate evaluation metrics and test conditions.')
    ]
    for area, ok, action in rules:
        checks.append({'Area': area, 'Status': 'Complete' if ok else 'Gap', 'Recommendation': '' if ok else action})
    purpose = (data.get('Purpose') or '').lower()
    terms = ['medical','healthcare','credit','loan','hiring','employment','admission','insurance','criminal']
    if any(term in purpose for term in terms):
        checks.append({'Area':'High-impact domain','Status':'Review','Recommendation':'Use domain-specific validation, documented human oversight, and additional governance controls before deployment.'})
    return checks

def risk_level(checks):
    gaps = sum(c['Status'] == 'Gap' for c in checks)
    reviews = sum(c['Status'] == 'Review' for c in checks)
    if gaps >= 5 or reviews >= 1: return 'High'
    if gaps >= 2: return 'Medium'
    return 'Low'
def model_card(data, checks):
    return {
        "model_details": {"name": data["Model Name"], "version": data["Model Version"], "type": data["Model Type"], "algorithm": data["Training Algorithm"]},
        "intended_use": {"purpose": data["Purpose"], "users": data["Intended Users"], "use": data["Intended Use"]},
        "performance": data["Metrics"],
        "limitations": data["Limitations"],
        "data": {"dataset": data["Training Dataset"], "source": data["Data Source"], "records": data["Records"], "features": data["Features"]},
        "governance": {"privacy": data["Privacy Review"], "fairness": data["Fairness Evaluation"], "security": data["Security Notes"], "monitoring": data["Monitoring Plan"]},
        "governance_gaps": [c for c in checks if c["Status"] != "Complete"]
    }

def dataset_datasheet(data):
    return {
        "dataset_name": data["Training Dataset"],
        "source": data["Data Source"],
        "records": data["Records"],
        "features": data["Features"],
        "intended_use": data["Intended Use"],
        "privacy": data["Privacy Review"],
        "limitations": data["Limitations"],
        "fairness_notes": data["Fairness Evaluation"]
    }

def pdf_report(data, checks):
    pdf=FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica","B",18)
    pdf.cell(0,10,"AI Governance Report",ln=True)
    pdf.set_font("Helvetica","",11)
    pdf.ln(4)
    pdf.multi_cell(0,7,f"Model: {data['Model Name']} | Version: {data['Model Version']}")
    pdf.ln(3)
    for key in ["Purpose","Model Type","Training Algorithm","Intended Users","Intended Use","Training Dataset","Data Source","Metrics"]:
        pdf.set_font("Helvetica","B",11); pdf.multi_cell(0,6,key)
        pdf.set_font("Helvetica","",10); pdf.multi_cell(0,6,str(data[key])); pdf.ln(1)
    pdf.add_page()
    pdf.set_font("Helvetica","B",15); pdf.cell(0,9,"Governance Assessment",ln=True); pdf.ln(3)
    for c in checks:
        pdf.set_font("Helvetica","B",10); pdf.multi_cell(0,6,f"{c['Area']}: {c['Status']}")
        if c["Recommendation"]:
            pdf.set_font("Helvetica","",10); pdf.multi_cell(0,6,c["Recommendation"])
        pdf.ln(2)
    return bytes(pdf.output())

st.title("🛡️ AI Governance Documentation Platform")
st.caption("Generate Model Cards, Dataset Datasheets, and governance gap reports from structured AI/ML project information.")

with st.sidebar:
    st.header("Project")
    st.write("Group 16")
    st.write("Governance-Ai")
    uploaded = st.file_uploader("Optional: upload a CSV dataset", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
    st.success(f"Dataset loaded: {len(df):,} rows × {len(df.columns):,} columns")
    st.dataframe(df.head(10), use_container_width=True)
    st.session_state["dataset_preview"] = {
        "records": str(len(df)),
        "features": ", ".join(df.columns.astype(str))
    }

st.subheader("1. Model & dataset information")
cols = st.columns(2)
data = {}
for i, (key, default) in enumerate(DEFAULT_FIELDS.items()):
    with cols[i % 2]:
        data[key] = st.text_area(key, value=default, height=70 if len(default)>80 else 55)

if uploaded:
    data["Records"] = st.session_state["dataset_preview"]["records"]
    data["Features"] = st.session_state["dataset_preview"]["features"]

if st.button("Generate Governance Package", type="primary", use_container_width=True):
    checks = risk_check(data)
    completeness = round(sum(c["Status"] == "Complete" for c in checks) / len(checks) * 100)
    card = model_card(data, checks)
    datasheet = dataset_datasheet(data)

    st.session_state["checks"] = checks
    st.session_state["card"] = card
    st.session_state["datasheet"] = datasheet
    st.session_state["data"] = data
    st.session_state["completeness"] = completeness
    st.session_state["risk_level"] = risk_level(checks)

if "checks" in st.session_state:
    st.divider()
    st.subheader("2. Governance dashboard")
    c1,c2,c3 = st.columns(3)
    c1.metric("Documentation completeness", f"{st.session_state['completeness']}%")
    gaps = sum(x["Status"] != "Complete" for x in st.session_state["checks"])
    c2.metric("Governance gaps", gaps)
    c3.metric("Checks performed", len(st.session_state["checks"]))
    st.metric("Overall governance risk", st.session_state["risk_level"])

    st.dataframe(pd.DataFrame(st.session_state["checks"]), use_container_width=True, hide_index=True)

    st.subheader("3. Recommended actions")
    for row in st.session_state["checks"]:
        if row["Status"] != "Complete":
            st.warning("**" + row["Area"] + " — " + row["Status"] + "**: " + row["Recommendation"])

    tab1,tab2,tab3=st.tabs(["Model Card","Dataset Datasheet","JSON / Export"])
    with tab1:
        st.json(st.session_state["card"])
    with tab2:
        st.json(st.session_state["datasheet"])
    with tab3:
        package = {
            "model_card": st.session_state["card"],
            "dataset_datasheet": st.session_state["datasheet"],
            "governance_checks": st.session_state["checks"]
        }
        text=json.dumps(package,indent=2)
        st.download_button("Download JSON package", text, file_name="governance_package.json", mime="application/json")
        st.download_button("Download PDF report", pdf_report(st.session_state["data"], st.session_state["checks"]), file_name="ai_governance_report.pdf", mime="application/pdf")

st.divider()
st.info("This prototype is a documentation and governance aid. It does not certify regulatory compliance or replace human review.")
