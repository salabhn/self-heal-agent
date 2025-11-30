from google.adk.agents import Agent
from google.adk.tools import AgentTool  # type: ignore

from ..config import config


fixer = Agent(
    model=config.model_name,
    name="fixer",
    description="You are a test automation expert.",
    instruction="""Your job is to apply patches to the test script based on the unified diff from {{ healer_results }}
    Apply fixes to {{ user_input_json["testScript"] }} and return the results in the following format.
    - A brief summary of the test execution
    - Mention any test case fails that were not due to the script
    - A brief summary of test fails due to the script and fixes applied
    - The full fixed test script in a yaml block like.
    ```<language>
    <complete fixed code>
    ```
    ## Additional context:
    Programming language: {{ language_detection_results["language"] }}
    Framework: {{language_detection_results["framework"] }}
    """,
)
