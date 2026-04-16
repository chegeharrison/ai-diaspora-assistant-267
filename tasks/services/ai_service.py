from django.conf import settings
import json
import requests


def analyze_customer_request(user_text: str) -> dict:
    api_key = settings.LLM_API_KEY.strip()
    api_url = settings.LLM_API_URL.strip()
    model = settings.LLM_MODEL.strip()

    if not api_key or not api_url or not model:
        raise RuntimeError("Missing LLM configuration in Django settings")

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": """Return strict JSON only in this format:
{
  "intent": "verify_document",
  "entities": {
    "amount": "",
    "recipient": "",
    "location": "",
    "urgency": "",
    "document_type": "",
    "service_type": "",
    "schedule": "",
    "task_code": ""
  },
  "steps": ["step 1", "step 2"],
  "messages": {
    "whatsapp": "",
    "email": "",
    "sms": ""
  }
}"""
            },
            {
                "role": "user",
                "content": user_text
            }
        ],
        "temperature": 0,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(api_url, headers=headers, json=payload, timeout=45)
    response.raise_for_status()

    data = response.json()
    content = data["choices"][0]["message"]["content"]

    return json.loads(content)