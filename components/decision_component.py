# components/decision_component.py
from typing import Dict, Any

class DecisionComponent:
    """
    Decides the buyer's action (OFFER / ACCEPT / REJECT) based on
    market price, budget, round number, and personality.
    """

    def __init__(self, personality_cfg: Dict[str, Any]):
        self.personality_cfg = personality_cfg
        self.last_offer = None

    def compute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Safe fallback — if no market price, use budget
        market_price = context.get("market") or context["budget"]

        budget = context["budget"]
        seller_price = context["seller_price"]
        round_num = context["round"]
        last_offer = context["last_offer"]

        archetype = self.personality_cfg.get("archetype", "Diplomatic-Analytical")

        # --- Opening offer percentage based on personality ---
        if archetype.lower().startswith("aggressive"):
            opening_ratio = 0.65
        elif archetype.lower().startswith("diplomatic"):
            opening_ratio = 0.80
        elif archetype.lower().startswith("data"):
            opening_ratio = 0.75
        else:
            opening_ratio = 0.78  # default safe value

        # --- Decide on action ---
        if seller_price and seller_price <= budget * 0.88:
            return {"action": "ACCEPT", "offer": seller_price}

        if round_num == 1 or last_offer is None:
            offer = int(market_price * opening_ratio)
        else:
            gap = seller_price - last_offer
            concession = max(1, int(gap * (0.5 if round_num < 5 else 0.3)))
            offer = last_offer + concession

        offer = min(offer, budget)

        if round_num >= 9 and seller_price <= budget:
            return {"action": "ACCEPT", "offer": seller_price}

        return {"action": "OFFER", "offer": offer}
