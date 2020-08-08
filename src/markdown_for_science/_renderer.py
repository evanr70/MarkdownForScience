from markdown_for_science.latex import tex_escape
from os.path import expanduser

from mistune.renderers import BaseRenderer


# noinspection PyMethodMayBeStatic
class LaTeXRenderer(BaseRenderer):
    NAME = "latex"
    IS_TREE = False

    def __init__(self, acronym_file=None):
        self.acronyms = {}
        if acronym_file is not None:
            with open(acronym_file, "r") as f:
                acronym_lines = f.read().splitlines()

            for acronym_line in acronym_lines:
                ref, short, full = acronym_line.split(",")
                self.acronyms[ref] = {"short": short, "full": full, "used": False}

        super().__init__()

    def heading(self, text, level):
        command = "sub" * (level - 1) + "section"
        return f"\\{command}{{{text}}}\n\n"

    def text(self, text):
        return tex_escape(text)

    def paragraph(self, text):
        return text + "\n\n"

    def link(self, link, text=None, title=None):
        if text is None:
            text = link

        return f"\\href{{{tex_escape(link)}}}{{{tex_escape(text)}}}"

    def acronym(self, open_token, content, close_token):
        if len(open_token) != len(close_token):
            return "".join([open_token, content, close_token])

        if content in self.acronyms:
            short = self.acronyms[content]["short"]
            long = self.acronyms[content]["full"]

            if len(open_token) == 2:
                long = long.capitalize()

            if self.acronyms[content]["used"]:
                acronym = short
            else:
                acronym = f"{long} ({short})"
                self.acronyms[content]["used"] = True

        else:
            acronym = f"UNKNOWN({content})"

        return acronym

    def image_options(self, src, alt="", title="", width="", height=""):
        begin = "\\begin{{figure}}"
        include = "\t\\includegraphics{options}{{{image}}}"
        centering = "\t\\centering"
        caption_placeholder = "{caption}"
        end = "\\end{{figure}}"

        latex_string = "\n".join([begin, include, centering, caption_placeholder, end])

        options = ""
        caption = ""

        if not width and not height:
            options = r"[width=\maxwidth{\textwidth}]"
        if width:
            options = f"[width={width}]"
        if height:
            options = f"[height={height}]"
        if title:
            caption = f"\t\\caption{title}"

        latex_string = latex_string.format(
            options=options, image=expanduser(src), caption=tex_escape(caption),
        )

        return latex_string

    def citation(self, label):
        return f"\\cite{{{label}}}"

    def display_math(self, equation):
        return f"\\begin{{equation}}\n\t{equation}\n\\end{{equation}}"

    def inline_math(self, equation):
        return equation

    def emphasis(self, text):
        return "<em>" + text + "</em>"

    def strong(self, text):
        return "<strong>" + text + "</strong>"

    # def codespan(self, text):
    #     return "<code>" + escape(text) + "</code>"

    def linebreak(self):
        return "<br />\n"

    # def inline_html(self, html):
    #     if self._escape:
    #         return escape(html)
    #     return html

    def newline(self):
        return ""

    def thematic_break(self):
        return "<hr />\n"

    def block_text(self, text):
        return text

    # def block_code(self, code, info=None):
    #     html = "<pre><code"
    #     if info is not None:
    #         info = info.strip()
    #     if info:
    #         lang = info.split(None, 1)[0]
    #         lang = escape_html(lang)
    #         html += ' class="language-' + lang + '"'
    #     return html + ">" + escape(code) + "</code></pre>\n"

    def block_quote(self, text):
        return "<blockquote>\n" + text + "</blockquote>\n"

    # def block_html(self, html):
    #     if not self._escape:
    #         return html + "\n"
    #     return "<p>" + escape(html) + "</p>\n"

    def block_error(self, html):
        return '<div class="error">' + html + "</div>\n"

    def list(self, text, ordered, level, start=None):
        if ordered:
            html = "<ol"
            if start is not None:
                html += ' start="' + str(start) + '"'
            return html + ">\n" + text + "</ol>\n"
        return "<ul>\n" + text + "</ul>\n"

    def list_item(self, text, level):
        return "<li>" + text + "</li>\n"
