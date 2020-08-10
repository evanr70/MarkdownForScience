"""Parse extended markdown to LaTeX

Usage:
  md4sci.py <input_file> [--toc] [--acronyms=<acronym_file>] [--output=<output_file] [--bibliography=<bib_file] [--markdown=<markdown_file>] [--chapters] [--print-toc]

Arguments:
  <input_file>  input file

Options:
  --toc  Is the input file a table of contents?
  -a <acronym_file> --acronyms=<acronym_file>  File containing acronyms
  -o <output_file> --output=<output_file>  Output file
  -b <bib_file> --bibliography=<bib_file>  Bibliography file
  -m <markdown_file> --markdown=<markdown_file>  Save the collected markdown to a file
  -c --chapters  Use the article format with chapters
  -T --print-toc  Add a table of contents to the document


"""

from docopt import docopt
from markdown_for_science import create_markdown
from markdown_for_science.ascii import ascii_sequence


def text_from_table_of_contents(file_name: str):
    with open(file_name, "r") as toc_file:
        text_file_names = toc_file.read().splitlines()

    text_files = []
    for text_file_name in text_file_names:
        text_file_name = text_file_name.lstrip()
        with open(text_file_name, "r") as text_file:
            text_files.append(text_file.read())

    full_text = "\n\n".join(text_files)
    return full_text


def text_from_file(filename: str):
    with open(filename, "r") as input_file:
        text = input_file.read()
    return text


def run():
    arguments = docopt(__doc__)
    input_file = arguments["<input_file>"]
    toc = arguments["--toc"]
    output = arguments["--output"]
    acronyms = arguments["--acronyms"]
    bibliography = arguments["--bibliography"]
    markdown_file_name = arguments["--markdown"]
    chapters = arguments["--chapters"]
    print_toc = arguments["--print-toc"]

    print(ascii_sequence)

    if not output:
        output = input_file.replace(".md", "")
        output = output + ".tex"

    info_string = f"Converting markdown file '{input_file}' into latex file '{output}'"
    if acronyms is not None:
        info_string = info_string + f" using acronyms in '{acronyms}'"
    if bibliography is not None:
        info_string = info_string + f" and bibliography from '{bibliography}'"

    print(info_string)

    if toc:
        markdown_text = text_from_table_of_contents(input_file)
    else:
        markdown_text = text_from_file(input_file)

    markdown = create_markdown(
        acronyms=acronyms, bibliography=bibliography, chapters=chapters, toc=print_toc,
    )
    latex_text = markdown(markdown_text)

    with open(output, "w") as output_file:
        output_file.write(latex_text)

    if markdown_file_name is not None:
        with open(markdown_file_name, "w") as markdown_file:
            markdown_file.write(markdown_text)


if __name__ == "__main__":
    run()
