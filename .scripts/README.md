# idxtool

The `idxtool` is a GPT indexing and searching tool for the CSP repo (ChatGPT System Prompt).

Contributions to `idxtool` are welcome. Please submit pull requests or issues to the CSP repo for review.

## Command line

```
usage: idxtool.py [-h] [--toc [TOC]] [--find-gpt FIND_GPT] 
                  [--template TEMPLATE] [--parse-gptfile PARSE_GPTFILE] 
		  [--rename]

idxtool: A GPT indexing and searching tool for the CSP repo

options:
  -h, --help            show this help message and exit
  --toc [TOC]           Rebuild the table of contents (TOC.md) file
  --find-gpt FIND_GPT   Find a GPT file by its ID or full ChatGPT URL
  --template TEMPLATE   Creates an empty GPT template file from a ChatGPT URL
  --parse-gptfile PARSE_GPTFILE
                        Parses a GPT file name
  --rename              Rename the GPT file names to include their GPT ID
```

## Features

- Rebuild TOC: Use `--toc` to rebuild the table of contents (TOC.md) file.
- Find GPT File: Use `--find-gpt [GPTID or Full ChatGPT URL or a response file with IDs/URLs]` to find a GPT by its ID or URL.
- Rename GPT: Use `--rename` to rename all the GPTs to include their GPTID as prefix.
- Create a starter template GPT file: Use `--template [Full ChatGPT URL]` to create a starter template GPT file.
- Help: Use `--help` to display the help message and usage instructions.

## Example

To rebuild the [TOC.md](../TOC.md) file, run:

```bash
python idxtool.py --toc
```

To find a GPT by its ID, run:

```bash
python idxtool.py --find-gpt 3rtbLUIUO
```

or by URL:
  
```bash
python idxtool.py --find-gpt https://chat.openai.com/g/g-svehnI9xP-retro-adventures
```

Additionally, you can have a file with a list of IDs or URLs and pass it to the `--find-gpt` option:

```bash
python idxtool.py --find-gpt @gptids.txt
```

(note the '@' symbol).

The `gptids.txt` file contains a list of IDs or URLs, one per line:

```text
3rtbLUIUO
https://chat.openai.com/g/g-svehnI9xP-retro-adventures
#vYzt7bvAm
w2yOasK1r
waDWNw2J3
```


## License

This tool is open-sourced under the GNU General Public License (GPL). Under this license, you are free to use, modify, and redistribute this software, provided that all copies and derivative works are also licensed under the GPL.

For more details, see the [GPLv3 License](https://www.gnu.org/licenses/gpl-3.0.html).
