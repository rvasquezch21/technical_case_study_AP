import os
import logging
from fastapi import FastAPI, BackgroundTasks
from dotenv import load_dotenv
from main_workflow import run_full_pipeline # We import your logic
from google.cloud import storage
import pandas as pd

def load_data_from_gcs(bucket_name, file_name):
    """Downloads the triggering file from GCS into a dataframe."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    
    # Download as string and read into pandas
    data = blob.download_as_text()
    from io import StringIO
    return pd.read_csv(StringIO(data))

# In your main() function, change the path:
df = load_data_from_gcs("mqmr-weekly-audits-project-1", "test_audit.csv")

load_dotenv()

app = FastAPI()

logging.basicConfig(level=logging.INFO)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/process")
def process():
    # aquí llamarías tu lógica de limpieza/flagging
    return {"message": "processing started"}

@app.post("/")
async def trigger_audit(background_tasks: BackgroundTasks):
    """
    Cloud Run receives an HTTP POST from Eventarc. 
    We run the audit in the background so the 'health check' succeeds immediately.
    """
    logging.info("Audit trigger received. Starting pipeline...")
    background_tasks.add_task(run_full_pipeline)
    return {"status": "Processing started", "message": "Audit is running in background"}

if __name__ == "__main__":
    # Get port from environment or default to 8080
    port = int(os.environ.get("PORT", 8080))
    
    import uvicorn
    # IMPORTANT: host must be "0.0.0.0", NOT "127.0.0.1"
    uvicorn.run(app, host="0.0.0.0", port=port)