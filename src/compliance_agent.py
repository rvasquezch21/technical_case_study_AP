import pandas as pd
import logging
from typing import List, Dict
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# 1. Load variables from .env into os.environ
load_dotenv()

def initialize_agent() -> genai.Client:
    """
    Initializes the Vertex AI Gemini Client using .env values.
    The SDK automatically detects:
    - GOOGLE_CLOUD_PROJECT
    - GOOGLE_CLOUD_LOCATION
    - GOOGLE_API_KEY (used as the bearer token)
    """
    try:
        # No arguments needed; it reads directly from the environment
        client = genai.Client(vertexai=True)
        print(f"Connected to Project: {os.getenv('GOOGLE_CLOUD_PROJECT')}")
        return client
    except Exception as e:
        print(f"Error: Check your .env file and Token validity. {e}")
        raise

# Example Usage within your existing flow
def run_pipeline():
    client = initialize_agent()
    # ... rest of your logic from Part 2 ...

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# --- AGENT CONFIGURATION ---
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")
MODEL_ID = "gemini-2.5-flash"

SYSTEM_INSTRUCTION = """
You are a Senior Compliance Communication Agent. Your sole purpose is to draft formal, 
high-priority warning emails to the Compliance Director based on 'High Risk' audit records.

Core Instructions:
1. Strict Data Adherence: Use only the provided Audit_ID and Risk_Score. 
2. Tone: Authoritative, urgent, and objective. Avoid "disaster" language.
3. No Hallucinations: Do not invent failure reasons or regulations. If unknown, 
   state "specific failure triggers are under review."
4. Structure: 
   - Subject: [URGENT] Audit_ID
   - Body: Summary, data table, and "Next Steps" call to action.
"""


def initialize_agent() -> genai.Client:
    """Initializes the Vertex AI Gemini Client."""
    return genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION
    )


def draft_compliance_email(client: genai.Client, audit_data: Dict) -> str:
    """Generates a single email draft using Gemini."""
    prompt = f"Draft email for the following data: {audit_data}"

    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.2,  # Low temperature to ensure consistency
            )
        )
        return response.text
    except Exception as e:
        logger.error(f"AI Generation failed for Audit {audit_data.get('Audit_ID')}: {e}")
        return "Draft generation failed."


def process_high_risk_audits(input_csv: str) -> None:
    """Reads cleaned data and triggers the AI agent for flagged records."""
    df = pd.read_csv(input_csv)

    # Filter for flagged records only
    high_risk_df = df[df['High_Risk_Flag'] == True]

    if high_risk_df.empty:
        logger.info("No high-risk audits found. No emails to draft.")
        return

    client = initialize_agent()
    logger.info(f"Processing {len(high_risk_df)} high-risk records...")

    for _, row in high_risk_df.iterrows():
        audit_info = {
            "Audit_ID": row['Audit_ID'],
            "Risk_Score": row['Risk_Score'],
            "Status": row['Status']
        }
        draft = draft_compliance_email(client, audit_info)

        # In a real pipeline, you'd save this to a DB or send via SendGrid/SMTP
        print(f"\n--- DRAFT FOR {row['Audit_ID']} ---\n{draft}\n")


if __name__ == "__main__":
    process_high_risk_audits("src/output/cleaned_audits.csv")