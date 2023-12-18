# idxtool

The `idxtool` is a GPT indexing and searching tool for the CSP repo (ChatGPT System Prompt).

## Command line

```
usage: idxtool.py [-h] [--update-logo UPDATE_LOGO] [--toc [TOC]]
                  [--update-description UPDATE_DESCRIPTION]
                  [--find-gptfile FIND_GPTFILE] [--find-gpttoc FIND_GPTTOC]
                  [--parse-gptfile PARSE_GPTFILE] [--rename RENAME]

idxtool: A GPT indexing and searching tool for the CSP repo

options:
  -h, --help            show this help message and exit
  --update-logo UPDATE_LOGO
                        Update the logos of the GPT file
  --toc [TOC]           Rebuild the table of contents (TOC.md) file
  --update-description UPDATE_DESCRIPTION
                        Update the descriptions of the GPT file
  --find-gptfile FIND_GPTFILE
                        Find a GPT by its ID or name
  --find-gpttoc FIND_GPTTOC
                        Searches the TOC.md file for the given gptid or free
                        style string
  --parse-gptfile PARSE_GPTFILE
                        Parses a GPT file name
  --rename              Rename all the GPT file names to include their GPT ID
```

## Features

- Update Logos: Use `--update-logo [filename]` to update the logos of the GPT file.
- Rebuild TOC: Use `--toc` to rebuild the table of contents (TOC.md) file.
- Update Descriptions: Use `--update-description [filename]` to update the descriptions of the GPT file.
- Find GPT File: Use `--find-gptfile [gptid or gpt name in quotes]` to find a GPT by its ID or name.
- Find GPT in TOC: Use `--find-gpttoc [gptid or string]` to search the TOC.md file for a given gptid or free style string.
- Rename GPT: Use `--rename` to rename all the GPTs to include their GPTID as prefix.
- Help: Use `--help` to display the help message and usage instructions.

## Usage

To use the tool, run the following command in your terminal with the appropriate arguments:

```bash
python idxtool.py [arguments]
```

Replace `[arguments]` with one of the feature commands listed above.

## Example

To update the logos of a GPT file named `example_gpt.json`, run:

```bash
python idxtool.py --update-logo example_gpt.json
```

## Installation

No additional installation is required. Ensure that you have Python installed on your system to run the tool.

## Contributing

Contributions to `idxtool` are welcome. Please submit pull requests or issues to the CSP repo for review.

## License

This tool is open-sourced under the GNU General Public License (GPL). Under this license, you are free to use, modify, and redistribute this software, provided that all copies and derivative works are also licensed under the GPL.

For more details, see the [GPLv3 License](https://www.gnu.org/licenses/gpl-3.0.html).
