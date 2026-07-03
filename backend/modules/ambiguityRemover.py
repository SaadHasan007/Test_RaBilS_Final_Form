import os
import re
import json
from groq import Groq


def build_llm_prompt(report):

    user_story = report["user_story"]
    notes = report["notes"]

    notes_text = "\n".join(f"- {n}" for n in notes)

    prompt = f"""
You are an expert requirements analyst specializing in agile user stories.

Your job is to rewrite the given user story to remove ambiguity based on the provided user story analysis report.

----------------------------------------
ORIGINAL USER STORY:
{user_story}

----------------------------------------
AMBIGUITY ISSUES IDENTIFIED: (analysis report)
{notes_text}

----------------------------------------
INSTRUCTIONS:

1. Rewrite the user story to eliminate ALL listed ambiguity issues.
2. Preserve the original intent and functionality.
3. Use clear, precise, and measurable language.
4. Do NOT add unrelated features or assumptions.
5. Keep the rewritten story concise and professional.
6. Return ONLY valid JSON.
7. Do NOT include markdown code fences.

----------------------------------------
REQUIRED OUTPUT FORMAT:
{{
    "processed_story": "As a <specific role>, I want <specific goal>, so that <clear benefit>.",
    "ambiguity_notes": [
        "Explanation of ambiguity fix 1",
        "Explanation of ambiguity fix 2"
    ]
}}
""" 
    return prompt

# # ─────────────────────────────────────────────────────────────────────────────
# # Groq-powered ambiguity detection + user story formatter
# # Free tier: 14,400 requests/day, works globally
# # Model: llama-3.3-70b-versatile (very capable, fast)
# # ─────────────────────────────────────────────────────────────────────────────

# SYSTEM_PROMPT = """You are an expert requirements analyst specializing in agile user stories.
# Your job is to:
# 1. Detect ALL ambiguous, vague, or unclear phrases in the given input.
# 2. Rewrite the input as a properly formatted user story using EXACTLY this format:

# As a <role>,
# I want <some goal>
# So that <benefit>.

# # Rules:
# # - If the input is already a well-formed user story, just clean it up and resolve any vague terms.
# # - If the input is missing a role, infer the most sensible one from context.
# # - If the input is missing a benefit (So that...), infer a reasonable one.
# # - Replace every vague term (e.g., "fast", "easy", "soon", "user-friendly", "seamless", "robust") with a specific, measurable alternative.
# # - Respond ONLY in valid JSON format with no extra text or markdown code fences:

# # {
# #   "formatted_story": "As a <role>\\nI want <some goal>\\nSo that <benefit>",
# #   "ambiguity_notes": [
# #     "Replaced 'fast' with 'within 2 seconds' for measurability.",
# #     "Added missing role: 'registered user'."
# #   ]
# # }"""


def _remove_ambiguity_with_groq(text, ambiguity_report) -> dict:
    """
    Calls the Groq API (LLaMA 3.3 70B) to detect ambiguity and reformat the story.
    """

    SYSTEM_PROMPT = build_llm_prompt({
        "user_story": text, 
        "notes": ambiguity_report
    })

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": text.strip()
             },
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

        if "processed_story" not in result:
            print("⚠ AI response missing 'processed_story' field. Returning original text with a warning note.")
            result["processed_story"] = text

        if "ambiguity_notes" not in result:
            print("⚠ AI response missing 'ambiguity_notes'")
            result["ambiguity_notes"] = []

    except json.JSONDecodeError:
        result = {
            "processed_story": content,
            "ambiguity_notes": ["Could not parse structured notes from AI response."],
        }

    return result


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def remove_ambiguity(text, ambiguity_report) -> dict:
    """
    If GROQ_API_KEY is set → uses LLaMA 3.3 70B (via Groq) to detect ambiguity
                             and reformat into 'As a / I want / So that' format.
    Returns: { "processed_story": str, "ambiguity_notes": [str], "used_ai": bool }
    """
    api_key = os.environ.get("GROQ_API_KEY", "").strip()

    result = {
        "processed_story": text,
        "ambiguity_notes": [],
        "used_ai": False
    } 

    if api_key:
        try:
            result = _remove_ambiguity_with_groq(text, ambiguity_report)
            result["used_ai"] = True
            return result
        except Exception as e:
            return {
                "processed_story": text,
                "ambiguity_notes": [
                    f"⚠ AI check failed ({str(e)})."
                    ],
                "used_ai": False
            }
    else:
        result["ambiguity_notes"].append(
                "⚠ AI check failed.Make sure Grok API key is set. errorCode: arl141"
                )
        return result