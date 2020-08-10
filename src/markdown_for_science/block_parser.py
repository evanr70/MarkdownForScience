import logging
import re

from mistune.block_parser import BlockParser

_logger = logging.getLogger("MarkdownForScience")


# noinspection PyMethodMayBeStatic
class ExtendedBlockParser(BlockParser):
    ABSTRACT = re.compile(r"(?s)\[Abstract](.*?)\[Abstract]")

    def __init__(self):
        self.RULE_NAMES = (
            "abstract",
            *self.RULE_NAMES,
        )
        super().__init__()
        _logger.debug("Using ExtendedBlockParser")

    def parse_abstract(self, m, state):
        return {"type": "abstract", "raw": m.group(1)}
