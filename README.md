<!--
High-quality README for the Money Manager project.
Includes clear setup steps (PowerShell), reproducible-environment guidance, troubleshooting, and development notes.
-->

# Money Manager

Lightweight desktop app to track monthly budgets and expenses, built with CustomTkinter (modern Tkinter wrapper).

This repository contains the application source (`local app.py`) and a small JSON-based persistence layer. The project is intended to run on Windows and is developed using a local virtual environment named `venv`.

## Table of contents
- Project overview
- Quick start (PowerShell)
- Reproducible environments (pip vs conda)
- Troubleshooting (common failures and fixes)
- Development notes
- Files of interest
- License

---

## Project overview

`local app.py` provides a simple UI to:
- Set monthly budgets per category
- Add expenses with category and amount
- Save budgets and expenses to JSON files and show a brief report

The UI uses `customtkinter` for a modern look. Data is stored in the project folder in `expenditure.json` and monthly budget files named like `YYYY-MM.json`.

This README focuses on getting the app running reliably on Windows PowerShell and on keeping your environment reproducible.

## Quick start (PowerShell)

These commands will create a standard virtual environment called `venv`, install dependencies from `requirements.txt` and run the app. They assume you have a working CPython 3.12+ installation. Use exact quoting because the project path contains spaces.

1) Create + activate the venv and install dependencies

```powershell
Set-Location "E:\programming\python projects\money manager"
& "C:\Users\busyp\AppData\Local\Programs\Python\Python312\python.exe" -m venv .\venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r .\requirements.txt
```

2) Run the application

```powershell
# from the project root (after activation) or run directly with the venv python
python .\local app.py
# or (without activation)
& .\venv\Scripts\python.exe .\local app.py
```

If you prefer a one-liner to create the venv and install dependencies (PowerShell):

```powershell
& "C:\Users\busyp\AppData\Local\Programs\Python\Python312\python.exe" -m venv .\venv ; .\venv\Scripts\Activate.ps1 ; python -m pip install --upgrade pip setuptools wheel ; python -m pip install -r .\requirements.txt
```

## Reproducible environments — pip vs conda

- Pip (venv): good for lightweight apps. The included `requirements.txt` pins the working versions I used to get the app running locally. On Windows some packages (older pandas/matplotlib) may require a C compiler — see Troubleshooting below.
- Conda: recommended if you want guaranteed binary packages (no build tools required). If you want, I can add an `environment.yml` that sets up a conda environment with the pinned packages.

If you want me to add an `environment.yml`, say so and I will create it (conda/mamba-compatible).

## Troubleshooting (common issues)

- Problem: Python crashes immediately with "ModuleNotFoundError: No module named 'encodings'"
	- Cause: Python's sys.prefix or venv is misconfigured and the interpreter looks for the standard library in the project folder.
	- Fix: Use a working Python to recreate the venv. Example commands:

	```powershell
	# remove broken envs (if you are sure)
	Remove-Item -Recurse -Force .\env -ErrorAction SilentlyContinue
	Remove-Item -Recurse -Force .\venv -ErrorAction SilentlyContinue

	# create a fresh venv with a known-good Python
	& "C:\Users\busyp\AppData\Local\Programs\Python\Python312\python.exe" -m venv .\venv
	.\venv\Scripts\Activate.ps1
	python -m pip install --upgrade pip setuptools wheel
	python -m pip install -r .\requirements.txt
	```

- Problem: `pip install -r requirements.txt` fails building wheels for `pandas` or `matplotlib` with
	`error: Microsoft Visual C++ 14.0 or greater is required`
	- Cause: pip is trying to compile C extensions because a prebuilt wheel wasn't available for your Python/platform.
	- Fix options:
		1. Use the bundled prebuilt wheel versions (the `requirements.txt` in this repo points to versions that install as binary wheels for Python 3.12).
		2. Install Microsoft Visual C++ Build Tools (not recommended unless you need to compile).
		3. Use conda and install from conda-forge (recommended for data-heavy projects).

- Problem: PowerShell command syntax errors
	- Remember to use `&` before a quoted executable path and use semicolons `;` to separate statements in a single line. Avoid `||`/`&&` (these are not PowerShell operators).

## Development notes

- UI source: `local app.py` — contains the `ExpenseTrackerApp` class and the main Tk loop.
- Data files:
	- `expenditure.json` — all expenses stored by month.
	- `YYYY-MM.json` — monthly budgets stored per month.
- If you add new Python dependencies, update `requirements.txt` with pinned versions or run `python -m pip freeze > requirements.txt` to capture the full environment.

## Files of interest

- `local app.py` — app entrypoint and UI logic
- `requirements.txt` — pinned packages used during development
- `README.md` — this file

## Cleanup (fresh start)

```powershell
Remove-Item -Recurse -Force .\env -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force .\venv -ErrorAction SilentlyContinue
```

## If you want me to do more

- Create an `environment.yml` (conda) for easier reproducibility — I can add this.
- Add a small `setup.ps1` script to fully automate the Windows setup and run steps.
- Package the app as a single executable (pyinstaller) for distribution.

---

If anything should be clarified or you want more guide content (screenshots, UX notes, or packaging steps), tell me what you prefer and I'll update this README.
