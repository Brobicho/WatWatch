import json
import re
import unicodedata
from openai import OpenAI


def normalize_title(title):
    """Normalize title for comparison (remove accents, lowercase, alphanum only)."""
    if not title:
        return ""
    
    # Remove everything in parentheses (years, versions, etc.)
    title = re.sub(r'\([^)]*\)', '', title)
    
    # Remove common version/sequel markers
    title = re.sub(r'\b(version|v\.|vol\.|volume|part|partie|saison|season|s\d+|épisode|episode|ep\.?)\b', '', title, flags=re.IGNORECASE)
    
    title = unicodedata.normalize("NFKD", title)
    title = title.encode("ascii", "ignore").decode("ascii")
    title = title.lower().strip()
    # Remove all non-alphanumeric characters and collapse spaces
    title = re.sub(r"[^a-z0-9]+", "", title)
    return title


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
Tu es un moteur de recommandation basé sur les goûts d'un utilisateur SensCritique.

Voici une liste d'œuvres que j'ai DÉJÀ vues/écoutées/lues :

{library_txt}

Et voici la même liste de titres au format JSON (NE JAMAIS LES RECOMMANDER) :
{seen_titles_json}

Je veux EXACTEMENT {n_suggestions} suggestions parmi les catégories SUIVANTES UNIQUEMENT :
{allowed_txt}

CONTRAINTES STRICTES :
- Renvoie toujours le titre français officiel de l'œuvre (tel que sur SensCritique)
- Le champ "category" DOIT être exactement une des valeurs suivantes : {allowed_txt}
- Ne recommande JAMAIS une œuvre dont le titre figure exactement dans la liste JSON ci-dessus.
- Si tu n'es pas sûr d'une catégorie, choisis la plus proche dans cette liste et reste cohérent.
- Si tu n'arrives pas à trouver assez d'œuvres qui respectent ces contraintes, propose-en moins, mais ne casse pas le JSON.
- IMPORTANT - CONTRAINTES D'ÉPOQUE :
  * Maximum 10% d'œuvres sorties avant 1980
  * Maximum 20% d'œuvres sorties avant 2000
  * Privilégie les œuvres récentes (2000+) pour au moins 80% des suggestions

FORMAT DE RÉPONSE (JSON STRICT, PAS DE TEXTE AUTOUR) :
{{
  "suggestions": [
    {{
      "title": "Titre de l'œuvre",
      "category": "Une valeur parmi : {allowed_txt}",
      "year": 2024,
      "reason": "Pourquoi cette recommandation est pertinente pour moi",
      "score": 0-100
    }}
  ]
}}

À PROPOS DES SCORES :
- Utilise réellement toute l'échelle 0-100.
- Certaines suggestions doivent être très fortes (>= 90).
- D'autres moyennes (~60-80).
- Au moins une sous 50 (pari/découverte).

Réponds STRICTEMENT avec du JSON valide, sans ``` ni explications autour.
"""


def build_retry_prompt(collection, n_needed, allowed_categories, duplicates, already_suggested):
    """Build a retry prompt when duplicates were filtered."""
    allowed_txt = ", ".join(allowed_categories)
    
    library_txt = "\n".join(
        f"- {x['title']} (cat={x['category']}, rating={x['rating_sc']})"
        for x in collection[:500]
    )
    
    seen_titles = [x["title"] for x in collection[:1000]]
    seen_titles_json = json.dumps(seen_titles, ensure_ascii=False, indent=2)
    
    duplicates_txt = ", ".join(duplicates)
    already_suggested_titles = [s["title"] for s in already_suggested]
    already_suggested_txt = ", ".join(already_suggested_titles)
    
    return f"""
Tu es un moteur de recommandation basé sur les goûts d'un utilisateur SensCritique.

Voici une liste d'œuvres que j'ai DÉJÀ vues/écoutées/lues :

{library_txt}

Liste complète des titres déjà vus (NE JAMAIS LES RECOMMANDER) :
{seen_titles_json}

ATTENTION : Tu as déjà suggéré ces œuvres qui étaient des DOUBLONS (déjà vues) :
{duplicates_txt}

Tu as aussi déjà suggéré ces œuvres VALIDES (ne les re-suggère pas) :
{already_suggested_txt}

Je veux maintenant EXACTEMENT {n_needed} NOUVELLES suggestions (différentes de celles ci-dessus) parmi les catégories SUIVANTES UNIQUEMENT :
{allowed_txt}

CONTRAINTES STRICTES :
- Renvoie toujours le titre français officiel de l'œuvre (tel que sur SensCritique)
- Le champ "category" DOIT être exactement une des valeurs suivantes : {allowed_txt}
- Ne recommande JAMAIS une œuvre dont le titre figure dans la liste JSON ci-dessus
- Ne recommande PAS les doublons que tu as déjà suggérés
- Ne recommande PAS les suggestions valides déjà faites
- Propose des œuvres COMPLÈTEMENT DIFFÉRENTES
- IMPORTANT - CONTRAINTES D'ÉPOQUE :
  * Maximum 10% d'œuvres sorties avant 1980
  * Maximum 20% d'œuvres sorties avant 2000
  * Privilégie les œuvres récentes (2000+) pour au moins 80% des suggestions

FORMAT DE RÉPONSE (JSON STRICT, PAS DE TEXTE AUTOUR) :
{{
  "suggestions": [
    {{
      "title": "Titre de l'œuvre",
      "category": "Une valeur parmi : {allowed_txt}",
      "year": 2024,
      "reason": "Pourquoi cette recommandation est pertinente pour moi",
      "score": 0-100
    }}
  ]
}}

À PROPOS DES SCORES :
- Utilise réellement toute l'échelle 0-100.
- Certaines suggestions doivent être très fortes (>= 90).
- D'autres moyennes (~60-80).
- Au moins une sous 50 (pari/découverte).

Réponds STRICTEMENT avec du JSON valide, sans ``` ni explications autour.
"""


def get_recommendations(collection, n_suggestions, categories, model):
    """Generate recommendations using OpenAI."""
    client = OpenAI()
    max_attempts = 10
    all_suggestions = []
    filtered_duplicates = []
    
    # Build sets once for performance
    existing_titles = {normalize_title(x["title"]) for x in collection}
    allowed_set = {c.lower() for c in categories} if categories else set()
    
    attempt = 0
    while len(all_suggestions) < n_suggestions and attempt < max_attempts:
        # Adjust prompt based on attempt
        if attempt == 0:
            prompt = build_prompt(collection, n_suggestions, categories)
        else:
            remaining_needed = n_suggestions - len(all_suggestions)
            prompt = build_retry_prompt(
                collection, 
                remaining_needed, 
                categories, 
                filtered_duplicates,
                all_suggestions
            )
        
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
            print(f"Tentative {attempt + 1}: AI response not parseable")
            print("JSON error:", e)
            attempt += 1
            continue

        suggestions = data.get("suggestions", [])
        already_suggested = {normalize_title(s["title"]) for s in all_suggestions}

        new_duplicates = []
        added_this_round = 0
        
        for s in suggestions:
            title = s.get("title")
            category = s.get("category")
            reason = s.get("reason", "")
            score = s.get("score", 0)
            year = s.get("year")

            if not title or not category:
                continue

            norm_title = normalize_title(title)
            
            # Empty after normalization = invalid
            if not norm_title:
                continue
            
            cat_clean = category.strip().lower()

            # Check if duplicate from collection (strict)
            if norm_title in existing_titles:
                new_duplicates.append(title)
                continue
            
            # Check if already suggested in previous attempts (strict)
            if norm_title in already_suggested:
                new_duplicates.append(title)
                continue
            
            # Additional check: detect sequels, prequels, remakes, versions
            # If normalized title is a strict prefix or starts the same way
            is_too_similar = False
            for existing_norm in existing_titles:
                if not norm_title or not existing_norm:
                    continue
                    
                # If one is a substring of the other
                if norm_title in existing_norm or existing_norm in norm_title:
                    is_too_similar = True
                    break
                
                # Check if they share a long common prefix (possible sequel/prequel)
                min_len = min(len(norm_title), len(existing_norm))
                if min_len >= 5:
                    common_prefix_len = 0
                    for i in range(min_len):
                        if norm_title[i] == existing_norm[i]:
                            common_prefix_len += 1
                        else:
                            break
                    # If 80%+ of the shorter title matches, it's too similar
                    if common_prefix_len / min_len >= 0.8:
                        is_too_similar = True
                        break
            
            if is_too_similar:
                new_duplicates.append(title)
                continue

            if allowed_set and cat_clean not in allowed_set:
                continue

            try:
                score = float(score)
            except (ValueError, TypeError):
                score = 0.0
            
            # Validate and convert year
            try:
                year = int(year) if year else None
            except (ValueError, TypeError):
                year = None

            all_suggestions.append({
                "title": title,
                "category": category,
                "reason": reason,
                "score": score,
                "year": year,
            })
            already_suggested.add(norm_title)
            added_this_round += 1
        
        # Track duplicates for next attempt
        if new_duplicates:
            filtered_duplicates.extend(new_duplicates)
            print(f"Tentative {attempt + 1}: {len(new_duplicates)} doublons filtrés, {added_this_round} ajoutés ({len(all_suggestions)}/{n_suggestions})")
        else:
            print(f"Tentative {attempt + 1}: {added_this_round} ajoutés ({len(all_suggestions)}/{n_suggestions})")
        
        attempt += 1
    
    if len(all_suggestions) < n_suggestions:
        print(f"ATTENTION: Seulement {len(all_suggestions)}/{n_suggestions} suggestions uniques trouvées après {attempt} tentatives")
    
    return all_suggestions[:n_suggestions]
