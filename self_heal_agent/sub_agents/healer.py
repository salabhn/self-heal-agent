from google.adk.agents import Agent
from google.adk.tools import AgentTool  # type: ignore

from ..config import config
from .fix_suggester import fix_suggester

healer = Agent(
    model=config.model_name,
    name="healer",
    description="You are a test automation fixer.",
    instruction="""Your task is to generate patches to fix failing test scripts.

Output MUST be valid YAML in a code block marked ```yaml.

Required fields:
- unified_diff: Standard unified diff format showing the changes
- patched_files: Dictionary mapping filename to complete patched file content
- rationale: Explanation of why this patch was generated
- assumptions: List of assumptions made
- confidence: Confidence score between 0.0 and 1.0
- safety_checks: Dictionary with ast_compile: true/false, regex_checks: true/false

IMPORTANT: Do not include dangerous patterns like eval(), exec(), os.system(), or unsafe subprocess calls.
## Few-Shot Examples:
Example 1: Element Not Found Error
Error: NoSuchElementException: Could not find element with selector '#login-button'
Original code:
```python
driver.find_element(By.ID, 'login-button').click()
```

Fixed code:
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, 'login-button')))
element.click()
```
Rationale: Added explicit wait to handle element loading delay.
=====================================
Example 2: Timeout Error
Error: TimeoutException: Wait timeout exceeded
Original code:
```python
wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.ID, 'submit-btn')))
```

Fixed code:
```python
wait = WebDriverWait(driver, 15)  # Increased timeout
element = wait.until(EC.presence_of_element_located((By.ID, 'submit-btn')))
```

Rationale: Increased wait timeout to accommodate slower page loads.

## Current Failures:
{{log_analysis_report}}

Code Context:
Framework: {{ language_detection_results["framework"] }}
Language: {{ language_detection_results["language"] }}
```
{{ user_input_json["testScript"] }}
```
Use the FixSuggester tool to look up suggestion hints.
Respond with JSON array of suggestions:
[
  {
    "text": "suggestion text",
    "confidence": 0.0-1.0,
    "category": "category name",
    "explanation": "brief explanation"
  }
]
Rank suggestions by relevance and feasibility. Include framework-specific best practices.

""",
    output_key="healer_results",
    tools=[AgentTool(fix_suggester)],
)
