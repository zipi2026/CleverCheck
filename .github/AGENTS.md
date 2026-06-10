---
name: clevercheck-agent
user-invocable: false
description: "Workspace agent instructions for the CleverCheck Python backend. Answer users in Hebrew and generate documentation files in English when requested."
---

# CleverCheck Workspace Agent Instructions

This file helps AI coding agents understand the main structure and conventions of the CleverCheck repository.

## Core structure
- Backend code is under `server/`
- Main entry point: `server/app.py`
- Flask controllers live in `server/controllers/`
- Business logic lives in `server/services/`
- Repository layer lives in `server/repositories/`
- ORM models live in `server/models/`
- Local ML model is stored in `server/my_model/`
- Dependencies are listed in `server/requirements.txt`

## Run and context notes
- The app runs with `python server/app.py`
- Default Flask port is `5000`
- The app uses a local SentenceTransformer model and a SQL Server connection via `pyodbc`

## Agent behavior
- Answer user questions in Hebrew by default.
- When creating documentation, summaries, or reports, generate the file content in English.
- Keep responses short and actionable.
- Use exact file paths from the workspace when suggesting changes.
- Prefer minimal, non-invasive modifications that fit the existing Flask/SQLAlchemy style.

## Important conventions
- The project does not currently have a top-level README or `.github` customization files.
- The local model path `server/my_model/` should be preserved when working with grading or ML-related code.
- Avoid assuming a different DB type; the current code uses SQL Server and `pyodbc`.
