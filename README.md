# MQMR Automated Compliance Audit Pipeline

This repository contains an enterprise-grade automation solution for processing mortgage audit data. The system leverages **Python**, **Google Cloud Platform (GCP)**, and **n8n** to transform raw CSV data into actionable, AI-generated compliance drafts.

---

## 🚀 Project Overview

The project is divided into four distinct phases, moving from core data logic to a fully orchestrated cloud ecosystem.

### Phase 1: Data Engineering & Cleaning
* **Logic:** A robust Python script cleans raw audit CSVs by handling missing values, standardizing date formats, and validating data types.
* **Scoring:** Implements a custom risk-scoring algorithm that assigns a weight to each compliance failure.

### Phase 2: AI Agent & Prompt Engineering
* **Intelligence:** Integration with **Gemini 1.5 Flash** via the Vertex AI API.
* **Hallucination Prevention:** Utilizes role-prompting (Senior Compliance Director) and strict grounding constraints to ensure the AI only uses provided audit data.

### Phase 3: Cloud Infrastructure (GCP)
* **Event-Driven:** Uses **Google Cloud Storage** and **Eventarc** to trigger workflows automatically upon file upload.
* **Scalability:** Orchestrated via **Cloud Workflows** and executed within **Cloud Run Jobs** for serverless, high-performance processing.

### Phase 4: Operational Orchestration (n8n)
* **Monitoring:** A visual workflow in **n8n** provides a "Control Tower" for the operations team.
* **Delivery:** Automated routing of high-risk drafts to **Slack** and persistent logging in **Google Sheets**.

---

## 🛠️ Setup & Execution

### 1. Local Environment
1.  Clone the repository.
2.  Install dependencies: `pip install -r requirements.txt`.
3.  Set your Google Application Credentials:
    `export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account.json"`

### 2. Execution via CLI
To run the primary cleaning and analysis script:
```bash
python main_workflow.py --input test_audit.csv --output cleaned_audit.csv