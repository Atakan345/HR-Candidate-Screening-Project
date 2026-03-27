import logging
import os
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from services.pdf_processor import extract_text_from_pdf
from services.ai_evaluator import evaluate_candidate
from services.sheets_logger import save_to_sheets
from services.slack_notifier import send_slack_notification

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="HR Candidate Screening Pipeline")

# Setup Jinja2 templates
os.makedirs("templates", exist_ok=True)
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/v1/analyze-cv")
async def analyze_cv(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return {"status": "error", "message": "Only PDF files are supported"}
        
    logger.info(f"Processing uploaded file: {file.filename}")
    
    # 1. Read and extract text
    file_bytes = await file.read()
    try:
        cv_text = extract_text_from_pdf(file_bytes)
        logger.info(f"Extracted {len(cv_text)} characters from PDF.")
    except Exception as e:
        logger.error(f"Failed to read PDF: {e}")
        return {"status": "error", "message": f"Failed to read PDF: {str(e)}"}
        
    if not cv_text.strip():
        return {"status": "error", "message": "Could not extract any text from the PDF. Ensure it is not an image-based PDF."}
        
    # 2. Analyze with AI
    logger.info("Sending text to AI for evaluation...")
    analysis_result = evaluate_candidate(cv_text)
    
    # 3. Save to Google Sheets
    logger.info("Saving results to Google Sheets...")
    sheets_success, sheets_msg = save_to_sheets(analysis_result)
    
    # 4. Notify Slack if Senior
    slack_success = None
    slack_msg = None
    classification = str(analysis_result.get("classification", "")).strip().lower()
    if classification == "senior":
        logger.info("Senior candidate detected, sending Slack notification...")
        slack_success, slack_msg = send_slack_notification(analysis_result)
    
    return {
        "status": "success",
        "data": analysis_result,
        "sheets_sync": {
            "success": sheets_success,
            "message": sheets_msg
        },
        "slack_notification": {
            "triggered": classification == "senior",
            "success": slack_success,
            "message": slack_msg
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
