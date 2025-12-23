from ...utils import EnvUtils, get_logger

logger = get_logger(__name__)


class UnstructuredParser:
    def __init__(self, config: dict):
        EnvUtils.ensure_package("unstructured")

    async def parse(self, path: str) -> str:
        from unstructured.partition.auto import partition

        logger.info(f"Parsing {path}")
        elements = partition(filename=str(path))
        return "\n\n".join([str(el) for el in elements])
