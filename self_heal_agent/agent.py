# from google.adk.agents.llm_agent import Agent
from google.adk.agents import Agent, SequentialAgent

from .sub_agents.context_extractor import content_extractor_agent
from .sub_agents.language_detector import language_detector
from .sub_agents.docker_file_builder import docker_file_builder
from .sub_agents.code_executor import code_executor
from .sub_agents.log_analyzer import log_analyzer
from .sub_agents.healer import healer
from .sub_agents.fixer import fixer
from .config import config


root_agent = SequentialAgent(
    name="SelfHealPipeline",
    sub_agents=[
        content_extractor_agent,
        language_detector,
        docker_file_builder,
        code_executor,
        log_analyzer,
        healer,
        fixer,
    ],
)
