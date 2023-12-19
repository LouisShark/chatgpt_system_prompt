"""
'oneoff.py' is a script that performs one-off operations on the GPT files

- Reformat all the GPT files in the source path and save them to the destination path.

"""

from gptparser import GptMarkdownFile
from typing import Tuple
import os

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
