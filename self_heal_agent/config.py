from dataclasses import dataclass
import os
from pathlib import Path


@dataclass
class LLMConfig:
    model_name: str = os.getenv("LLM_MODEL_NAME", default="gemini-2.5-flash")
    sandbox_path: str = str(Path("./sandbox_folder").resolve())


config = LLMConfig()
