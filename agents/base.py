# base_agent
import os
from typing import List, Dict
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY_78060"),
)

class BaseAgent:
    def __init__(self, name: str, system_prompt: str, model: str = "meta-llama/llama-4-scout-17b-16e-instruct"):
        self.name = name
        self.system_prompt = {"role": "system", "content": system_prompt.strip()}
        self.model = model
        self.history: List[Dict[str, str]] = [self.system_prompt]

    def respond(self, message_from_other_agent: str) -> str:
        # Log the incoming message
        self.history.append({"role": "user", "content": message_from_other_agent})

        response = client.chat.completions.create(
            model=self.model,
            messages=self.history,
            temperature=0.7,
            max_tokens=300,
        )

        reply = response.choices[0].message.content.strip()
        self.history.append({"role": "assistant", "content": f"{self.name}: {reply}"})
        return reply
