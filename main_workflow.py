import os
import pandas as pd
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment
load_dotenv()

# Logger configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def initialize_genai_client() -> genai.Client:
    """Initializes the Vertex AI client using .env config."""
    return genai.Client(vertexai=True)

def run_compliance_agent(client: genai.Client, row: pd.Series) -> str:
    """Sends a specific high-risk row to Gemini for email drafting."""
    system_instruction = (
        "You are a Senior Compliance Communication Agent. Draft a formal, urgent "
        "warning email to the Compliance Director. Use only the provided Audit_ID "
        "and Risk_Score. Do not hallucinate failure reasons. Tone: Professional/Objective."
    )
    
    prompt = f"Data: Audit_ID: {row['Audit_ID']}, Risk_Score: {row['Risk_Score']}, Status: {row['Status']}"
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2
            )
        )
        return response.text.strip()
    except Exception as e:
        logger.error(f"Failed to draft for {row['Audit_ID']}: {e}")
        return "Drafting error."

def main():
    # 1. Load and Clean (Logic from Part 1)
    logger.info("Starting Data Cleaning Pipeline...")
    input_path = "src/data/data.csv"
    output_path = "src/output/cleaned_audits.csv"
    
    if not os.path.exists(input_path):
        logger.error(f"Input file missing at {input_path}")
        return

    df = pd.read_csv(input_path)
    
    # Cleaning Risk_Score
    df['Risk_Score'] = pd.to_numeric(df['Risk_Score'], errors='coerce').fillna(0)
    
    # Flagging Logic
    df['High_Risk_Flag'] = (df['Status'] == 'Fail') & (df['Risk_Score'] > 80)
    
    # Save cleaned data
    os.makedirs("src/output/", exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Cleaned data saved to {output_path}")

    # 2. Trigger AI Agent (Logic from Part 2)
    high_risk_cases = df[df['High_Risk_Flag'] == True]
    
    if high_risk_cases.empty:
        logger.info("No high-risk records detected. Process finished.")
        return

    logger.info(f"Found {len(high_risk_cases)} high-risk records. Initializing AI Agent...")
    client = initialize_genai_client()
    
    for idx, row in high_risk_cases.iterrows():
        logger.info(f"Drafting email for Audit {row['Audit_ID']}...")
        email_draft = run_compliance_agent(client, row)
        
        # Output the draft (In production, this would go to an Email API or a DB)
        print("-" * 50)
        print(f"REPORT FOR AUDIT {row['Audit_ID']}")
        print(email_draft)
        print("-" * 50)

if __name__ == "__main__":
    main()