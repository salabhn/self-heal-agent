from pathlib import Path
from typing import List

import docker

# from docker import errors
from .config import config


async def build_docker_image(
    test_script: str, docker_file_content: str, run_cmd: List[str]
) -> dict:
    """Builds a docker image to based on given docker file conent

    Args:
        test_script (str): The test script to execute
        docker_file_content (str): Contents of Dockerfile to create the image
        run_cmd (List[str]) : The command parts to run the test script as a list (e.g., ["python", "script.py"])

    Returns:
        dict: Image build results in the format
        {
        "status": "success" | "failed",
        "docker_image": ...,
        "logs": [...]
        }
    """
    sandbox_dir = Path(config.sandbox_path)
    sandbox_dir.mkdir(parents=True, exist_ok=True)
    docker_file = sandbox_dir / "Dockerfile"
    with docker_file.open("w", newline="") as f:
        f.write(docker_file_content)
    script_path = sandbox_dir / run_cmd[-1]
    with script_path.open("w", newline="") as f:
        f.write(test_script)
    print(f"Written docker file contents to {docker_file}")
    client = docker.from_env()
    try:
        # file_obj = BytesIO(docker_file_content.encode())
        print("Building image")
        d_image, build_logs = client.images.build(
            path=str(sandbox_dir.resolve()),
            rm=True,
        )
        print(f"Image build success.")
        return {"status": "success", "image": d_image.attrs["Id"]}
    except docker.errors.BuildError as e:  # type: ignore
        build_logs = list(e.build_log)
        print(f"Error building image. {build_logs[-2:]}")
        return {
            "docker_image": "",
            "status": "failed",
            "logs": build_logs[-5:],
        }


async def run_docker_container(docker_image: str) -> dict:
    """Run docker container from given docker image

    Args:
        docker_image (str): Name of the docker image.

    Returns:
        dict: Container results in the format
        {
        "status": ..., # success | failed
        "logs": [...]
        }
    """
    client = docker.from_env()
    try:
        print("Creating container")
        lc = docker.types.LogConfig(  # type: ignore
            type=docker.types.LogConfig.types.JSON,  # type: ignore
            config={"max-size": "1g", "labels": "production_status,geo"},
        )
        container = client.containers.run(
            docker_image,
            log_config=lc,
            environment={"PYTHONUNBUFFERED": "1"},
        )
        print("Container run success")
        print(container)
        return {"status": "success", "logs": container}
    except Exception as e:
        print("Error building container")
        print(e)
        return {"status": "failed", "logs": ["Error running container", str(e)]}
