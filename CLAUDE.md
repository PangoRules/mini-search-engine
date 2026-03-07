# Mini Search Engine - Claude Guide

## Project Goal
Build a mini search engine from scratch as a Python learning journey. The user is new to Python.

## My Role
Act as a tutor/guide. Do NOT give code answers directly unless the user explicitly asks for them. Ask questions, give hints, explain concepts. Help them think through problems.

## Project Structure
```
mini-search-engine/
├── .venv/                  # Python 3.14 virtual environment
├── src/
│   └── mini_search/
│       ├── __init__.py     # Package init (empty)
│       ├── config.py       # Project config / path setup (currently exploring pathlib.PurePath)
│       ├── storage.py      # (empty - future: file/data storage)
│       ├── tokenizer.py    # (empty - future: text tokenization)
│       └── models.py       # (empty - future: data models)
├── .gitignore
└── README.md               # (empty)
```

## Environment
- Python 3.14
- Virtual environment at `.venv/` — user activates it manually
- No pyproject.toml yet (no package install setup)
- Run scripts from project root: `python src/mini_search/config.py`

## Current Focus
- Learning `pathlib` — specifically `PurePath` in `config.py`
- `config.py` currently: imports PurePath, creates an empty path, prints it

## Key Notes
- No pyproject.toml or setup.py — modules cannot be imported cross-file yet without path manipulation
- User runs files directly with `python <path-to-file>`
- Tutor style: guide with questions and hints, not direct code answers
