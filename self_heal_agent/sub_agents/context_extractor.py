import os
import json  # New: Required for parsing the structured output from the LLM
from google.adk.agents import LlmAgent

# from google.adk.runners import InMemoryRunner
from google.adk.models.google_llm import Gemini

from ..config import config


content_extractor_agent = LlmAgent(
    name="ContentExtractorAgent",
    model=config.model_name,
    description="Extracts the URL and test script from a user's free-form input and outputs a JSON object.",
    instruction="""
        Analyze the user's request, which contains a website URL and a test script to run.
        Your sole task is to extract the website URL and the complete test script. 
        
        Output ONLY a valid JSON object with the following structure: 
        { "website": "...", "testScript": "..." }
        Do not add any greetings, explanations, or additional text outside of the JSON.
    """,
    output_key="user_input_json",  # Stores the raw JSON string output in the session state
)
