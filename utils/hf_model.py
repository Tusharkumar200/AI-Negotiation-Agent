# utils/hf_model.py
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class HuggingFaceModel:
    """
    Hugging Face API wrapper for LLaMA-3 and other models.
    Auto-switches between chat_completion and text_generation.
    """
    def __init__(self, model_name=None, api_token=None):
        self.model_name = model_name or os.getenv("HF_MODEL")
        self.api_token = api_token or os.getenv("HF_TOKEN")

        if not self.api_token:
            raise ValueError("Missing Hugging Face API token. Set HF_TOKEN in .env file.")

        self.client = InferenceClient(model=self.model_name, token=self.api_token)

    def generate(self, prompt: str, max_tokens: int = 128, temperature: float = 0.7) -> str:
        """
        Generate a response from HF API.
        Uses chat_completion for LLaMA-3, text_generation otherwise.
        """
        if "llama" in self.model_name.lower():
            # LLaMA-3 uses chat-based API
            completion = self.client.chat_completion(
                messages=[
                    {"role": "system", "content": "You are a helpful negotiation assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return completion.choices[0].message["content"].strip()

        # Fallback for normal text-generation models
        output = self.client.text_generation(
            prompt,
            max_new_tokens=max_tokens,
            temperature=temperature,
            do_sample=True,
            repetition_penalty=1.1
        )
        return output.strip()
