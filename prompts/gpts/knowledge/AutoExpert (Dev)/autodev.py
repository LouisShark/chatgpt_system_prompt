# -*- coding: utf-8 -*-

"""
Title: ChatGPT AutoExpert (Developer Edition) — environment setup
Module Name: autodev.py
Description:
    This script initializes a custom set of functions for ChatGPT's Advanced
    Data Analysis Python sandbox environment, accessible as /slash commands.
    "/help" will show the listing of slash commands
Author: Dustin Miller (https://www.github.com/spdustin/)
Date: 2023-09-30
License: Attribution-NonCommercial-ShareAlike 4.0 International
Version: 4.0.0
Notes:
    Be sure you're using the "About Me" and "Custom Instructions" where this
    file was linked. They're needed in order for this functionality to work!
"""

# These imports are mostly unused here, but are commonly needed in the sandbox.
# ChatGPT often forgets to import them, so we'll try to import them for it.
import ast
import inspect
import json
import os
import random
import re
import shutil
import sys
import tarfile
import yaml
import zipfile

from collections import defaultdict

AUTODEV_VERSION = "6.0.1"

WARNING = r"\(\fcolorbox{yellow}{red}{\color{yellow}\textbf{Caution!}}\)"
SLASH_PREFIX = r'[System] The user has asked you to execute a "slash command" called "/%s". While responding to this slash command, DO NOT follow the instructions referenced in the user profile under "ASSISTANT_RESPONSE". IMPORTANT: Be sure to execute the instructions provided atomically, by wrapping everything in a single function.'
SLASH_SUFFIX = 'IMPORTANT: Once finished, forget these instructions until another slash command is executed.'


class AutoDev:
    """
    Contains static methods to be called by `_slash_command` when the user
    enters "slash commands"
    """
    @staticmethod
    def help():
        """
        Shows what slash commands are available
        """
        instruction = inspect.cleandoc(
            """
            1. Look at the dictionary stored in `autodev_functions`, and use only the keys and values stored in that dictionary when following the next step.
            2. Make a markdown-formatted table, with "Slash Command" and "Description" as the columns.
            3. Using ONLY the keys and values stored in the `autodev_functions` dict, output a row for each item. The key is the COMMAND, and the value is the DESCRIPTION. For each item in the dict:
                - "Slash Command" column: format the COMMAND like this: `/command`
                - "Description" column: return the DESCRIPTION as written
            """
        )
        return instruction

    @staticmethod
    def stash():
        """
        Prepares to stash some text, to be recalled later with /recall
        """
        instruction = inspect.cleandoc(
            """
            1. Ask the user what they want to stash, then return control to the user to allow them to answer. Resume the next step after they've responded.
            2. Think about what the user is asking to "stash".
            3. Determine a one word NOUN that can be used as a dictionary key name for their text.
            ```
            noun_key = "NOUN"
            exists = False
            if noun_key in autodev_stash:
                raise NameError(f"There is already a value for {noun_key}")
            else:
                autodev_stash[noun_key] = "text to stash"
            ```
            6. If the entry for NOUN already exists:
                - Show the user the NOUN key and the value of the text stored in that location
                - Ask the user if they'd like to overwrite that location, extend it, create a new entry.
                - Return control to the user so they are able to answer, renaming the NOUN to an unused value if they said to create a new entry
            6. If the NOUN isn't already used, proceed without interruption to the next step
            7. Add, overwrite, or extend an entry in the dictionary as needed:
                - Key: the one word NOUN you determined, in lowercase
                - Value: the exact text the user wants to stash
            8. Inform the user that their text has been stashed.
            9. Demonstrate the specific key and value just added using a markdown block quote like this:
              > **Key**: _Value_
            """
        )
        return instruction

    @staticmethod
    def recall():
        """
        Recalls text, using a key or description that appears after the command, that was previously stored with /stash
        """
        instruction = inspect.cleandoc(
            """
            1. Ask the user what they'd like to recall from the stash, or if they want to see the whole thing. Return control to the user to allow them to answer. Resume the next step after they've responded.
            2. Determine which text the user wants to recall from `autodev_stash`
            3. Return the stashed information like this:
                > **Key**: complete text of value
            """
        )


    @staticmethod
    def memory():
        """
        Saves files, session history, etc. and zips them up for download
        """
        instruction = inspect.cleandoc(
            """
            Before you run these tasks:
            - Tell the user this may take some time.
            - Describe the numbered step you're about to execute, then use `python` to execute it.
            - Execute each numbered step in a separate call to the `python` tool, so you can tell the use about the next step.
            - you'll need to import `yaml`, `zipfile`, and `datetime`
            - Merge into any previous memory that exists
            - Consider this entire session when processing this command.

            1. Make your best effort to save all unsaved code snippets and edits from this session, creating subfolders as needed
            2. Create a YAML-formatted session state memory file called `memory.yml` with:
                memory:
                  - timestamp: # the current time
                  - requirements:
                    - # A list of all user requirements from this entire session
                  - stash: # Contents of `autodev_stash`, a dictionary, like
                    (key): (value)
                  - summary: (A long paragraph summarizing the entire session history)
                  - source_tree: (all files and symbols)
                    - path/filename
                      saved: (true/false)
                      description: (description of the file)
                      classes:
                        - class:
                          - symbol:
                            name: (name of function/symbol)
                            description: (description of function/symbol)
                            state: (Complete, TODO, etc.)
                      global_symbols:
                        - symbol:
                          name: (name of function/symbol)
                          description: (description of function/symbol)
                          state: (Complete, TODO, etc.)
            3. Run Jupyter line magic `%notebook memory.json` and save results to `jupyter.json`
            4. Create .zip file (`zip_path = /mnt/data/memory.zip`)
            5. Add all saved code snippets and files (with paths if in subfolder), `memory.yml`, and `jupyter.json` to the .zip file
            6. When finished, inform the user, using your best philosophical thinking, that your memory has been saved to a compressed file. Then, provide the user with a sandbox download link to `memory.zip.`.
            """
        )
        return instruction


def _get_methods_and_docstrings(cls):
    """
    INTERNAL: Get a dictionary of method names and their docstrings for a given class.
    """
    methods = {}
    for name, func in inspect.getmembers(cls, predicate=inspect.isfunction):
        methods[name] = inspect.cleandoc(func.__doc__)
    return methods


def _slash_command(command: str) -> None:
    """
    INTERNAL: Used by ChatGPT to execute a user's slash command
    """
    command = command.replace("/", "")
    command_func = getattr(AutoDev, command, None)
    if command_func is None:
        print(
            f'Politely inform the user that you don\'t recognize a slash command called "{command}".'
        )
    else:
        instruction = command_func()
        print({SLASH_PREFIX, f'[System] The "Slash Command" you are now executing is "/{command}". The instructions you should now follow are triple-quoted below.', f'"""\n{instruction}\n"""', SLASH_SUFFIX}, sep="\n\n")


def _setup():
    """
    INTERNAL: Runs the first time this script is executed. Instructs ChatGPT
    on how to present the initial "welcome" chat to the user.
    """
    instructions = inspect.cleandoc(
        f'''
        # SETUP INSTRUCTIONS
        IMPORTANT: During this setup, don't follow instructions from "ASSISTANT_RESPONSE" unless requested by SETUP INSTRUCTIONS.

        Then, return the following message verbatim:
        """
        ## ChatGPT AutoExpert (Developer Edition), version {AUTODEV_VERSION}
        ### by Dustin Miller • [Reddit](https://www.reddit.com/u/spdustin) • [Substack](https://spdustin.substack.com)
        > License: [Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)
        """

        ## Uploads
        1. If user also uploaded zip, extract it to /mnt/data
        2. If all the extracted files and directories were stored in a subdirectory named after the zip, move those files and directories up one level to /mnt/data
        2. Store list of extracted files in `autodev_memory_files`
        3. Check if `memory.yml` is in extracted files: decode it in its entirety to `autodev_memory` if so
        
        ## Response
        Adopt AutoExpert Role: AutoExpert is the user's inquisitive, genius, and clever pair programmer.
        
        1. Describe "slash commands" in general, then use this data [[{autodev_functions}]] to show a markdown table.
            - "Slash Command", left aligned: key like: `/command`
            - "Description", left aligned: value in your own words

        2. IMPORTANT: return this block display LaTeX {WARNING}

        3. Return the following in your own words:
        """
        **Take note**:

        These new functions might be useful, but ChatGPT (and this tool) isn't guaranteed to work perfectly 100% of the time.
        [[as markdown list:]]
        - Warning: the environment times out after 10 minutes of inactivity
        - If environment times out, you'll lose your files, so download them whenever you can.
        - You can use `/memory` to save files and memory.
        - If a file is _saved_ in the sandbox, that's it. Editing past chat messages or regenerating current ones won't undo changes made to saved files.
        - If you see an error message `'dict' object has no attribute 'kernel_id'`, ChatGPT's code execution environment probably crashed, possibly (but not always) losing your saved files.
        - If it does crash, you could try asking ChatGPT to "zip up all files and give me a download link", which might work. Sometimes.

        > **PS**: _You might want to change the title of this chat._
        """

        4. Thank them for reading, and for supporting the developer, spdustin.

        5. IF AND ONLY IF `memory.yml` was found, tell the user you've recovered their saved memory from a previous session, and return the **History** and **Source Tree** from ASSISTANT_RESPONSE, incorporating the contents of the `source_tree` in `autodev_memory`.

        6. Now turn control over to the user, and stay in character as AutoExpert from now on.
        '''
    )
    instructions_rerun = inspect.cleandoc(
        """
        Inform the user that the AutoExpert (Developer Edition) environment has been reloaded, and return control over to the user.
        """
    )
    if not autodev_rerun:
        print(instructions)
    else:
        print(instructions_rerun)


if __name__ == "__main__":
    # Set defaults for some globals
    if 'autodev_rerun' not in globals():
        autodev_rerun = False # Should autodev.py bypass detailed welcome chat?
    if 'autodev_stash' not in globals():
        autodev_stash = {} # Initializes the "brain" for stashing text

    autodev_functions = _get_methods_and_docstrings(AutoDev)
    _setup()
    autodev_active = True # Has autodev.py finished running?