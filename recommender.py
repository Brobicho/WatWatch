import json
import re
import unicodedata
from openai import OpenAI


def normalize_title(title):
    """Normalize title for comparison (remove accents, lowercase, alphanum only)."""
    if not title:
        return ""
    
    title = unicodedata.normalize("NFKD", title)
    title = title.encode("ascii", "ignore").decode("ascii")
    title = title.lower().strip()
    title = re.sub(r"[^a-z0-9]+", " ", title)
    return title.strip()


def build_prompt(collection, n_suggestions, allowed_categories):
    """Build the OpenAI prompt for recommendations."""
    allowed_txt = ", ".join(allowed_categories)

    library_txt = "\n".join(
        f"- {x['title']} (cat={x['category']}, rating={x['rating_sc']})"
        for x in collection[:500]
    )

    seen_titles = [x["title"] for x in collection[:1000]]
    seen_titles_json = json.dumps(seen_titles, ensure_ascii=False, indent=2)

    return f"""
You are a recommendation engine based on a SensCritique user's tastes.

Here is a list of works I have ALREADY seen/listened to/read:

{library_txt}

And here is the same list of titles in JSON format (NEVER RECOMMEND THESE):
{seen_titles_json}

I want EXACTLY {n_suggestions} suggestions from the FOLLOWING categories ONLY:
{allowed_txt}

STRICT CONSTRAINTS:
- The "category" field MUST be exactly one of the following values: {allowed_txt}
- NEVER recommend a work whose title appears exactly in the JSON list above.
- If you're unsure about a category, choose the closest one from this list and stay consistent.
- If you can't find enough works that meet these constraints, suggest fewer, but don't break the JSON.

RESPONSE FORMAT (STRICT JSON, NO TEXT AROUND IT):
{{
  "suggestions": [
    {{
      "title": "Work title",
      "category": "One value from: {allowed_txt}",
      "reason": "Why this recommendation is relevant to me",
      "score": 0-100
    }}
  ]
}}

ABOUT SCORES:
- Actually use the full 0-100 scale.
- Some suggestions should be very strong (>= 90).
- Others medium (~60-80).
- At least one below 50 (risky/discovery).

Respond STRICTLY with valid JSON, without ``` or explanations around it.
"""


def get_recommendations(collection, n_suggestions, categories, model):
    """Generate recommendations using OpenAI."""
    client = OpenAI()
    prompt = build_prompt(collection, n_suggestions, categories)

    response = client.responses.create(
        model=model,
        input=prompt,
        store=False,
    )

    raw = response.output_text.strip()

    # Clean markdown code blocks if present
    if raw.startswith("```"):
        lines = raw.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        raw = "\n".join(lines).strip()

    try:
        data = json.loads(raw)
    except Exception as e:
        print("AI response not parseable after cleaning:")
        print(raw)
        print("JSON error:", e)
        return []

    suggestions = data.get("suggestions", [])
    existing_titles = {normalize_title(x["title"]) for x in collection}
    allowed_set = {c.lower() for c in categories} if categories else set()

    clean = []
    for s in suggestions:
        title = s.get("title")
        category = s.get("category")
        reason = s.get("reason", "")
        score = s.get("score", 0)

        if not title or not category:
            continue

        norm_title = normalize_title(title)
        cat_clean = category.strip().lower()

        if norm_title in existing_titles:
            continue

        if allowed_set and cat_clean not in allowed_set:
            continue

        try:
            score = float(score)
        except (ValueError, TypeError):
            score = 0.0

        clean.append({
            "title": title,
            "category": category,
            "reason": reason,
            "score": score,
        })

    return clean
