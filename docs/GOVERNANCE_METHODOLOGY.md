# Governance Methodology

## Purpose
The governance engine is a lightweight checklist-based assessment designed for an academic prototype. It asks whether relevant documentation/evidence has been supplied; it does not independently prove compliance.

## Assessment areas
| Area | Evidence expected |
|---|---|
| Purpose & intended use | Problem definition, intended users, benefits, prohibited uses |
| Model limitations | Known limitations, assumptions, failure modes, out-of-scope use |
| Data provenance | Source, collection method, ownership/provenance |
| Privacy | Personal-data handling, retention, consent/legal basis, access controls |
| Fairness | Relevant subgroup evaluation and methodology |
| Security | Threats, access controls, abuse cases, mitigations |
| Monitoring | Drift, performance monitoring, incident handling, retraining criteria |
| Performance metrics | Metrics, validation method, test conditions, baseline |

## Risk logic
- Low: fewer than two documentation gaps and no high-impact review.
- Medium: two to four documentation gaps.
- High: five or more gaps, or a high-impact-domain review.

The risk level is a documentation-review signal, not a prediction of actual harm or legal compliance.

## High-impact review
The prototype looks for terms associated with potentially consequential domains such as healthcare, credit, hiring, admissions, insurance, criminal justice, legal services, and welfare. A match does not mean the system is unlawful or harmful. It simply requests stronger human review and domain-specific controls.

## Dataset profiling
For an uploaded CSV, the system calculates rows and columns, missing cells and average missingness, duplicate rows, data types, unique value counts, and numeric minimum and maximum values.

These statistics help reviewers identify issues for investigation. They do not replace statistical validation, privacy analysis, security testing, or fairness testing.

## Human oversight
Governance-Ai is intentionally designed as decision support. Final decisions about deployment, privacy, fairness, security, safety, and compliance remain with qualified people responsible for the system.