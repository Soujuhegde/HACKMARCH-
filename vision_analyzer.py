"""
VISION ANALYZER — AI Facial Health Analysis
Uses Google Gemini 2.0 Flash to detect visible health indicators from images.
"""

import json
import urllib.request
import urllib.error
import base64
from recommendation_engine import GEMINI_URL

VISION_PROMPT = """You are a focused Medical Computer Vision AI. 
Analyze STRICTLY the facial features in this image. Do not consider any other data.

Output exactly 3 indicators in JSON:
1. skin: "Good", "Moderate", or "Poor" (Focus on visible hydration/texture)
2. eyes: "Clear", "Redness", or "Yellowing" (Focus on the sclera/conjunctiva)
3. fatigue: "Low", "Medium", or "High" (Focus on dark circles/orbital area)

Output ONLY valid JSON:
{"skin": "...", "eyes": "...", "fatigue": "...", "summary": "brief visible facial insight", "confidence": 0.9}
"""

def analyze_face_image(image_bytes: bytes, mime_type: str = "image/jpeg") -> dict:
    """
    Takes raw image bytes, sends to Gemini Vision, returns structured indicators.
    Includes a fallback if the API is rate-limited (429).
    """
    img_b64 = base64.b64encode(image_bytes).decode('utf-8')
    
    payload = {
        "contents": [{
            "parts": [
                {"text": VISION_PROMPT},
                {"inline_data": {
                    "mime_type": mime_type,
                    "data": img_b64
                }}
            ]
        }],
        "generationConfig": {
            "temperature": 0.1,
            "response_mime_type": "application/json"
        }
    }
    
    req = urllib.request.Request(
        GEMINI_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            candidates = result.get("candidates", [])
            if candidates:
                text_response = candidates[0]["content"]["parts"][0]["text"]
                return json.loads(text_response)
            return get_vision_fallback("No response from AI")
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return get_vision_fallback("API Rate Limit Reached (429). Providing standard indicators.")
        return get_vision_fallback(f"HTTP Error {e.code}")
    except Exception as e:
        return get_vision_fallback(str(e))

def get_vision_fallback(reason: str):
    """Fallback if API fails"""
    return {
        "skin": "Moderate",
        "eyes": "Clear",
        "fatigue": "Low",
        "summary": "Standard analysis based on baseline facial traits.",
        "confidence": 0.5,
        "is_fallback": True,
        "reason": reason
    }
