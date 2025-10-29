from ..utils import get_logger
from .base_env import BasicEnv

logger = get_logger(__name__)


class E2BEnv(BasicEnv):
    def __init__(self):
        pass

    async def build(self):
        """Build the environment."""
        from e2b_code_interpreter import AsyncSandbox

        self.sandbox = await AsyncSandbox.create(template="code-interpreter-v1", timeout=3600)
        logger.info(f"E2B sandbox created with id: {self.sandbox.sandbox_id}")

    def get_state(self) -> str:
        return ""
