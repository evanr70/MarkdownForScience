from mistune.inline_parser import *
import logging

_logger = logging.getLogger("MarkdownForScience")


# noinspection PyMethodMayBeStatic
class ExtendedInlineParser(InlineParser):
    IMAGE_OPTIONS = r"\!\[(.*?)\]\((.*?)\)(?:\[width=(.*?)\])?(?:\[height=(.*?)\])?"
    CITATION = r"<< *(.*?) *>>"
    DISPLAY_MATH = r"^\s*?\$\$(.*?)\$\$.*?"
    INLINE_MATH = r"(\$.*?\$)"
    ACRONYM = r"(%{1,2}) *(.+?) *(%{1,2})"
    CHAPTER = r"^\!#\s(.*?)(?:\r\n|\r|\n)?$"
    QUOTES = "(?<!\\S)([\"'])([^\\1]+?)\\1"

    def __init__(self, renderer, chapters):
        self.RULE_NAMES = (
            "quotes",
            "chapter",
            "image_options",
            "citation",
            "display_math",
            "inline_math",
            "acronym",
            *self.RULE_NAMES,
        )
        super().__init__(renderer)
        self.chapters = chapters

    def parse_image_options(self, m, state):
        caption = m.group(1)
        src = m.group(2)
        width = m.group(3)
        height = m.group(4)
        return "image_options", src, caption, width, height

    def parse_quotes(self, m, state):
        quote = m.group(0)[0]
        number = 1 if quote == "'" else 2
        text = m.group(2)
        return "quotes", number, text

    def parse_citation(self, m, state):
        return "citation", m.group(1)

    def parse_display_math(self, m, state):
        return "display_math", m.group(1)

    def parse_inline_math(self, m, state):
        return "inline_math", m.group(1)

    def parse_acronym(self, m, state):
        open_token = m.group(1)
        content = m.group(2)
        close_token = m.group(3)
        return "acronym", open_token, content, close_token

    def parse_chapter(self, m, state):
        if not self.chapters:
            _logger.warning(
                "Chapter notation (!#) has been found, but the "
                "program has been run with chapters set to False.\n"
                "If you expected chapters to be rendered, use the "
                "'--chapters/-c' option."
            )

        chapter_title = m.group(1)
        return "chapter", chapter_title
