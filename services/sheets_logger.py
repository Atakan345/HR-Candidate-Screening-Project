import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()

def get_sheets_client():
    creds_json = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
    if not os.path.exists(creds_json):
        return None
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scope)
    client = gspread.authorize(creds)
    return client

def save_to_sheets(candidate_data: dict):
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    if not sheet_id:
        return False, "GOOGLE_SHEET_ID not set in .env"
    
    client = get_sheets_client()
    if not client:
        return False, "Google credentials file missing or invalid"
        
    try:
        sheet = client.open_by_key(sheet_id).sheet1
        
        headers = [
            "Candidate Name", 
            "Email",
            "Experience (Years)", 
            "Skills", 
            "Suitability Score", 
            "Classification", 
            "Action",
            "AI Analysis"
        ]
        
        # Check if row 1 has headers, if not, insert them at row 1
        try:
            first_row = sheet.row_values(1)
            if not first_row or first_row[0] != headers[0]:
                sheet.insert_row(headers, index=1)
        except Exception:
            # Fallback if row_values(1) fails for any reason
            sheet.insert_row(headers, index=1)
            
        score = candidate_data.get("suitability_score", 0)
        try:
            score = int(score)
        except (ValueError, TypeError):
            score = 0
            
        if score >= 80:
            action = "interview"
        elif score >= 50:
            action = "screen"
        else:
            action = "reject"
            
        row = [
            candidate_data.get("candidate_name", ""),
            candidate_data.get("email", ""),
            candidate_data.get("experience_years", ""),
            candidate_data.get("skills", ""),
            candidate_data.get("suitability_score", ""),
            candidate_data.get("classification", ""),
            action,
            candidate_data.get("analysis", "")
        ]
        sheet.append_row(row)
        return True, "Saved successfully"
    except Exception as e:
        return False, str(e)
