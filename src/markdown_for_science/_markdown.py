import mistune
from markdown_for_science._renderer import LaTeXRenderer
from markdown_for_science.plugins import create_plugins
from mistune import Markdown


class ExtendedMarkdown:
    """Encapsulate the standard Markdown object"""

    front_matter = "\\documentclass{article}\n\\begin{document}\n"
    end_matter = "\\end{document}\n"

    def __init__(self, markdown: Markdown):
        self.markdown = markdown

    def __getattr__(self, item):
        return getattr(self.markdown, item)

    def parse(self, s, state=None):
        result = self.markdown.parse(s, state)
        return self.front_matter + result + self.end_matter

    def __call__(self, s):
        return self.parse(s)


def create_markdown(acronym_file: str = None):
    extended_markdown = mistune.create_markdown(
        renderer=LaTeXRenderer(), plugins=create_plugins(acronym_file),
    )
    return ExtendedMarkdown(extended_markdown)
