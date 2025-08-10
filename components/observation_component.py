import re
from typing import Dict, Any

# Fallback: define a placeholder ContextComponent
class ContextComponent:
    pass


class ObservationComponent(ContextComponent):
    def extract_price(self, message: str) -> int:
        prices = re.findall(r"\d{2,6}", message.replace(",", ""))
        return int(prices[0]) if prices else None

    def analyze_tone(self, message: str) -> str:
        message_lower = message.lower()
        if "final" in message_lower or "last" in message_lower:
            return "firm"
        if "maybe" in message_lower or "consider" in message_lower:
            return "flexible"
        return "neutral"

    def make_pre_act_value(self) -> str:
        return "Observation component active."

    def get_state(self) -> Dict[str, Any]:
        return {}

    def set_state(self, state: Dict[str, Any]) -> None:
        pass
