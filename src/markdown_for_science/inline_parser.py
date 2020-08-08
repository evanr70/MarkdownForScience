from mistune.inline_parser import *


# noinspection PyMethodMayBeStatic
class ExtendedInlineParser(InlineParser):
    IMAGE_OPTIONS = r"\!\[(.*?)\]\((.*?)\)(?:\[width=(.*?)\])?(?:\[height=(.*?)\])?"
    CITATION = r"<< *(.*?) *>>"
    DISPLAY_MATH = r"^\s*?\$\$(.*?)\$\$.*?"
    INLINE_MATH = r"(\$.*?\$)"
    ACRONYM = r"(%{1,2}) *(.+?) *(%{1,2})"

    def __init__(self, renderer):
        self.RULE_NAMES = (
            "image_options",
            "citation",
            "display_math",
            "inline_math",
            "acronym",
            *self.RULE_NAMES,
        )
        super().__init__(renderer)

    def parse_image_options(self, m, state):
        caption = m.group(1)
        src = m.group(2)
        width = m.group(3)
        height = m.group(4)
        return "image_options", src, caption, width, height

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
