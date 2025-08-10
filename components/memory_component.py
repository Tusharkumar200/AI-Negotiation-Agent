# components/memory_component.py

from typing import Any, Dict, List

# Define a minimal ContextComponent base class
class ContextComponent:
    def __init__(self):
        pass


class BuyerMemoryComponent(ContextComponent):
    """
    Memory component to store negotiation history.
    Compatible with Concordia's ContextComponent interface.
    """

    def __init__(self):
        super().__init__()
        self.history: List[Dict[str, Any]] = []
        self.rounds = 0
        self.last_offer = None

    def record_round(self, round_data: Dict[str, Any]) -> None:
        """Record each negotiation round details."""
        self.history.append(round_data)
        self.rounds += 1
        if round_data.get("buyer_offer") is not None:
            self.last_offer = round_data["buyer_offer"]

    def make_pre_act_value(self) -> str:
        """Return a short summary string for LLM context."""
        if not self.history:
            return "No prior negotiation history."
        # Limit to last 3 rounds for brevity
        recent = self.history[-3:]
        summary = []
        for r in recent:
            summary.append(
                f"Round {r.get('round', '?')}: "
                f"Seller asked ₹{r.get('seller_price', '?')} | "
                f"Buyer {r.get('buyer_action', '')} ₹{r.get('buyer_offer', '')}"
            )
        return "\n".join(summary)

    def get_state(self) -> Dict[str, Any]:
        """Save state."""
        return {
            "history": self.history,
            "rounds": self.rounds,
            "last_offer": self.last_offer
        }

    def set_state(self, state: Dict[str, Any]) -> None:
        """Restore state."""
        self.history = state.get("history", [])
        self.rounds = state.get("rounds", len(self.history))
        self.last_offer = state.get("last_offer", None)
