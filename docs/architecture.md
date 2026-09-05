# Payslip Processor — Architecture

How the modules in `src/payslip_processor/` fit together. For the step-by-step processing logic within each module, see [`algorithm.md`](./algorithm.md).

## Module overview

| Module | Responsibility |
|---|---|
| `main.py` | Orchestrates the full pipeline for a single run: load workbook → locate employee blocks → clear output → extract details → generate DOCX → convert to PDF → merge into master PDF. |
| `gui.py` | Builds the Tkinter window, wires up the Browse/Exit/Open File Location buttons, runs `main()` on a background thread, and reports success/failure back to the UI. |
| `directories.py` | Single source of truth for every path the app touches — templates, DOCX output, individual PDFs, master PDF — resolved with `pathlib` relative to the project root. No other module hardcodes a path. |
| `config.py` | Defines the employee data structure (the dict "shape" every employee record is built from), including nested `duplicates` and `specials` fields. |
| `excel_reader.py` | Opens the input workbook with `openpyxl` (`data_only=True`) and returns the active worksheet. |
| `employee_parser.py` | Scans the worksheet for employee block markers ("EMPLOYEE INFORMATION" / "Net Salary Paid"), then extracts each field's value into a fresh copy of the `config.py` dict shape per block. |
| `docx_generator.py` | Maps extracted employee fields to template placeholder keys, chooses the correct template (with/without Employee ID), and renders each DOCX payslip via `docxtpl`. |
| `pdf_converter.py` | Converts the generated DOCX files to PDF (via `docx2pdf`, which shells out to MS Word) and merges all individual PDFs into one master PDF using `pymupdf`. |
| `file_utils.py` | Clears and recreates the output folders at the start of each run, so results never mix between months. |
| `__init__.py` | Package entry point; exposes the public API for the modules above. |

## Data flow

```
excel_reader.py          → worksheet object
        │
        ▼
employee_parser.py       → list[employee dict]  (shape defined in config.py)
        │
        ▼
docx_generator.py        → placeholder map → rendered .docx per employee
        │
        ▼
pdf_converter.py          → individual .pdf per employee → merged master .pdf
```

Every module above reads its input/output locations from `directories.py` rather than constructing paths itself. `file_utils.py` is invoked once, early in `main.py`, before any employee data is built — this guarantees a clean slate for every run.

## Threading model

`gui.py` owns the only thread that touches Tkinter widgets. `main()` — and everything it calls (`excel_reader`, `employee_parser`, `docx_generator`, `pdf_converter`, `file_utils`) — runs entirely on a background thread. Results are marshalled back to the main thread as a single "done" or "failed" callback, so the UI never blocks and never gets touched from the worker thread directly.

## Why this split exists

- **`directories.py` is isolated** so that moving folders around, or porting the app off Windows, only requires touching one file.
- **`config.py` is isolated** from `employee_parser.py` so the *shape* of an employee record (what fields exist) is decoupled from *how* those fields get found in the sheet.
- **`pdf_converter.py` keeps two conversion strategies** (Word-dependent and Word-independent) side by side, so switching away from the MS Word dependency later is a one-line change in `main.py`, not a rewrite.
- **`gui.py` has no business logic** — it only knows how to call `main()` and update three widgets based on the result. All actual payroll logic lives in modules that don't know a GUI exists, which keeps the pipeline testable from the command line if ever needed.