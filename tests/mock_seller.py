# tests/mock_seller.py
from dataclasses import dataclass
from typing import Dict, Any
import random

@dataclass
class MockSeller:
    """
    Simple mock seller used by tests and demo runner.
    Behavior:
      - Opening ask = 150% of market
      - If buyer offer >= min_price * 1.1 -> accept
      - Else forms counter = max(min_price, int(buyer_offer * 1.15))
    """

    scenario: Dict[str, Any]

    def __post_init__(self):
        prod = self.scenario["product"]
        self.market_price = int(prod["base_market_price"])
        self.min_price = int(self.scenario.get("seller_min", int(self.market_price * 0.82)))
        self.opening_ask = int(self.market_price * 1.5)
        self._last_counter = self.opening_ask

    def send_message(self) -> str:
        """
        Seller sends the current asking message (opening or counter).
        """
        if self._last_counter is None:
            self._last_counter = self.opening_ask
        return f"Seller opening ask: ₹{self._last_counter}"

    def receive_buyer_offer(self, buyer_offer: int):
        """
        Update seller state given buyer offer and set next counter.
        """
        # if buyer offer is None or 0, set counter as opening ask
        if not buyer_offer:
            self._last_counter = self.opening_ask
            return
        # If buyer offer meets seller profit target -> seller would accept in real system
        if buyer_offer >= int(self.min_price * 1.1):
            # set flag by making _last_counter equal to buyer_offer (indicates acceptance in demo)
            self._last_counter = buyer_offer
            return
        # otherwise seller reduces price moderately (but not below min_price)
        proposed = max(self.min_price, int(buyer_offer * 1.15))
        # add small randomness to emulate real seller
        jitter = random.randint(-500, 500)
        proposed = max(self.min_price, proposed + jitter)
        self._last_counter = proposed
