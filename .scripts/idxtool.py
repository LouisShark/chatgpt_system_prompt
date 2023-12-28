"""
idxtool is a script is used to perform various GPT indexing and searching tasks

- Find a GPT file by its ID or full ChatGPT URL or via a file containing a list of GPT IDs.
- Rename all the GPTs to include their ChatGPT/g/ID in the filename.
- Generate TOC
- etc.
"""

import sys, os, argparse
from typing import Tuple
from urllib.parse import quote

import gptparser
from gptparser import enum_gpts, parse_gpturl, enum_gpt_files, get_prompts_path

TOC_FILENAME = 'TOC.md'
TOC_GPT_MARKER_LINE = '- GPTs'

def get_toc_file() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', TOC_FILENAME))

def rename_gpts():
    effective_rename = nb_ok = nb_total = 0

    for ok, gpt in enum_gpts():
        nb_total += 1
        if not ok or not (id := gpt.id()):
            print(f"[!] {gpt.filename}")
            continue
        # Skip files with correct prefix
        basename = os.path.basename(gpt.filename)
        if basename.startswith(f"{id.id}_"):
            nb_ok += 1
            continue
        effective_rename += 1

        # New full file name with ID prefix
        new_fn = os.path.join(os.path.dirname(gpt.filename), f"{id.id}_{basename}")
        print(f"[+] {basename} -> {os.path.basename(new_fn)}")
        if os.system(f"git mv \"{gpt.filename}\" \"{new_fn}\"") == 0:
            nb_ok += 1
            continue

        # If git mv failed, then try os.rename
        try:
            os.rename(gpt.filename, new_fn)
            nb_ok += 1
            continue
        except OSError as e:
            print(f"Rename error: {e.strerror}")

    msg = f"Renamed {nb_ok} out of {nb_total} GPT files."
    ok = nb_ok == nb_total
    if effective_rename == 0:
        msg = f"All {nb_total} GPT files were already renamed. No action taken."
        print(msg)

    return (ok, msg)


def parse_gpt_file(filename) -> Tuple[bool, str]:
    ok, gpt = gptparser.GptMarkdownFile.parse(filename)
    if ok:
        file_name_without_ext = os.path.splitext(os.path.basename(filename))[0]
        dst_fn = os.path.join(
            os.path.dirname(filename),
            f"{file_name_without_ext}.new.md")
        gpt.save(dst_fn)
    else:
        print(gpt)

    return (ok, gpt)


def rebuild_toc(toc_out: str = '') -> Tuple[bool, str]:
    """
    Rebuilds the table of contents (TOC.md) file by reading all the GPT files in the prompts/gpts directory.
    """
    if not toc_out:
        print(f"Rebuilding Table of Contents (TOC.md) in place")
    else:
        print(f"Rebuilding Table of Contents (TOC.md) to '{toc_out}'")

    toc_in = get_toc_file()
    if not toc_out:
        toc_out = toc_in

    if not os.path.exists(toc_in):
        return (False, f"TOC File '{toc_in}' does not exist.")


    # Read the TOC file and find the marker line for the GPT instructions
    out = []
    marker_found = False
    with open(toc_in, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith(TOC_GPT_MARKER_LINE):
                marker_found = True
                break
            else:
                out.append(line)
    if not marker_found:
        return (False, f"Could not find the marker '{TOC_GPT_MARKER_LINE}' in '{toc_in}'. Please revert the TOC file and try again.")

    # Write the TOC file all the way up to the marker line
    try:
        ofile = open(toc_out, 'w', encoding='utf-8')
    except:
        return (False, f"Failed to open '{toc_out}' for writing.")

    # Write the marker line and each GPT entry
    out.append(f"{TOC_GPT_MARKER_LINE}\n")

    nb_ok = nb_total = 0
    gpts = []
    for ok, gpt in enum_gpts():
        nb_total += 1
        if ok:
            if gpt_id := gpt.id():
                nb_ok += 1
                gpts.append((gpt_id, gpt))
            else:
                print(f"[!] No ID detected: {gpt.filename}")
        else:
            print(f"[!] {gpt}")

    # Consistently sort the GPTs by ID and GPTs title
    def gpts_sorter(key):
        gpt_id, gpt = key
        version = f"{gpt.get('version')}" if gpt.get('version') else ''
        return f"{gpt.get('title')}{version} (id: {gpt_id.id}))"
    gpts.sort(key=gpts_sorter)

    for id, gpt in gpts:
        file_link = f"./prompts/gpts/{quote(os.path.basename(gpt.filename))}"
        version = f" {gpt.get('version')}" if gpt.get('version') else ''
        out.append(f"  - [{gpt.get('title')}{version} (id: {id.id})]({file_link})\n")

    ofile.writelines(out)
    ofile.close()
    msg = f"Generated TOC with {nb_ok} out of {nb_total} GPTs."

    ok = nb_ok == nb_total
    if ok:
        print(msg)
    return (ok, msg)

def make_template(url, verbose=True):
    """Creates an empty GPT template file from a ChatGPT URL"""
    if not (gpt_info := parse_gpturl(url)):
        msg = f"Invalid ChatGPT URL: '{url}'"
        if verbose:
            print(msg)
        return (False, msg)

    filename = os.path.join(get_prompts_path(), f"{gpt_info.id}_RENAMEME.md")
    if os.path.exists(filename):
        msg = f"File '{filename}' already exists."
        if verbose:
            print(msg)
        return (False, msg)

    with open(filename, 'w', encoding='utf-8') as file:
        for field, info in gptparser.SUPPORTED_FIELDS.items():
            if field == 'verif_status':
                continue
            if field == 'url':
                file.write(f"{gptparser.FIELD_PREFIX} {info.display}: {url}\n\n")
            elif field == 'instructions':
                file.write(f"{gptparser.FIELD_PREFIX} {info.display}:\n```markdown\n{info.display} here...\n```\n\n")
            elif field == 'logo':
                file.write(f"{gptparser.FIELD_PREFIX} {info.display}: <img ...>\n\n")
            else:
                file.write(f"{gptparser.FIELD_PREFIX} {info.display}: {info.display} goes here...\n\n")

    msg = f"Created template '{filename}' for URL '{url}'"
    if verbose:
        print(msg)
    return (True, msg)

def find_gptfile(keyword, verbose=True):
    """Find a GPT file by its ID or full ChatGPT URL
    The ID can be prefixed with '@' to indicate a file containing a list of GPT IDs.
    """
    keyword = keyword.strip()
    # Response file with a set of GPT IDs
    if keyword.startswith('@'):
        with open(keyword[1:], 'r', encoding='utf-8') as file:
            ids = set()
            for line in file:
                line = line.strip()
                # Skip comments
                if line.startswith('#'):
                    continue
                # If the line is a GPT URL, then extract the ID
                if gpt_info := parse_gpturl(line):
                    ids.add(gpt_info.id)
                    continue
                # If not a GPT URL, then it's a GPT ID
                ids.add(line)
    elif gpt_info := parse_gpturl(keyword):
        # A single GPT URL
        ids = {gpt_info.id}
    else:
        # A single GPT ID
        ids = {keyword}

    if verbose:
        print(f'Looking for GPT files with IDs: {", ".join(ids)}')
    matches = []
    for id, filename in enum_gpt_files():
        if id in ids:
            if verbose:
                print(filename)
            matches.append((id, filename))

    return matches


def main():
    parser = argparse.ArgumentParser(description='idxtool: A GPT indexing and searching tool for the CSP repo')

    parser.add_argument('--toc', nargs='?', const='', type=str, help='Rebuild the table of contents (TOC.md) file')
    parser.add_argument('--find-gpt', type=str, help='Find a GPT file by its ID or full ChatGPT URL')
    parser.add_argument('--template', type=str, help='Creates an empty GPT template file from a ChatGPT URL')
    parser.add_argument('--parse-gptfile', type=str, help='Parses a GPT file name')
    parser.add_argument('--rename', action='store_true', help='Rename the GPT file names to include their GPT ID')

    # Handle arguments
    ok = True

    args = parser.parse_args()
    if args.parse_gptfile:
        ok, err = parse_gpt_file(args.parse_gptfile)
        if not ok:
            print(err)
    elif args.toc is not None:
        ok, err = rebuild_toc(args.toc)
        if not ok:
            print(err)
    elif args.find_gpt:
        find_gptfile(args.find_gpt)
    elif args.template:
        make_template(args.template)
    elif args.rename:
        ok, err = rename_gpts()
        if not ok:
            print(err)

    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
