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

_CHAT_CONFIG = types.GenerateContentConfig(
  temperature=0.2,
  top_p=0.95,
  top_k=40,
  max_output_tokens=2048,
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

CHAT_PROMPT = """You are ContractLens, an assistant that answers user questions about contracts and user agreements.

Use ONLY the provided document excerpts, saved analysis results, and conversation history as your grounding context.
If the answer is not clearly supported by that context, say so directly.
Do not invent legal citations, lawsuits, or facts.
Do not present yourself as a lawyer.

Answer from the user's perspective:
- be plain-language and specific
- point out practical risk
- mention which uploaded document(s) you relied on by filename
- when helpful, suggest what the user should double-check in the original text
- add a brief disclaimer that this is not legal advice only when the question asks for legal recommendations

CONVERSATION HISTORY:
{history}

DOCUMENT CONTEXT:
{document_context}

USER QUESTION:
{question}
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


def _format_history(history: list[dict]) -> str:
    if not history:
        return "No prior conversation."

    lines = []
    for item in history[-8:]:
        role = item.get("role", "user").upper()
        content = (item.get("content") or "").strip()
        if content:
            lines.append(f"{role}: {content}")
    return "\n".join(lines) if lines else "No prior conversation."


def _format_documents(documents: list[dict]) -> str:
    blocks = []
    for index, doc in enumerate(documents, start=1):
        analysis = json.dumps(doc.get("analysis") or {}, ensure_ascii=True)
        document_text = (doc.get("document_text") or doc.get("preview_text") or "")[:12000]
        blocks.append(
            f"DOCUMENT {index}: {doc.get('filename', 'Untitled')}\n"
            f"DOCUMENT_ID: {str(doc.get('_id', ''))}\n"
            f"EXTRACTED_TEXT:\n{document_text}\n\n"
            f"SAVED_ANALYSIS_JSON:\n{analysis}"
        )
    return "\n\n---\n\n".join(blocks) if blocks else "No documents were provided."


async def chat_with_documents(question: str, documents: list[dict], history: list[dict] | None = None) -> str:
    prompt = CHAT_PROMPT.format(
        history=_format_history(history or []),
        document_context=_format_documents(documents),
        question=question.strip(),
    )

    response = await _client.aio.models.generate_content(
        model=_MODEL,
        contents=prompt,
        config=_CHAT_CONFIG,
    )
    return (response.text or "").strip()
