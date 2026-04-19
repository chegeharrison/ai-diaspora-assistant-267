from django.conf import settings
import json
import requests
import logging
logger = logging.getLogger(__name__)

VALID_INTENTS = {
    "send_money",
    "get_airport_transfer",
    "hire_service",
    "verify_document",
    "check_status",
}

INTENT_ALIASES = {
    "schedule_service": "hire_service",
    "airport_pickup": "get_airport_transfer",
    "airport_transfer": "get_airport_transfer",
    "money_transfer": "send_money",
    "status_check": "check_status",
    "document_verification": "verify_document",
}

ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        "intent": {"type": "string"},
        "entities": {
            "type": "object",
            "properties": {
                "amount": {"type": "string"},
                "recipient": {"type": "string"},
                "location": {"type": "string"},
                "urgency": {"type": "string"},
                "document_type": {"type": "string"},
                "service_type": {"type": "string"},
                "schedule": {"type": "string"},
                "task_code": {"type": "string"},
            },
            "required": [
                "amount",
                "recipient",
                "location",
                "urgency",
                "document_type",
                "service_type",
                "schedule",
                "task_code",
            ],
            "additionalProperties": False,
        },
        "steps": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 3,
        },
    },
    "required": ["intent", "entities", "steps"],
    "additionalProperties": False,
}

MESSAGE_SCHEMA = {
    "type": "object",
    "properties": {
        "whatsapp": {"type": "string"},
        "email": {"type": "string"},
        "sms": {"type": "string"},
    },
    "required": ["whatsapp", "email", "sms"],
    "additionalProperties": False,
}

ANALYSIS_SYSTEM_PROMPT = """
You are an AI operations assistant for a diaspora support platform serving Kenyans living abroad.

Classify the request into ONE valid intent only:
- send_money
- get_airport_transfer
- hire_service
- verify_document
- check_status

Rules:
- send_money = sending money, amounts, recipients, bills, emergency support
- get_airport_transfer = airport pickup, drop-off, JKIA pickup, landing time
- hire_service = cleaners, lawyers, errand runners, local service providers
- verify_document = land titles, title deeds, IDs, certificates, agreements
- check_status = asking for the status of an existing task code

Return:
- one valid intent only
- entities
- at least 3 specific steps
- no fake intents
- no placeholder steps like "step 1"

Return strict JSON only.
"""

MESSAGE_SYSTEM_PROMPT = """
You are an AI customer communications assistant for Vunoh Global.

Generate 3 customer messages for a diaspora support task:
- whatsapp: conversational, concise, natural
- email: formal, structured, includes task code and useful details
- sms: under 160 characters, includes task code

Brand rules:
- Always write the company name exactly as: Vunoh Global
- Do not write VunoH, VUNOH, or any other variation

Email rules:
- Email must begin with "Dear Customer,"
- Never address the email to Vunoh Global or Vunoh Global Team

Rules:
- All 3 messages must be non-empty
- Do not invent phone numbers, email addresses, tracking links, or timelines
- Do not claim a task is completed unless the system explicitly says so
- Do not say "I will transfer" or act like the assistant personally executes the task
- Use wording like "we have received your request", "your request is being processed", or "current status"
- If intent is check_status, use only the exact status provided
- Return strict JSON only
"""

def _call_groq_json(system_prompt: str, user_prompt: str, schema: dict) -> dict:
    api_key = settings.LLM_API_KEY.strip()
    api_url = settings.LLM_API_URL.strip()
    model = settings.LLM_MODEL.strip()

    if not api_key or not api_url or not model:
        raise RuntimeError("Missing LLM configuration in Django settings")

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "diaspora_output",
                "strict": True,
                "schema": schema,
            },
        },
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=45)
        response.raise_for_status()

        data = response.json()
        content = data["choices"][0]["message"]["content"]
        return json.loads(content)

    except requests.exceptions.HTTPError:
        logger.exception("Groq HTTP error. Status=%s Body=%s", response.status_code, response.text[:2000])
        raise RuntimeError("Groq API returned an HTTP error")

    except Exception:
        logger.exception("Groq request or JSON parsing failed")
        raise

def normalize_intent(intent: str) -> str:
    cleaned = (intent or "").strip().lower()
    if cleaned in VALID_INTENTS:
        return cleaned
    return INTENT_ALIASES.get(cleaned, cleaned)

def clean_steps(steps: list[str]) -> list[str]:
    good_steps = []

    for step in steps:
        text = (step or "").strip()
        lower = text.lower()

        if not text:
            continue
        if lower in {"step 1", "step 2", "step 3"}:
            continue
        if lower.startswith("step ") and len(text) <= 10:
            continue

        good_steps.append(text)

    return good_steps

def normalize_blank(value):
    if value is None:
        return ""
    text = str(value).strip()
    if text.lower() in {"n/a", "na", "none", "null", "not provided"}:
        return ""
    return text


def validate_analysis_result(data: dict) -> dict:
    intent = normalize_intent(data.get("intent", ""))

    if intent not in VALID_INTENTS:
        raise ValueError(f"Invalid intent returned by AI: {intent}")

    entities = data.get("entities", {}) or {}
    normalized_entities = {
        "amount": normalize_blank(entities.get("amount", "")),
        "recipient": normalize_blank(entities.get("recipient", "")),
        "location": normalize_blank(entities.get("location", "")),
        "urgency": normalize_blank(entities.get("urgency", "")),
        "document_type": normalize_blank(entities.get("document_type", "")),
        "service_type": normalize_blank(entities.get("service_type", "")),
        "schedule": normalize_blank(entities.get("schedule", "")),
        "task_code": normalize_blank(entities.get("task_code", "")),
    }

    steps = clean_steps(data.get("steps", []))
    if len(steps) < 3:
        raise ValueError("AI returned fewer than 3 valid steps")

    return {
        "intent": intent,
        "entities": normalized_entities,
        "steps": steps,
    }

def normalize_brand_name(text: str) -> str:
    replacements = {
        "VunoH Global": "Vunoh Global",
        "VUNOH Global": "Vunoh Global",
        "VUNOH GLOBAL": "Vunoh Global",
        "VunoH": "Vunoh",
    }

    cleaned = text
    for wrong, correct in replacements.items():
        cleaned = cleaned.replace(wrong, correct)

    return cleaned

def validate_messages(data: dict) -> dict:
    whatsapp = normalize_brand_name((data.get("whatsapp", "") or "").strip())
    email = normalize_brand_name((data.get("email", "") or "").strip())
    sms = normalize_brand_name((data.get("sms", "") or "").strip())

    if not whatsapp:
        raise ValueError("WhatsApp message is empty")
    if not email:
        raise ValueError("Email message is empty")
    if not sms:
        raise ValueError("SMS message is empty")
    if len(sms) > 160:
        raise ValueError("SMS exceeds 160 characters")

    banned_phrases = [
        "call 1-800",
        "@company.com",
        "tracking link",
    ]

    combined = f"{whatsapp} {email} {sms}".lower()
    for phrase in banned_phrases:
        if phrase in combined:
            raise ValueError("Generated message contains invented contact details or unsupported claims")

    return {
        "whatsapp": whatsapp,
        "email": email,
        "sms": sms,
    }

def analyze_customer_request(user_text: str) -> dict:
    prompt = f"""
Analyze this request and return structured task data.

Customer request:
{user_text}
"""

    raw = _call_groq_json(ANALYSIS_SYSTEM_PROMPT, prompt, ANALYSIS_SCHEMA)
    return validate_analysis_result(raw)

def generate_task_messages(
    raw_request: str,
    task_code: str,
    intent: str,
    entities: dict,
    risk_score: int,
    employee_assignment: str,
    actual_status: str = "",
    referenced_task_code: str = "",
) -> dict:
    if intent == "check_status":
        code = referenced_task_code or "Unknown"
        status_text = actual_status or "Unknown"

        return {
            "whatsapp": f"Hi! Task {code} is currently {status_text}. We’ll notify you when the status changes.",
            "email": (
                f"Dear Customer,\n\n"
                f"Thank you for checking the status of task {code}.\n"
                f"Current status: {status_text}.\n\n"
                f"We will notify you if there are any changes.\n\n"
                f"Best regards,\n"
                f"Vunoh Global Customer Support"
            ),
            "sms": f"Task {code} status: {status_text}."
        }

    prompt = f"""
Generate 3 customer messages for this saved task.

Task code: {task_code}
Intent: {intent}
Entities: {json.dumps(entities)}
Risk score: {risk_score}
Assigned team: {employee_assignment}
Original request: {raw_request}
Referenced task code: {referenced_task_code}
Actual referenced task status: {actual_status}
"""

    raw = _call_groq_json(MESSAGE_SYSTEM_PROMPT, prompt, MESSAGE_SCHEMA)
    return validate_messages(raw)