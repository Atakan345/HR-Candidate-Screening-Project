import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def evaluate_candidate(cv_text: str) -> dict:
    # Check for Gemini key in different cases
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("Gemini_API_Key")
    
    if not gemini_key:
        return {
            "candidate_name": "No Name (API key missing)",
            "experience_years": 0,
            "skills": "",
            "suitability_score": 0,
            "classification": "Not Suitable",
            "analysis": "Lütfen .env dosyasına Gemini_API_Key değerini girin."
        }
    
    genai.configure(api_key=gemini_key)
    
    prompt = f"""You are an expert HR recruiter. Please analyze the following CV and extract details.
Return ONLY a valid JSON object with the following exactly keys (do not add any markdown, just output JSON):
- "candidate_name" (string, full candidate name)
- "experience_years" (integer, total number of years or 0)
- "skills" (string, comma separated)
- "suitability_score" (integer from 1-100)
- "classification" (string, exact value from: "Junior", "Mid-level", "Senior", "Not Suitable")
- "analysis" (string, short 1-2 sentence explanation of suitability based on the profile)

Here is the CV text:
{cv_text}
"""
    try:
        # Check accessible models to avoid 404 Not Found error
        avail_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model = next((m for m in avail_models if 'flash' in m or 'pro' in m), avail_models[0] if avail_models else 'gemini-pro')
        
        model = genai.GenerativeModel(target_model)
        response = model.generate_content(prompt)
        content = response.text.strip()
        
        # Strip potential markdown formatting from Gemini's output
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
            
        return json.loads(content)
    except Exception as e:
        return {
            "candidate_name": "Extraction Error",
            "experience_years": 0,
            "skills": "",
            "suitability_score": 0,
            "classification": "Not Suitable",
            "analysis": f"AI extraction failed: {str(e)}"
        }
