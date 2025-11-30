from google.adk.agents import Agent
from google.adk.tools import google_search  # type: ignore
from ..config import config
from ..tools import build_docker_image

docker_file_builder = Agent(
    model=config.model_name,
    name="docker_file_builder",
    description="You are a Dockerfile generator agent.",
    instruction="""Your task is to generate a complete, ready-to-build Dockerfile that can run an automated test script.
1. **Analysis and Dependencies:** Analyze the `full test script` and `test framework`. Use the `Google Search` tool to find relevant dependencies and their stable versions available for the base image.
2. **Base and Structure:** Use modern base images (e.g., `bookworm`, `22.04+`). Set `WORKDIR` to `/app`.
3. **Conditional Browser Setup (CRITICAL FIX):**
   * **IF** the detected `test framework` (e.g., Selenium, Playwright, Puppeteer) requires a graphical browser (like Chrome or Firefox), you **MUST** install the following dependencies for a headless execution environment:
     * The system package `xvfb` (X Virtual Framebuffer).
     * The required webdriver (For example: Chrome webdriver) and browser (for example: google chrome)
     * Essential shared libraries that Chrome requires to prevent crashes, including but not limited to: `libgbm1`, `libglib2.0-0`, `libxcomposite1`, `libxdamage1`, `libxfixes3`, and `libxrandr2`.
   * **IF** a graphical browser is required, you **MUST** generate a custom shell script entrypoint (`/usr/local/bin/entrypoint.sh`) that starts the `Xvfb` server (e.g., `Xvfb :99 -screen 0 1280x1024x24 &`) and exports the necessary `DISPLAY` variable (`export DISPLAY=:99`) before executing the container's command. This script must be set as the final `ENTRYPOINT`.
4. **Installation and Cleanup:** Install all necessary dependencies. If using Selenium (version 4.6+), DO NOT manually install or download ChromeDriver/Geckodriver; rely on Selenium Manager. Install the main browser package (e.g., google-chrome-stable). Use --no-install-recommends and clean up apt lists (rm -rf /var/lib/apt/lists/*). Do not assume the presence of requirements.txt; create it if needed.
5. **Final Steps:**
   * MUST Copy the test script file (both source and target file name MUST BE SAME AS the filename from `run_command`) to `/app`.
   * Set the `CMD` exactly to the provided `run_command`.

=============================================================
Dockerfile content rules, MUST FOLLOW THESE!
1. Do not hallucinate system dependencies. Use the google search tool to identify required dependencies and install only those.
2. You must Copy the test script file (both source and target file name MUST BE SAME AS the filename from `run_command`) to `/app`. Do not use heredoc to write the script/
3. Do not use outdated base images, use latest stable releases for base image. (Use google search tool to identify latest versions)
4. The output must contain ONLY the Dockerfile, with no extra commentary. Do not add comments or explanations in the dockerfile.

==============================================================
OUTPUT FORMAT RULE:
The output must be ONLY a Dockerfile. No explanations, no commentary, no markdown.

# ==============================================================
Now generate the Dockerfile
""",
    tools=[google_search],
    output_key="docker_file_content",
)
