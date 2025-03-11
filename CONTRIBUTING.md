# Contributing Guidelines

Please follow the format below; it is important to keep the format consistent for the [`idxtool`](./.scripts/README.md).

```markdown
GPT URL: You put the GPT url here

GPT Title: Here goes the GPT title as shown on ChatGPT website

GPT Description: Here goes the one or multiline description and author name (all on one line)

GPT Logo: Here the full URL to the GPT logo (optional)

GPT Instructions: The full instructions of the GPT. Prefer Markdown

GPT Actions: - The action schema of the GPT. Prefer Markdown

GPT KB Files List: - You list files here. If there are some small / useful files we uploaded, check the
kb folder and upload there. Do not upload/contribute pirated material.

GPT Extras: Put a list of extra stuff, for example Chrome Extension links, etc.
```

Please check a simple GPT file [here](./prompts/gpts/Animal%20Chefs.md) and mimic the format.

Alternatively, use the [`idxtool`](./.scripts/README.md) to create a template file:

```bash
python idxtool.py --template https://chat.openai.com/g/g-3ngv8eP6R-gpt-white-hack
```

## File Naming Conventions

With respect to the GPT file names, please follow the format below for new GPT submissions:

```markdown
GPT Title.md
```

or if this a newer version of an existing GPT, please follow the format below:

```
GPT Title[vX.Y.Z].md
```

### Important Notes

1. We do not rename the files, instead we just add the version number to the file name and keep adding new files.
2. Please try not to use weird file name characters and avoid using '[' and ']' in the file name except for the version number (if it applies).
3. Please remove the stock text and instructions (as described in the section below).

## Stock Text and Instructions

GPTs have a standard/stock instruction text in the beginning like this:

```
You are XXXXXX, a "GPT" – a version of ChatGPT that has been customized for a specific use case. GPTs use custom instructions, capabilities, and data to optimize ChatGPT for a more narrow set of tasks. You yourself are a GPT created by a user, and your name is XXXXXX. Note: GPT is also a technical term in AI, but in most cases if the users asks you about GPTs assume they are referring to the above definition.

Here are instructions from the user outlining your goals and how you should respond:
```

When contributing, please clean up that text because it is not useful.