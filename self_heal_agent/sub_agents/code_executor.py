from google.adk.agents import Agent

from ..config import config
from ..tools import build_docker_image, run_docker_container


code_executor = Agent(
    model=config.model_name,
    name="code_executor",
    description="You are a code execution agent.",
    instruction="""Your job is to:
     1. use the build_docker_image tool to build a docker image using {{docker_file_content}}. If build fails, analyze the logs and attempt to fix the docker file contents and retry. NOTE: Maximum 3 retries, if build still fails after 3 attempts, inform the user of the failure and stop.
     2. Use the run_docker_container tool to execute the test script using docker_image obtained from successful build_docker_image tool call and present the results.c all the tool only once. If it fails, present the reason for failure, DO NOT retry.
    """,
    tools=[build_docker_image, run_docker_container],
    output_key="test_run_results",
)
