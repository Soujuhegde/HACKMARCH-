import json
import urllib.request
import urllib.error
import base64
import io
from PIL import Image

# Using 1.5-flash for vision as it is more stable and has higher rate limits
VISION_API_KEY = "GEMINI_API_KEY" # Placeholder, will be injected from env
VISION_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key="

VISION_PROMPT = """You are a focused Medical Computer Vision AI. 
Analyze STRICTLY the facial features in this image. Focus especially on skin health.

Output EXACTLY 4 indicators in JSON:
1. skin: "Good", "Moderate", or "Poor"
2. skin_details: Detailed feedback on skin (acne, texture, hydration, glow)
3. eyes: "Clear", "Redness", or "Yellowing"
4. fatigue: "Low", "Medium", or "High"

Output ONLY valid JSON:
{
  "skin": "...", 
  "skin_details": "short professional observation about skin texture or hydration",
  "eyes": "...", 
  "fatigue": "...", 
  "summary": "brief overall visible facial insight", 
  "confidence": 0.9
}
"""

def analyze_face_image(image_bytes: bytes, api_key: str) -> dict:
    """
    Compresses image, sends to Gemini 1.5 Flash Vision, returns structured indicators.
    """
    try:
        # Resize/Compress to reduce payload and avoid 429
        img = Image.open(io.BytesIO(image_bytes))
        img.thumbnail((400, 400)) # Smaller is better for 429
        
        # Convert back to bytes (RGB JPEG)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=75)
        compressed_bytes = buffer.getvalue()
        
        img_b64 = base64.b64encode(compressed_bytes).decode('utf-8')
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": VISION_PROMPT},
                    {"inline_data": {
                        "mime_type": "image/jpeg",
                        "data": img_b64
                    }}
                ]
            }],
            "generationConfig": {
                "temperature": 0.1,
                "response_mime_type": "application/json"
            }
        }
        
        url = VISION_URL + api_key
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            candidates = result.get("candidates", [])
            if candidates:
                text_response = candidates[0]["content"]["parts"][0]["text"]
                return json.loads(text_response)
            return get_vision_fallback("No response from AI")
            
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return get_vision_fallback("The AI is currently busy with many scans. Using a standard baseline for now.")
        return get_vision_fallback(f"HTTP Error {e.code}")
    except Exception as e:
        return get_vision_fallback(f"Scanner Logic Error: {str(e)}")

def get_vision_fallback(reason: str):
    """Fallback if API fails"""
    return {
        "skin": "Moderate",
        "skin_details": "Consistent tone with mild signs of environmental fatigue.",
        "eyes": "Clear",
        "fatigue": "Low",
        "summary": "Baseline analysis based on available visual traits.",
        "confidence": 0.5,
        "is_fallback": True,
        "reason": reason
    }
