import os
import urllib.request
import json
import logging

logger = logging.getLogger(__name__)

def send_slack_notification(candidate_data: dict):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        logger.warning("SLACK_WEBHOOK_URL is not set in .env. Skipping Slack notification.")
        return False, "Webhook URL not configured"
        
    name = candidate_data.get("candidate_name", "Unknown Candidate")
    experience = candidate_data.get("experience_years", 0)
    score = candidate_data.get("suitability_score", 0)
    skills = candidate_data.get("skills", "")
    
    message = {
        "text": f"🎉 *New Senior Candidate Identified!*\n*Name:* {name}\n*Experience:* {experience} years\n*Score:* {score}/100\n*Skills:* {skills}"
    }
    
    data = json.dumps(message).encode("utf-8")
    req = urllib.request.Request(webhook_url, data=data, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                logger.info(f"Successfully sent Slack notification for {name}")
                return True, "Notification sent"
            else:
                logger.error(f"Failed to send Slack notification. Status: {response.status}")
                return False, f"HTTP Status {response.status}"
    except Exception as e:
        logger.error(f"Error sending Slack notification: {e}")
        return False, str(e)
