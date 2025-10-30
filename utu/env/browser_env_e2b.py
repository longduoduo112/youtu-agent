import logging

from agents import Tool

from ..config import ToolkitConfig
from ..tools.utils import AgentsMCPUtils
from .base_env import BasicEnv

logger = logging.getLogger(__name__)


class BrowserE2BEnv(BasicEnv):
    """Browser environment for agents.
    Here we used TencentCloud's agend sandbox service. https://cloud.tencent.com/product/agentsandbox"""

    def __init__(self, config: dict = None):
        self.config = config or {}

    async def build(self):
        """Build the environment. We use docker to run a browser container."""
        from e2b import AsyncSandbox

        # start browser sandbox
        self.sandbox: AsyncSandbox = await AsyncSandbox.create(template="browser-v1", timeout=3600)
        sandbox_url = self.sandbox.get_host(9000)
        novnc_url = (
            f"https://{sandbox_url}/novnc/vnc_lite.html?&path=websockify?access_token={self.sandbox._envd_access_token}"
        )
        logger.info(f"browser sandbox created: {self.sandbox.sandbox_id}")
        logger.info(f"vnc url: {novnc_url}")
        cdp_url = f"https://{sandbox_url}/cdp"

        # run mcp server
        config = ToolkitConfig(
            mode="mcp",
            mcp_transport="stdio",
            config={
                "command": "npx",
                "args": [
                    "-y",
                    "@playwright/mcp@latest",
                    "--cdp-endpoint",
                    cdp_url,
                    "--cdp-header",
                    f"X-Access-Token: {self.sandbox._envd_access_token}",
                ],
            },
        )
        self.mcp_server = AgentsMCPUtils.get_mcp_server(config)
        await self.mcp_server.connect()

    async def cleanup(self):
        await self.mcp_server.cleanup()
        await self.sandbox.kill()

    async def get_tools(self) -> list[Tool]:
        """Get the tools available in the environment."""
        return await AgentsMCPUtils.get_tools_agents(self.mcp_server)
