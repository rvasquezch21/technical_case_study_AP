# technical_case_study_AP
Case study for AP, an automation of a data cleaning process for the analysis of an AI Agent using the Gemini API, while also designing a scalable cloud infrastructure on Google Cloud Platform (GCP) to handle the pipeline, and a visual orchestration.


# Audit Data & AI Agent Pipeline

## Overview
Automated pipeline to clean audit datasets and trigger a Gemini AI Agent to draft 
compliance emails for high-risk records (Risk Score > 80 and Status: Fail).

## Setup
1. **Environment:** Place your `.env` file in the root directory.
2. **Key:** Ensure your Service Account JSON is at the path specified in `.env`.
3. **Install Dependencies:**
   ```bash
   pip3 install -r requirements.txt