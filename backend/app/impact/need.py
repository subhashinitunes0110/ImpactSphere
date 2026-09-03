import os
import pandas as pd
from typing import Dict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.normpath(os.path.join(BASE_DIR, "../../../data/need_indicators.csv"))

def load_need_db() -> Dict[str, Dict[str, float]]:
    if not os.path.exists(DATA_PATH):
        return {}
    df = pd.read_csv(DATA_PATH)
    database = {}
    for _, row in df.iterrows():
        database[row["district"]] = {
            "healthcare": float(row["healthcare"]),
            "education": float(row["education"]),
            "water": float(row["water"]),
            "livelihood": float(row["livelihood"]),
            "infrastructure": float(row["infrastructure"]),
            "existing_coverage": float(row["existing_coverage"]),
        }
    return database

NEED_DB = load_need_db()

def calculate_need_metrics(district: str, sector: str) -> Dict[str, float]:
    data = NEED_DB.get(district, {
        "healthcare": 50.0, "education": 50.0, "water": 50.0,
        "livelihood": 50.0, "infrastructure": 50.0, "existing_coverage": 50.0
    })
    
    composite_need = (
        data["healthcare"] * 0.25 +
        data["education"] * 0.20 +
        data["water"] * 0.20 +
        data["livelihood"] * 0.20 +
        data["infrastructure"] * 0.15
    )
    
    sector_key = sector.lower()
    sector_val = data.get(sector_key, composite_need)
    final_need = (sector_val * 0.60) + (composite_need * 0.40)
    
    coverage = data["existing_coverage"]
    unmet_need = final_need * (1.0 - (coverage / 100.0))
    
    return {
        "need_score": round(final_need, 2),
        "unmet_need_score": round(unmet_need, 2),
        "geographic_score": round(unmet_need, 2)
    }