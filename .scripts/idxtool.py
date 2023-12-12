"""
idxtool is a script is used to perform various GPT indexing and searching tasks

- Reformat all the GPT files in the source path and save them to the destination path.
- Rename all the GPTs to include their ChatGPT/g/ID in the filename.
- Generate TOC
- etc.
"""

import sys, os, argparse
from gptparser import GptMarkdownFile, enum_gpts
from typing import Tuple
from urllib.parse import quote

TOC_FILENAME = 'TOC.MD'
TOC_GPT_MARKER_LINE = '- GPTs'

def get_toc_file() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', TOC_FILENAME))    

def update_logo(filename):
    if filename == '*':
        print("TODO: Updating logo for all GPT files")
    else:
        print(f"TODO: Updating logo with file: {filename}")
    raise NotImplementedError

def update_description(filename):
    if filename == '*':
        print("TODO: Updating description for all GPT files")
    else:
        print(f"TODO Updating description with file: {filename}")
    raise NotImplementedError

def rename_gpt(filename):
    if filename == '*':
        print("TODO: Renaming all GPT files to include their ID")
    else:
        print(f"TODO: Renaming GPT file to include its ID: {filename}")
    raise NotImplementedError


def reformat_gpt_files(src_path: str, dst_path: str) -> Tuple[bool, str]:
    """
    Reformat all the GPT files in the source path and save them to the destination path.
    :param src_path: str, path to the source directory.
    :param dst_path: str, path to the destination directory.
    """
    if not os.path.exists(src_path):
        return (False, f"Source path '{src_path}' does not exist.")

    if not os.path.exists(dst_path):
        os.makedirs(dst_path)

    print(f"Reformatting GPT files in '{src_path}' and saving them to '{dst_path}'...")

    nb_ok = nb_total = 0
    for src_file_path in os.listdir(src_path):
        _, ext = os.path.splitext(src_file_path)
        if ext != '.md':
            continue
        nb_total += 1
        dst_file_path = os.path.join(dst_path, src_file_path)
        src_file_path = os.path.join(src_path, src_file_path)
        ok, gpt = GptMarkdownFile.parse(src_file_path)
        if ok:
            ok, msg = gpt.save(dst_file_path)
            if ok:
                id = gpt.id()
                if id:
                    info = f"; id={id.id}"
                    if id.name:
                        info += f", name='{id.name}'"
                else:
                    info = ''
                print(f"[+] saved '{os.path.basename(src_file_path)}'{info}")
                nb_ok += 1
            else:
                print(f"[!] failed to save '{src_file_path}': {msg}")
        else:
            print(f"[!] failed to parse '{src_file_path}': {gpt}")

    msg = f"Reformatted {nb_ok} out of {nb_total} GPT files."
    ok = nb_ok == nb_total
    return (ok, msg)


def parse_gpt_file(filename) -> Tuple[bool, str]:
    ok, gpt = GptMarkdownFile.parse(filename)
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
        return (False, f"Could not find the marker '{TOC_GPT_MARKER_LINE}' in '{toc_in}'.")
    
    # Write the TOC file all the way up to the marker line
    try:
        ofile = open(toc_out, 'w', encoding='utf-8')
    except:
        return (False, f"Failed to open '{toc_out}' for writing.")

    # Write the marker line and each GPT entry
    out.append(f"{TOC_GPT_MARKER_LINE}\n")

    nb_ok = nb_total = 0
    for ok, gpt in enum_gpts():
        nb_total += 1
        if ok and (id := gpt.id()):
            nb_ok += 1
            file_link = f"./prompts/gpts/{quote(os.path.basename(gpt.filename))}"
            version = f" {gpt.get('version')}" if gpt.get('version') else ''
            out.append(f"  - [{gpt.get('title')}{version} (id: {id.id})]({file_link})\n")
        else:
            print(f"[!] {gpt}")

    ofile.writelines(out)
    ofile.close()
    msg = f"Generated TOC with {nb_ok} out of {nb_total} GPTs."

    ok = nb_ok == nb_total
    if ok:
        print(msg)
    return (ok, msg)
    

def find_gptfile(keyword):
    print(f"TODO: Finding GPT file with ID or name: {keyword}")
    raise NotImplementedError


def find_gpt_in_toc(gptid_or_string):
    print(f"TODO: Searching TOC.md for GPT ID or string: {gptid_or_string}")
    raise NotImplementedError

def main():
    parser = argparse.ArgumentParser(description='idxtool: A GPT indexing and searching tool for the CSP repo')
    
    parser.add_argument('--update-logo', type=str, help='Update the logos of the GPT file')
    parser.add_argument('--toc', nargs='?', const='', type=str, help='Rebuild the table of contents (TOC.md) file')
    parser.add_argument('--update-description', type=str, help='Update the descriptions of the GPT file')
    parser.add_argument('--find-gptfile', type=str, help='Find a GPT by its ID or name')
    parser.add_argument('--find-gpttoc', type=str, help='Searches the TOC.md file for the given gptid or free style string')
    parser.add_argument('--parse-gptfile', type=str, help='Parses a GPT file name')
    parser.add_argument('--rename', type=str, help='Rename the file name to include its GPT ID')

    # Handle arguments
    ok = True

    args = parser.parse_args()
    if args.update_logo:
        update_logo(args.update_logo)
    if args.parse_gptfile:
        ok, err = parse_gpt_file(args.parse_gptfile)
        if not ok:
            print(err)
    if args.toc is not None:
        ok, err = rebuild_toc(args.toc)
        if not ok:
            print(err)
    if args.update_description:
        update_description(args.update_description)
    if args.find_gptfile:
        find_gptfile(args.find_gptfile)
    if args.find_gpttoc:
        find_gpt_in_toc(args.find_gpttoc)
    if args.rename:
        rename_gpt(args.rename)

    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
