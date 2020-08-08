# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound
from markdown_for_science._renderer import LaTeXRenderer
from markdown_for_science._markdown import create_markdown, ExtendedMarkdown

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = 'MarkdownForScience'
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = 'unknown'
finally:
    del get_distribution, DistributionNotFound
