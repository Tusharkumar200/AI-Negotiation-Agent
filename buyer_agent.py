import os
import json
from typing import Dict, Any
from dotenv import load_dotenv

from components.memory_component import BuyerMemoryComponent
from components.personality_component import BuyerPersonalityComponent
from components.observation_component import ObservationComponent
from components.decision_component import DecisionComponent
from utils.helpers import load_product_data
from utils.hf_model import HuggingFaceModel  # ✅ Our Hugging Face wrapper

# Load .env variables
load_dotenv()

HERE = os.path.dirname(os.path.abspath(__file__))


class BuyerAgent:
    """
    AI Buyer Agent using Concordia components + Hugging Face LLM.
    """

    def __init__(self, name: str, personality_cfg: Dict[str, Any], model: HuggingFaceModel):
        self.name = name
        self.personality_cfg = personality_cfg
        self.model = model
        self._build_components()

    def _build_components(self):
        """Initialize all Concordia-style components."""
        self.memory = BuyerMemoryComponent()
        self.personality = BuyerPersonalityComponent(self.personality_cfg)
        self.observation = ObservationComponent()
        self.decision = DecisionComponent(self.personality_cfg)

    def negotiate(self, product: Dict[str, Any], budget: int, seller_message: str, round_num: int) -> Dict[str, Any]:
        """
        Main negotiation loop per round.
        """
        # Step 1: Understand seller
        seller_price = self.observation.extract_price(seller_message)
        seller_tone = self.observation.analyze_tone(seller_message)

        # Step 2: Decide next move
        decision = self.decision.compute({
            "product": product,
            "budget": budget,
            "market": product.get("market_price"),
            "seller_price": seller_price,
            "seller_tone": seller_tone,
            "round": round_num,
            "last_offer": self.memory.last_offer
        })

        # Step 3: Build context for LLM
        system_prompt = f"""
You are {self.name}, a {self.personality_cfg['archetype']} buyer.
Traits: {', '.join(self.personality_cfg['traits'])}.
You are negotiating for {product['name']}.
Budget: ₹{budget}.
Never exceed your budget. 
Maintain personality consistency.
Negotiation history:
{self.memory.make_pre_act_value()}
        """.strip()

        # Step 4: Generate natural response
        buyer_msg = self.model.generate(
            prompt=system_prompt +
                   f"\nSeller: {seller_message}\n" +
                   f"Action: {decision['action']} ₹{decision['offer']}\n" +
                   "Buyer message:",
            max_tokens=50
        )

        # Step 5: Save round to memory
        self.memory.record_round({
            "round": round_num,
            "seller_price": seller_price,
            "seller_message": seller_message,
            "buyer_offer": decision["offer"],
            "buyer_action": decision["action"]
        })

        return {
            "action": decision["action"],
            "offer": decision["offer"],
            "message": buyer_msg.strip()
        }


def load_personality(name: str) -> Dict[str, Any]:
    """Load personality from JSON file."""
    cfg_path = os.path.join(HERE, "personality_config.json")
    with open(cfg_path, "r", encoding="utf-8") as f:
        all_cfg = json.load(f)
    return all_cfg.get(name, list(all_cfg.values())[0])


def run_demo():
    from tests.mock_seller import MockSeller

    # Load data
    product_data = load_product_data(os.path.join(HERE, "data", "products.json"))
    personality_cfg = load_personality("Diplomatic-Analytical")

    # Initialize Hugging Face LLM
    model = HuggingFaceModel(
        model_name=os.getenv("HF_MODEL", "meta-llama/Meta-Llama-3-8B-Instruct"),
        api_token=os.getenv("HF_TOKEN")
    )

    # Create buyer
    buyer = BuyerAgent("BuyerBot", personality_cfg, model)

    # Test scenarios
    scenarios = [
        ("Easy Market", product_data[0]),
        ("Tight Budget", product_data[1]),
        ("Premium Product", product_data[2])
    ]

    for scenario_name, product in scenarios:
        print("\n" + "=" * 50)
        print(f"Scenario: {scenario_name}")
        seller = MockSeller(product)
        budget = product["budget"]

        for rnd in range(1, 11):
            seller_msg = seller.send_message()
            decision = buyer.negotiate(product, budget, seller_msg, rnd)
            print(f"[Round {rnd}] Buyer -> action={decision['action']} offer={decision['offer']} msg={decision['message']}")

            if decision["action"].upper() == "ACCEPT":
                print(f"Buyer accepted at seller price {decision['offer']}")
                break

            seller.receive_buyer_offer(decision["offer"])


if __name__ == "__main__":
    run_demo()
