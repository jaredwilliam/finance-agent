# Project: Personal Finance Assistant

## Project Goal

The main goal is to build a Python application that reads a Python dictionary provided by the user and categorizes each transaction using the Anthropic API, and outputs the results into a new Python dictionary.

## Key Technologies

- **Language:** Python 3
- **Libraries:** `anthropic`

## Core Logic & Design

- The core logic revolves around a specific, structured prompt.
- The prompt template is found in `docs/prompt-template.md`.
- The AI's response for each transaction must be a Python dictionary object as defined in `docs/prompt-template.md`.

## Preferences

- Please follow SOLID principles for any classes you suggest.
- Prefer highly modular code with clear, self-documenting functions.
- The main script file will be named `finance_agent.py`.
