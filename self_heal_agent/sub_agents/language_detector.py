from google.adk.agents import Agent

from ..config import config


def build_prompt(script_content: str) -> str:
    """Builds the prompt to be given to language detector agent

    Args:
        script_content: Script content
    Returns:
        str: Formatted prompt string
    """

    system_prompt = """You are a test automation expert. Analyze the provided test script and identify:
        1. Programming language (python, javascript, bdd, etc.)
        2. Test framework (pytest, unittest, cypress, playwright, jest, behave, etc.)
        3. Appropriate command to run the test

        Respond with a JSON object in this exact format:
        {
        "language": "python|javascript|bdd|etc",
        "framework": "pytest|unittest|cypress|playwright|jest|behave|selenium|etc",
        "runner_cmd": "command to run the test",
        "confidence": 0.0-1.0,
        "reasoning": "brief explanation"
        }"""

    few_shot_examples = """Example 1:
        Script:
        ```python
        import pytest
        def test_login():
            assert True
        ```
        Response:
        {"language": "python", "framework": "pytest", "runner_cmd": "pytest test_file.py", "confidence": 0.95, "reasoning": "Uses pytest import and test_ prefix"}

        Example 2:
        Script:
        ```javascript
        describe('Login', () => {
        it('should login', () => {
            cy.visit('/login')
        })
        })
        ```
        Response:
        {"language": "javascript", "framework": "cypress", "runner_cmd": "npx cypress run", "confidence": 0.95, "reasoning": "Uses Cypress API (cy.visit, describe, it)"}"""

    # Truncate script if too long (keep first 2000 chars)
    script_preview = script_content[:2000]
    if len(script_content) > 2000:
        script_preview += "\n... (truncated)"

    prompt = f"""{system_prompt}

        ## Few-Shot Examples:
        {few_shot_examples}

        ## Test Script to Analyze:
        ```
        {script_preview}
        ```

        Analyze this script and provide the JSON response:"""

    return prompt


language_detector = Agent(
    model=config.model_name,
    name="language_detector",
    description="Identify the programming language details from given script",
    static_instruction=f"""You are a test automation expert. Analyze the provided test script and identify:
        1. Programming language (python, javascript, bdd, etc.)
        2. Test framework (pytest, unittest, cypress, playwright, jest, behave, etc.)
        3. Appropriate command to run the test

        Respond with a JSON object in this exact format:
        {{
        "language": "python|javascript|bdd|etc",
        "framework": "pytest|unittest|cypress|playwright|jest|behave|selenium|etc",
        "runner_cmd": "command to run the test as an array of strings",
        "confidence": 0.0-1.0,
        "reasoning": "brief explanation",
        }}

        ## Few-Shot Examples:
        Example 1:
        Script:
        ```python
        import pytest
        def test_login():
            assert True
        ```
        Response:
        {{"language": "python", "framework": "pytest", "runner_cmd": "pytest test_file.py", "confidence": 0.95, "reasoning": "Uses pytest import and test_ prefix"}}

        Example 2:
        Script:
        ```javascript
        describe('Login', () => {{
        it('should login', () => {{
            cy.visit('/login')
        }})
        }})
        ```
        Response:
        {{"language": "javascript", "framework": "cypress", "runner_cmd": "npx cypress run", "confidence": 0.95, "reasoning": "Uses Cypress API (cy.visit, describe, it)"}}""",
    instruction="""## Test Script to Analyze:
        ```
        {{ user_input_json["testScript"] }}
        ```""",
    output_key="language_detection_results",
)
