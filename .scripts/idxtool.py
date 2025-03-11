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
    Rebuilds the table of contents (TOC.md) file, generating only the Prompt Collections section
    that links to the TOC.md files in the prompts subdirectories.
    The TOC file is completely regenerated, not preserving any existing content.
    """
    if not toc_out:
        print(f"Rebuilding Table of Contents (TOC.md) in place")
    else:
        print(f"Rebuilding Table of Contents (TOC.md) to '{toc_out}'")

    toc_in = get_toc_file()
    if not toc_out:
        toc_out = toc_in

    # Generate new TOC content
    out = []
    out.append("# ChatGPT System Prompts - Table of Contents\n\n")
    out.append("This document contains a table of contents for the ChatGPT System Prompts repository.\n\n")

    # Add links to TOC.md files in prompts directory subdirectories
    prompts_base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'prompts'))
    if os.path.exists(prompts_base_path):
        prompt_dirs = []
        for dirname in os.listdir(prompts_base_path):
            dir_path = os.path.join(prompts_base_path, dirname)
            toc_path = os.path.join(dir_path, TOC_FILENAME)
            # Only include directories that have a TOC.md file
            if os.path.isdir(dir_path) and os.path.exists(toc_path):
                prompt_dirs.append(dirname)

        if prompt_dirs:
            out.append("## Prompt Collections\n\n")
            prompt_dirs.sort(key=str.lower)  # Sort alphabetically case-insensitive
            for dirname in prompt_dirs:
                # Create a relative link to the subdirectory TOC file
                link = f"./prompts/{dirname}/{TOC_FILENAME}"
                out.append(f"- [{dirname} Collection]({link})\n")

    # Combine into a single string
    new_content = ''.join(out)

    # Check if the file exists and if its content matches the new content
    if os.path.exists(toc_out):
        try:
            with open(toc_out, 'r', encoding='utf-8') as existing_file:
                existing_content = existing_file.read()
                if existing_content == new_content:
                    msg = f"TOC content unchanged, skipping write to '{toc_out}'"
                    print(msg)
                    return (True, msg)
        except Exception as e:
            print(f"Warning: Could not read existing TOC file: {str(e)}")

    # Content is different or file doesn't exist, write the new content
    try:
        with open(toc_out, 'w', encoding='utf-8') as ofile:
            ofile.write(new_content)
        msg = f"Generated TOC with Prompt Collections only."
        return (True, msg)
    except Exception as e:
        msg = f"Failed to write TOC file: {str(e)}"
        return (False, msg)

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

def generate_toc_for_prompts_dirs() -> Tuple[bool, str]:
    """
    Generates a single TOC.md file for each directory under prompts:
    - For the gpts directory, uses the original GPT-specific TOC generation logic.
    - For all other directories (including newly added ones), uses the generic recursive logic.

    This function automatically detects all subdirectories under prompts, ensuring future-proof
    extensibility without requiring code changes when new directories are added.
    """
    prompts_base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'prompts'))
    if not os.path.exists(prompts_base_path):
        return (False, f"Prompts directory '{prompts_base_path}' does not exist.")

    print(f"Generating TOC.md files for all directories under '{prompts_base_path}'")
    success = True
    messages = []

    # Dynamically discover all directories under prompts/
    try:
        all_dirs = [d for d in os.listdir(prompts_base_path)
                  if os.path.isdir(os.path.join(prompts_base_path, d))]
    except Exception as e:
        return (False, f"Error scanning prompts directory: {str(e)}")

    if not all_dirs:
        return (False, "No subdirectories found under prompts/")

    # Define which directory needs special GPT-specific handling
    # If you need to change the behavior, you only need to change this constant
    SPECIAL_DIR = "gpts"

    # Track if special directory was found and processed
    special_dir_processed = False

    def collect_files_recursively(dir_path, base_path=None):
        """
        Recursively collect all markdown files from a directory and its subdirectories.

        Args:
            dir_path: The current directory being processed
            base_path: The base directory path used for computing relative paths

        Returns:
            A list of tuples (relative_path, filename, title) where:
            - relative_path is the path relative to the base directory
            - filename is the name of the file
            - title is the extracted title from the file
        """
        if base_path is None:
            base_path = dir_path

        result = []

        try:
            items = os.listdir(dir_path)
        except (FileNotFoundError, PermissionError) as e:
            print(f"Warning: Could not access directory '{dir_path}': {str(e)}")
            return result

        for item in items:
            item_path = os.path.join(dir_path, item)

            # Skip TOC.md
            if item == TOC_FILENAME:
                continue

            try:
                if os.path.isfile(item_path) and item.endswith('.md'):
                    # Check if file exists and is readable
                    if not os.path.exists(item_path):
                        print(f"Warning: The file {item_path} does not exist")
                        continue

                    # Get relative path from the base directory to the file's directory
                    rel_dir_path = os.path.relpath(os.path.dirname(item_path), base_path)
                    if rel_dir_path == '.':
                        rel_dir_path = ''

                    # Extract title from the file
                    title = os.path.splitext(item)[0]
                    try:
                        with open(item_path, 'r', encoding='utf-8') as f:
                            first_line = f.readline().strip()
                            if first_line.startswith('# '):
                                title = first_line[2:].strip()
                    except Exception as e:
                        print(f"Warning: Could not read file '{item_path}': {str(e)}")

                    result.append((rel_dir_path, item, title))

                elif os.path.isdir(item_path):
                    # Recursively collect files from subdirectories using the same base_path
                    result.extend(collect_files_recursively(item_path, base_path))
            except Exception as e:
                print(f"Warning: Error processing '{item_path}': {str(e)}")

        return result

    def generate_gpts_toc(dir_path):
        """
        Generate TOC.md for gpts directory using the original GPT-specific logic.
        The file is completely regenerated, not preserving any existing content.

        Args:
            dir_path: Path to the gpts directory

        Returns:
            A tuple (success, message) indicating success/failure and a descriptive message
        """
        toc_path = os.path.join(dir_path, TOC_FILENAME)

        # Generate new content
        try:
            out = []
            out.append(f"# gpts - Table of Contents\n\n")

            # Count GPTs
            enumerated_gpts = list(enum_gpts())
            nb_ok = sum(1 for ok, gpt in enumerated_gpts if ok and gpt.id())

            out.append(f"## GPTs ({nb_ok} total)\n\n")

            nb_ok = nb_total = 0
            gpts = []
            for ok, gpt in enumerated_gpts:
                nb_total += 1
                if ok:
                    if gpt_id := gpt.id():
                        nb_ok += 1
                        gpts.append((gpt_id, gpt))
                    else:
                        print(f"[!] No ID detected: {gpt.filename}")
                else:
                    print(f"[!] {gpt}")

            # Consistently sort the GPTs by title
            def gpts_sorter(key):
                gpt_id, gpt = key
                version = f"{gpt.get('version')}" if gpt.get('version') else ''
                return f"{gpt.get('title', '').lower()}{version} (id: {gpt_id.id}))"  # Case-insensitive sort
            gpts.sort(key=gpts_sorter)

            for id, gpt in gpts:
                file_link = f"./{quote(os.path.basename(gpt.filename))}"
                version = f" {gpt.get('version')}" if gpt.get('version') else ''
                out.append(f"- [{gpt.get('title')}{version} (id: {id.id})]({file_link})\n")

            new_content = ''.join(out)

            # Check if the file exists and if its content matches the new content
            if os.path.exists(toc_path):
                try:
                    with open(toc_path, 'r', encoding='utf-8') as existing_file:
                        existing_content = existing_file.read()
                        if existing_content == new_content:
                            msg = f"TOC content unchanged for 'gpts', skipping write"
                            print(msg)
                            return (True, msg)
                except Exception as e:
                    print(f"Warning: Could not read existing gpts TOC file: {str(e)}")

            # Content is different or file doesn't exist, write the new content
            with open(toc_path, 'w', encoding='utf-8') as toc_file:
                toc_file.write(new_content)

            return (True, f"Generated TOC.md for 'gpts' with {nb_ok} out of {nb_total} GPTs.")
        except Exception as e:
            return (False, f"Error generating TOC.md for 'gpts': {str(e)}")

    # Process each top-level directory under prompts/
    for dirname in sorted(all_dirs, key=str.lower):  # Sort for consistent processing order
        dir_path = os.path.join(prompts_base_path, dirname)
        if not os.path.isdir(dir_path):
            messages.append(f"Directory '{dirname}' does not exist, skipping")
            continue

        # For gpts directory, use the original GPT-specific logic
        if dirname == SPECIAL_DIR:
            special_dir_processed = True
            ok, msg = generate_gpts_toc(dir_path)
            success = success and ok
            messages.append(msg)
            continue

        # For other directories, use the new recursive logic
        # Collect all markdown files in this directory and its subdirectories
        md_files = collect_files_recursively(dir_path)

        if not md_files:
            messages.append(f"No markdown files found in '{dirname}' or its subdirectories, skipping TOC generation")
            continue

        # Generate TOC.md for this directory
        toc_path = os.path.join(dir_path, TOC_FILENAME)
        try:
            # Generate new content
            out = []
            out.append(f"# {dirname} - Table of Contents\n\n")

            # Group files by their subdirectory
            files_by_dir = {}
            for rel_dir_path, filename, title in md_files:
                if rel_dir_path not in files_by_dir:
                    files_by_dir[rel_dir_path] = []
                files_by_dir[rel_dir_path].append((filename, title))

            # First list files in the root directory
            if '' in files_by_dir:
                root_files = files_by_dir['']
                root_files.sort(key=lambda x: x[1].lower())  # Sort alphabetically by title, case-insensitive

                for filename, title in root_files:
                    out.append(f"- [{title}](./{quote(filename)})\n")

                # Add a separator if we have subdirectories
                if len(files_by_dir) > 1:
                    out.append("\n")

            # Then list files in subdirectories
            subdirs = [d for d in files_by_dir.keys() if d != '']
            if subdirs:
                out.append("## Subdirectories\n\n")

                # Sort subdirectories alphabetically, case-insensitive
                subdirs.sort(key=str.lower)

                for subdir in subdirs:
                    # Write the subdirectory name as a heading
                    display_subdir = subdir.replace('\\', '/') # Ensure consistent path display
                    out.append(f"### {display_subdir}\n\n")

                    # Sort files in this subdirectory alphabetically by title, case-insensitive
                    subdir_files = files_by_dir[subdir]
                    subdir_files.sort(key=lambda x: x[1].lower())

                    for filename, title in subdir_files:
                        # Create a link with the correct relative path to the file
                        # Use os.path.join for correct path construction then replace backslashes for display
                        link_path = os.path.join(subdir, filename).replace('\\', '/')
                        out.append(f"- [{title}](./{quote(link_path)})\n")

                    out.append("\n")

            new_content = ''.join(out)

            # Check if the file exists and if its content matches the new content
            if os.path.exists(toc_path):
                try:
                    with open(toc_path, 'r', encoding='utf-8') as existing_file:
                        existing_content = existing_file.read()
                        if existing_content == new_content:
                            msg = f"TOC content unchanged for '{dirname}', skipping write"
                            print(msg)
                            messages.append(msg)
                            continue  # Skip to next directory
                except Exception as e:
                    print(f"Warning: Could not read existing TOC file for '{dirname}': {str(e)}")

            # Content is different or file doesn't exist, write the new content
            with open(toc_path, 'w', encoding='utf-8') as toc_file:
                toc_file.write(new_content)

            messages.append(f"Generated TOC.md for '{dirname}' with {len(md_files)} total files")

        except Exception as e:
            success = False
            messages.append(f"Error generating TOC.md for '{dirname}': {str(e)}")

    # Warn if special directory was expected but not found
    if not special_dir_processed and SPECIAL_DIR in all_dirs:
        messages.append(f"Warning: Special directory '{SPECIAL_DIR}' was found but could not be processed")

    result_message = "\n".join(messages)
    return (success, result_message)

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
        if args.toc:
            ok, err = rebuild_toc(args.toc)
        else:
            # First rebuild the main TOC file
            ok, msg = rebuild_toc('')
            print(msg)
            # Then generate TOC files for subdirectories under prompts/
            sub_ok, sub_err = generate_toc_for_prompts_dirs()
            ok = ok and sub_ok
            err = sub_err if not sub_ok else ""
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
