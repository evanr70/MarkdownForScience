from mistune import HTMLRenderer
from markdown_for_science.latex import tex_escape


class LaTeXRenderer(HTMLRenderer):
    NAME = "latex"
    IS_TREE = False

    def __init__(self):
        super().__init__()

    def heading(self, text, level):
        command = "sub" * (level - 1) + "section"
        return f"\\{command}{{{text}}}\n\n"

    def text(self, text):
        return tex_escape(text)

    def paragraph(self, text):
        return text + "\n\n"
