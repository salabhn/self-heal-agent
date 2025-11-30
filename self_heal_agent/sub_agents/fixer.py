from google.adk.agents import Agent
from google.adk.tools import AgentTool  # type: ignore

from ..config import config


fixer = Agent(
    model=config.model_name,
    name="fixer",
    description="You are a test automation expert.",
    instruction="""Your job is to apply patches to the test script based on the unified diff from {{ healer_results }}
    Apply fixes to {{ user_input_json["testScript"] }} and return the results in a yaml block like.
    ```python
    <complete fixed code>
    ```
    ## Additional context:
    Programming language: {{ language_detection_results["language"] }}
    Framework: {{language_detection_results["framework"] }}
    """,
)
