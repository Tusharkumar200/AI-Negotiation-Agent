# tests/test_negotiation.py
import os
import json
from buyer_agent import BuyerAgent, load_personality
from tests.mock_seller import MockSeller

def test_agent_runs_and_never_exceeds_budget():
    # load personalities
    personality = load_personality("Diplomatic-Analytical")
    # Create a dummy minimal model object with generate() for tests
    class DummyModel:
        def generate(self, prompt: str, max_tokens: int = 64):
            # return a deterministic short response
            return "Let's find a middle ground. I can offer this price."

    model = DummyModel()
    agent = BuyerAgent("TestAgent", personality, model)

    # simple product
    product_info = {"product":{"name":"Alphonso Mangoes","quantity":100,"base_market_price":180000}, "budget":200000, "seller_min":150000}
    seller = MockSeller(product_info)

    budget = product_info["budget"]

    seller_msg = seller.send_message()
    for rnd in range(1, 8):
        decision = agent.negotiate(product_info["product"], budget, seller_msg, rnd)
        # decision should have action and offer keys
        assert "action" in decision and "offer" in decision
        # if action is accept, ensure accepted price <= budget
        if decision["action"].lower() == "accept":
            assert decision["offer"] <= budget
            break
        seller.receive_buyer_offer(decision["offer"])
