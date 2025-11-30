from google.adk.agents import Agent

from ..config import config


log_analyzer = Agent(
    model=config.model_name,
    name="log_analyzer",
    description="You are a test automation expert.",
    instruction="""Analyze the error logs and  for all failed test cases, provide:
    1. Root cause analysis (what actually caused the error)
    2. Suggested fix category (e.g., "add_wait", "fix_selector", "increase_timeout", "fix_assertion")
    3. Severity assessment (low, medium, high, critical)
    4. More specific error classification if the current one is too generic

    Respond with JSON in this format:
    [{
    "test_case": "the failed test case name",
    "root_cause": "detailed explanation of the root cause",
    "suggested_fix_category": "category name",
    "severity": "low|medium|high|critical",
    "error_type": "optional more specific error type"
    }]
    =======================
    Full logs:
    {{ test_run_results["logs"] }}
    =======================
    Provide enhanced analysis:
    """,
    output_key="log_analysis_report",
)
