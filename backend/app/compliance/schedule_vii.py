import re
from typing import Dict, List, Optional

def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))

def match_schedule_vii(
    activity_description: str,
    sector: Optional[str] = None
) -> Dict[str, object]:

    text = f"{activity_description} {sector or ''}".lower()

    keyword_groups = {
        "Schedule VII(i)": {
            "health", "healthcare", "hospital", "sanitation",
            "water", "nutrition", "malnutrition", "poverty", "hunger"
        },
        "Schedule VII(ii)": {
            "education", "school", "skill", "vocational",
            "livelihood", "training"
        },
        "Schedule VII(iii)": {
            "women", "gender", "empowerment", "senior",
            "orphan", "inequality"
        },
        "Schedule VII(iv)": {
            "environment", "climate", "forest", "soil",
            "biodiversity", "animal", "sustainability"
        },
        "Schedule VII(v)": {
            "heritage", "culture", "library", "handicraft",
            "art", "museum"
        },
        "Schedule VII(vi)": {
            "veteran", "war", "armed", "forces"
        },
        "Schedule VII(vii)": {
            "sport", "sports", "olympic", "paralympic", "athlete"
        },
        "Schedule VII(viii)": {
            "relief", "pmcares", "welfare", "fund"
        },
        "Schedule VII(ix)": {
            "research", "incubator", "science", "technology",
            "engineering", "medicine", "laboratory"
        },
        "Schedule VII(x)": {
            "rural", "village", "agriculture"
        },
        "Schedule VII(xi)": {
            "slum", "slums"
        },
        "Schedule VII(xii)": {
            "disaster", "flood", "earthquake",
            "rehabilitation", "reconstruction"
        },
    }

    tokens = _tokens(text)

    scores = {
        category: len(tokens & keywords)
        for category, keywords in keyword_groups.items()
    }

    ranked = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    if not ranked or ranked[0][1] == 0:
        return {
            "match": False,
            "category": None,
            "confidence": 0.0,
            "alternatives": []
        }

    best_category, best_score = ranked[0]

    confidence = min(
        0.99,
        0.55 + 0.12 * best_score
    )

    alternatives: List[str] = [
        category
        for category, score in ranked[1:3]
        if score > 0
    ]

    return {
        "match": True,
        "category": best_category,
        "confidence": round(confidence, 2),
        "alternatives": alternatives
    }
