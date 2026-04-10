import json

from google import genai
from google.genai import types

from app.config import GEMINI_API_KEY

# NOTE: max_output_tokens raised from 1024 → 8192 so the full analysis fits.
# gemini-2.0-flash-lite is the cheapest available model; swap for
# "gemini-2.5-flash-lite" once it is generally available.
_MODEL = "gemini-2.5-flash-lite"

_CONFIG = types.GenerateContentConfig(
    temperature=0.2,
    top_p=0.95,
    top_k=40,
    max_output_tokens=8192,
    response_mime_type="application/json",
)

_client = genai.Client(api_key=GEMINI_API_KEY)

ANALYSIS_PROMPT = """You are an expert legal analyst helping everyday users understand contracts and user agreements.
Analyze the document below from the CLIENT / USER perspective and return ONLY a single valid JSON object with this schema:

{{
  "summary": "<plain-language overview, 2-3 paragraphs, no legalese>",
  "red_flags": [
    {{
      "title": "<short label>",
      "description": "<why this harms / disadvantages the user>",
      "severity": "high|medium|low"
    }}
  ],
  "similar_cases": [
    {{
      "type": "court_settlement|similar_agreement|ignored_clause|helpful_info",
      "title": "<case or reference name>",
      "description": "<what happened>",
      "relevance": "<how it relates to a clause in this document>"
    }}
  ]
}}

type values:
- court_settlement  → real legal case / settlement involving a similar clause
- similar_agreement → another company's ToS that was revised after user backlash or legal challenge
- ignored_clause    → clause that looked scary but courts/regulators have routinely declined to enforce
- helpful_info      → any other context useful to the user (consumer protection laws, regulatory guidance, etc.)

Focus especially on:
• Broad data collection / sharing rights
• Unilateral modification without notice
• Mandatory arbitration and class-action waivers
• Auto-renewal and difficult cancellation
• Unexpected IP assignment
• Disproportionate limitation of liability

CONTRACT / AGREEMENT TEXT:
{contract_text}
"""


async def analyze_contract(text: str) -> dict:
    prompt = ANALYSIS_PROMPT.format(contract_text=text[:50_000])

    # Use the native async client so we don't block the event loop
    response = await _client.aio.models.generate_content(
        model=_MODEL,
        contents=prompt,
        config=_CONFIG,
    )

    raw = response.text.strip()

    # Strip accidental markdown fences
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: return a safe structure with the raw text
        return {
            "summary": raw[:2000],
            "red_flags": [],
            "similar_cases": [],
        }
