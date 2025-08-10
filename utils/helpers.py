# utils/helpers.py
import json
import os
from typing import List, Dict, Any

HERE = os.path.dirname(os.path.abspath(__file__))  # this file's directory

def load_product_data(path: str) -> List[Dict[str, Any]]:
    """
    Load product scenarios from given path (data/products.json).
    """
    if not os.path.exists(path):
        # Fallback inline defaults
        return [
            {"name":"Easy Market", "product":{"name":"Alphonso Mangoes","quantity":100,"base_market_price":180000}, "budget":200000, "seller_min":150000},
            {"name":"Tight Budget", "product":{"name":"Kesar Mangoes","quantity":150,"base_market_price":150000}, "budget":140000, "seller_min":125000},
            {"name":"Premium Product", "product":{"name":"Export Mangoes","quantity":50,"base_market_price":200000}, "budget":190000, "seller_min":175000}
        ]
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    # If data format uses "scenarios" key, return that as list of dicts
    if isinstance(data, dict) and "scenarios" in data:
        return data["scenarios"]
    if isinstance(data, list):
        return data
    # otherwise attempt to normalize
    return list(data.values())
