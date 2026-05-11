import os
import re
import json
from groq import Groq



def build_llm_prompt(report):
    user_story = report["user_story"]
    notes = report["notes"]

    notes_text = "\n".join(f"- {n}" for n in notes)

    prompt = f"""
You are an expert in software requirements engineering.

Your task is to rewrite the given user story to remove ambiguity based on the provided analysis report.

----------------------------------------
ORIGINAL USER STORY:
{user_story}

----------------------------------------
AMBIGUITY ISSUES IDENTIFIED:
{notes_text}

----------------------------------------
INSTRUCTIONS:

1. Rewrite the user story to eliminate ALL listed ambiguity issues.
2. Preserve the original intent and functionality.
3. Use clear, precise, and measurable language.
4. Replace vague terms with specific descriptions.
5. Ensure proper format:

"As a <specific user>, I want <specific action>, so that <clear benefit>."

6. Do NOT add new features.

----------------------------------------
OUTPUT:
Only return the improved user story.
"""

    return prompt

# # ─────────────────────────────────────────────────────────────────────────────
# # Groq-powered ambiguity detection + user story formatter
# # Free tier: 14,400 requests/day, works globally
# # Model: llama-3.3-70b-versatile (very capable, fast)
# # ─────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are an expert requirements analyst specializing in agile user stories.
Your job is to:
1. Detect ALL ambiguous, vague, or unclear phrases in the given input.
2. Rewrite the input as a properly formatted user story using EXACTLY this format:

As a <role>,
I want <some goal>
So that <benefit>.

# Rules:
# - If the input is already a well-formed user story, just clean it up and resolve any vague terms.
# - If the input is missing a role, infer the most sensible one from context.
# - If the input is missing a benefit (So that...), infer a reasonable one.
# - Replace every vague term (e.g., "fast", "easy", "soon", "user-friendly", "seamless", "robust") with a specific, measurable alternative.
# - Respond ONLY in valid JSON format with no extra text or markdown code fences:

# {
#   "formatted_story": "As a <role>\\nI want <some goal>\\nSo that <benefit>",
#   "ambiguity_notes": [
#     "Replaced 'fast' with 'within 2 seconds' for measurability.",
#     "Added missing role: 'registered user'."
#   ]
# }"""


def _check_ambiguity_with_groq(text: str) -> dict:
    """
    Calls the Groq API (LLaMA 3.3 70B) to detect ambiguity and reformat the story.
    """
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text.strip()},
        ],
        temperature=0.2,
        max_tokens=600,
    )

    content = response.choices[0].message.content.strip()

    # Strip markdown code fences if model wraps output in ```json ... ```
    if content.startswith("```"):
        content = re.sub(r"^```[a-z]*\n?", "", content)
        content = re.sub(r"\n?```$", "", content)

    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        result = {
            "formatted_story": content,
            "ambiguity_notes": ["Could not parse structured notes from AI response."],
        }

    return result


# ─────────────────────────────────────────────────────────────────────────────
# Fallback: simple regex-based checker (used when GROQ_API_KEY is not set)
# ─────────────────────────────────────────────────────────────────────────────

USER_STORY_PATTERN = re.compile(
    r"^\s*as\s+a\s+.+\n\s*i\s+want\s+.+\n\s*so\s+that\s+.+",
    re.IGNORECASE | re.MULTILINE,
)

VAGUE_TERMS = [
    "fast", "easy", "quickly", "efficiently", "user-friendly",
    "robust", "seamless", "soon", "simple", "better", "nice",
    "improved", "smooth",
]


def _check_ambiguity_fallback(text: str) -> dict:
    notes = []
    for term in VAGUE_TERMS:
        pattern = r'\b' + re.escape(term) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            notes.append(
                f"Vague term detected: '{term}'. Consider a specific, measurable alternative."
            )
    if not USER_STORY_PATTERN.search(text):
        notes.append(
            "Input does not follow the standard format: "
            "'As a <role> / I want <goal> / So that <benefit>'. "
            "Please reformat your story, or set GROQ_API_KEY to auto-format."
        )
    return {"formatted_story": text.strip(), "ambiguity_notes": notes}


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def check_ambiguity(text: str) -> dict:
    """
    If GROQ_API_KEY is set → uses LLaMA 3.3 70B (via Groq) to detect ambiguity
                             and reformat into 'As a / I want / So that' format.
    If not set             → falls back to regex detection.

    Returns: { "formatted_story": str, "ambiguity_notes": [str], "used_ai": bool }
    """
    api_key = os.environ.get("GROQ_API_KEY", "").strip()

    if api_key:
        try:
            result = _check_ambiguity_with_groq(text)
            result["used_ai"] = True
            return result
        except Exception as e:
            result = _check_ambiguity_fallback(text)
            result["ambiguity_notes"].insert(
                0, f"⚠ AI check failed ({str(e)}). Falling back to basic detection."
            )
            result["used_ai"] = False
            return result
    else:
        result = _check_ambiguity_fallback(text)
        result["used_ai"] = False
        return result
