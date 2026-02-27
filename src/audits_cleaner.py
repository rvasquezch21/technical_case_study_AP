import pandas as pd
import numpy as np
import logging
import os
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """Loads a CSV file into a DataFrame with basic error handling."""
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return None
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Successfully loaded {len(df)} records from {file_path}")
        return df
    except Exception as e:
        logger.error(f"Error loading CSV: {e}")
        return None


def clean_risk_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the Risk_Score column by coercing non-numeric data to NaN
    and filling with 0.
    """
    logger.info("Cleaning 'Risk_Score' column...")
    # errors='coerce' turns strings like "error_reading" or "ninety" into NaN
    df['Risk_Score'] = pd.to_numeric(df['Risk_Score'], errors='coerce').fillna(0)
    # Ensure float/int type for mathematical comparisons
    df['Risk_Score'] = df['Risk_Score'].astype(float)
    return df


def apply_flagging_logic(df: pd.DataFrame) -> pd.DataFrame:
    """Applies business logic to flag high-risk records."""
    logger.info("Applying High_Risk_Flag logic...")

    # Requirement: Status == "Fail" AND Risk_Score > 80
    df['High_Risk_Flag'] = (df['Status'] == 'Fail') & (df['Risk_Score'] > 80)

    flagged_count = df['High_Risk_Flag'].sum()
    logger.info(f"Flagging complete. {flagged_count} high-risk records identified.")
    return df


def save_data(df: pd.DataFrame, output_path: str) -> None:
    """Saves the processed DataFrame to the specified path."""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        logger.info(f"Processed data saved to {output_path}")
    except Exception as e:
        logger.error(f"Failed to save data: {e}")


def main():
    # Path configuration based on project structure
    input_file = "data/data.csv"
    output_file = "output/cleaned_audits.csv"

    # Execution Flow
    df = load_data(input_file)

    if df is not None:
        df = clean_risk_scores(df)
        df = apply_flagging_logic(df)
        save_data(df, output_file)
    else:
        logger.critical("Pipeline aborted: Input data could not be processed.")


if __name__ == "__main__":
    main()