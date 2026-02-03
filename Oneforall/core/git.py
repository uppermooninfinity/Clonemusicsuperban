import asyncio
import shlex
from typing import Tuple

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

import config
from ..logging import LOGGER


def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    return asyncio.get_event_loop().run_until_complete(install_requirements())


def git():
    # 🔒 If no token → skip git completely (NO CRASH)
    if not config.GIT_TOKEN:
        LOGGER(__name__).warning("GIT_TOKEN not set, skipping git update")
        return

    REPO_LINK = config.UPSTREAM_REPO

    try:
        GIT_USERNAME = REPO_LINK.split("com/")[1].split("/")[0]
        TEMP_REPO = REPO_LINK.split("https://")[1]
        AUTH_REPO = f"https://{GIT_USERNAME}:{config.GIT_TOKEN}@{TEMP_REPO}"
    except Exception as e:
        LOGGER(__name__).error(f"Invalid UPSTREAM_REPO format: {e}")
        return

    try:
        repo = Repo()
        LOGGER(__name__).info("Git repository found")
    except InvalidGitRepositoryError:
        LOGGER(__name__).info("No git repo found, initializing new one")
        repo = Repo.init()
        repo.create_remote("origin", AUTH_REPO)

    try:
        origin = repo.remote("origin")
        origin.set_url(AUTH_REPO)

        origin.fetch()
        origin.pull()

        install_req("pip3 install --no-cache-dir -r requirements.txt")
        LOGGER(__name__).info("Successfully fetched updates from upstream")

    except GitCommandError as e:
        LOGGER(__name__).error(f"Git update failed: {e}")
        return