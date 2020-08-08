"""Parse extended markdown to LaTeX

Usage:
  md4sci.py <toc> [--acronyms=<acronym_file>] [--output=<output_file] [--bibliography=<bib_file]

Arguments:
  <toc>  table of contents

Options:
  -a <acronym_file> --acronyms=<acronym_file>  File containing acronyms
  -o <output_file> --output=<output_file>  Output file
  -b <bib_file> --bibliography=<bib_file>  Bibliography file


"""

from docopt import docopt
from markdown_for_science import create_markdown


def text_from_table_of_contents(file_name: str):
    with open(file_name, "r") as toc_file:
        text_file_names = toc_file.read().splitlines()

    text_files = []
    for text_file_name in text_file_names:
        with open(text_file_name, "r") as text_file:
            text_files.append(text_file.read())

    full_text = "\n\n".join(text_files)
    return full_text


def run():
    arguments = docopt(__doc__)
    toc = arguments["<toc>"]
    output = arguments["--output"]
    acronyms = arguments["--acronyms"]
    bibliography = arguments["--bibliography"]

    info_string = f"Converting markdown file '{toc}' into latex file '{output}'"
    if acronyms is not None:
        info_string = info_string + f" using acronyms in '{acronyms}'"
    if bibliography is not None:
        info_string = info_string + f" and bibliography from '{bibliography}'"

    print(info_string)

    markdown_text = text_from_table_of_contents(toc)
    markdown = create_markdown(acronyms=acronyms, bibliography=bibliography)
    latex_text = markdown(markdown_text)

    with open(output, "w") as output_file:
        output_file.write(latex_text)


if __name__ == "__main__":
    run()
