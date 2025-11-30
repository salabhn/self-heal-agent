from google.adk.agents import Agent

from ..config import config


fix_suggester = Agent(
    model=config.model_name,
    name="fix_suggester",
    description="You are a test automation expert.",
    instruction="""Based on the error and test code, provide ranked suggestions for fixing the issue.
    Use the fix_suggeston
Respond with JSON array of suggestions:
[
  {
    "text": "suggestion text",
    "confidence": 0.0-1.0,
    "category": "category name",
    "explanation": "brief explanation"
  }
]
Rank suggestions by relevance and feasibility. Include framework-specific best practices.""",
)
