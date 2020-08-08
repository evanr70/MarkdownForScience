def plugin_factory(input_pattern, output_pattern, name, group=1):
    def parser(self, m, state):
        content = m.group(group)
        return name, content

    def renderer(content):
        return output_pattern.format(content)

    def plugin(md):
        md.inline.register_rule(name, input_pattern, parser)
        md.inline.rules.append(name)
        md.renderer.register(name, renderer)

    return plugin


def plugin_from_functions(pattern, parser, renderer, name, block=False):
    def plugin(md):
        md.inline.register_rule(name, pattern, parser)
        md.inline.rules.append(name)
        md.renderer.register(name, renderer)

    return plugin
