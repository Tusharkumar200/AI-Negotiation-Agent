# AI-Negotiation-Agent

A modular Python agent for buyer-seller negotiation simulations using LLMs (Hugging Face). Easily configure personalities, budgets, and test negotiation strategies.

---

## Features

- Modular components: memory, decision, observation, and personality
- Hugging Face LLM integration (via API)
- Configurable buyer archetypes
- Built-in seller mock for testing

---

## Quick Start

1. **Install requirements**  
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up `.env`**  
   ```
   HF_TOKEN=your_huggingface_token
   HF_MODEL=meta-llama/Meta-Llama-3-8B-Instruct
   ```

3. **Try a minimal negotiation loop:**
   ```python
   from buyer_agent import BuyerAgent, load_personality
   from utils.hf_model import HuggingFaceModel
   from tests.mock_seller import MockSeller

   personality = load_personality("Diplomatic-Analytical")
   model = HuggingFaceModel()
   agent = BuyerAgent("Alice", personality, model)
   scenario = {"product": {"name": "Mangoes", "base_market_price": 180000}, "budget": 200000, "seller_min": 150000}
   seller = MockSeller(scenario)
   for rnd in range(1, 4):
       seller_msg = seller.send_message()
       result = agent.negotiate(scenario["product"], scenario["budget"], seller_msg, rnd)
       print(result)
       if result["action"] == "ACCEPT": break
       seller.receive_buyer_offer(result["offer"])
   ```

---

## Personalities

Define archetypes and traits in `personality_config.json`:
```json
{
  "Diplomatic-Analytical": {
    "archetype": "Diplomatic-Analytical",
    "traits": ["patient", "data-driven", "polite"]
  }
}
```

---

## License

No license specified.  
[View full code on GitHub](https://github.com/Tusharkumar200/AI-Negotiation-Agent)
