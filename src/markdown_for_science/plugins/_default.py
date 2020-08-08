from markdown_for_science.plugins._base import plugin_factory, plugin_from_functions


def create_plugins(acronym_file=None):
    citation_plugin = plugin_factory(r"<< *(.*?) *>>", "\\cite{{{}}}", "citation")
    display_math_plugin = plugin_factory(
        r"^\s*?\$\$(.*?)\$\$.*?",
        "\\begin{{equation}}\n\t{}\n\\end{{equation}}",
        "display_math",
    )
    inline_math_plugin = plugin_factory(r"(\$.*?\$)", "{}", "inline_math")
    plugins = [citation_plugin, display_math_plugin, inline_math_plugin]
    if acronym_file:
        acronym_plugin = create_acronym_plugin(acronym_file)
        plugins.append(acronym_plugin)
    return plugins


def create_acronym_plugin(acronym_file: str):
    acronyms = {}
    if acronym_file is not None:
        with open(acronym_file, "r") as f:
            acronym_lines = f.read().splitlines()

        for acronym_line in acronym_lines:
            ref, short, full = acronym_line.split(",")
            acronyms[ref] = {"short": short, "full": full, "used": False}

    pattern = r"(%{1,2}) *(.+?) *(%{1,2})"

    name = "acronym"

    def parser(self, m, state):
        open_token = m.group(1)
        content = m.group(2)
        close_token = m.group(3)

        return name, open_token, content, close_token

    def renderer(open_token, content, close_token):
        if len(open_token) != len(close_token):
            return "".join([open_token, content, close_token])

        if content in acronyms:
            short = acronyms[content]["short"]
            long = acronyms[content]["full"]

            if len(open_token) == 2:
                long = long.capitalize()

            if acronyms[content]["used"]:
                acronym = short
            else:
                acronym = f"{long} ({short})"
                acronyms[content]["used"] = True

        else:
            acronym = f"UNKNOWN({content})"

        return acronym

    return plugin_from_functions(pattern, parser, renderer, name)
