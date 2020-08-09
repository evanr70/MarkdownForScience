from markdown_for_science._renderer import LaTeXRenderer
from markdown_for_science.inline_parser import ExtendedInlineParser
from mistune import Markdown, HTMLRenderer, AstRenderer, PLUGINS


class ExtendedMarkdown(Markdown):
    doc_class = "\\documentclass{{{document_class}}}\n"
    graphicx = "\\usepackage{graphicx}\n"
    hyperref = "\\usepackage{hyperref}\n"
    csquotes = "\\usepackage{csquotes}\n"
    listings = (
        "\\usepackage{listings}\n"
        "\\lstset{basicstyle=\\footnotesize\\ttfamily,breaklines=true}\n"
        "\\lstset{framextopmargin=50pt,frame=b}\n"
        "\\lstset{backgroundcolor=\\color{lightgray!20}}\n"
    )
    xcolor = "\\usepackage[dvipsnames]{xcolor}\n"
    commands = (
        "\\makeatletter\n"
        "\\def\\maxwidth#1{\\ifdim\\Gin@nat@width>#1 #1"
        "\\else\\Gin@nat@width\\fi}\n\\makeatother\n"
    )
    begin = "\\begin{document}\n"
    end_matter = "\\end{document}\n"

    def __init__(
        self,
        renderer,
        inline=None,
        block=None,
        plugins=None,
        bibliography="",
        chapters=False,
        toc=False,
    ):
        super().__init__(renderer, inline=inline, block=block, plugins=plugins)

        self.document_class = "report" if chapters else "article"

        self.biblatex = ""
        self.bib_resource = ""
        self.print_bib = ""
        if bibliography:
            self.biblatex = "\\usepackage[backend=biber,style=nature]{biblatex}\n"
            self.bib_resource = f"\\addbibresource{{{bibliography}}}\n"
            self.print_bib = "\\printbibliography\n"
        self.table_of_contents = ""
        if toc:
            self.table_of_contents = "\\tableofcontents\n"

    def latex_parse(self, s, state=None):
        result = self.parse(s, state)
        return "".join(
            [
                self.doc_class.format(document_class=self.document_class)
                + self.graphicx
                + self.hyperref
                + self.csquotes
                + self.xcolor
                + self.listings
                + self.biblatex
                + self.bib_resource
                + self.commands
                + self.begin
                + self.table_of_contents
                + result
                + self.print_bib
                + self.end_matter
            ]
        )

    def __call__(self, s):
        return self.latex_parse(s)


def create_markdown(
    escape=True,
    renderer=None,
    plugins=None,
    acronyms=None,
    bibliography="",
    chapters=False,
    toc=False,
):
    """Create a Markdown instance based on the given condition.

    :param escape: Boolean. If using html renderer, escape html.
    :param renderer: renderer instance or string of ``html`` and ``ast``.
    :param plugins: List of plugins, string or callable.

    This method is used when you want to re-use a Markdown instance::

        markdown = create_markdown(
            escape=False,
            renderer='html',
            plugins=['url', 'strikethrough', 'footnotes', 'table'],
        )
        # re-use markdown function
        markdown('.... your text ...')
    """
    if renderer is None or renderer == "latex":
        renderer = LaTeXRenderer(acronym_file=acronyms, chapters=chapters)
    if renderer == "html":
        renderer = HTMLRenderer(escape=escape)
    elif renderer == "ast":
        renderer = AstRenderer()

    if plugins:
        _plugins = []
        for p in plugins:
            if isinstance(p, str):
                _plugins.append(PLUGINS[p])
            else:
                _plugins.append(p)
        plugins = _plugins
    return ExtendedMarkdown(
        renderer,
        inline=ExtendedInlineParser(renderer, chapters=chapters),
        plugins=plugins,
        bibliography=bibliography,
        chapters=chapters,
        toc=toc,
    )
