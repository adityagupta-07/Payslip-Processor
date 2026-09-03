# Payslip Processor

A desktop tool that turns a single payroll Excel sheet into individual employee payslips (DOCX + PDF) and one merged master PDF — with a simple point-and-click interface.

No scripting, no command line. Select the Excel file, click a button, and collect the finished payslips.


## What it does

1. You give it a payroll Excel workbook containing a block of data per employee.
2. It reads every employee's details out of the sheet.
3. It fills each one into a Word template (payslip layout).
4. It converts every payslip to PDF.
5. It stitches all the individual PDFs into a single master PDF for the month.

All output — the DOCX files, the individual PDFs, and the master PDF — is organized automatically into folders you can open with one click.


## Features

- 🖱️ **Simple GUI** — browse for a file, click once, done. No terminal required.
- 🧵 **Non-blocking processing** — the app stays responsive while it works, with a live status indicator.
- 📄 **Two payslip layouts** — automatically picks a template depending on whether the employee has an Employee ID.
- 💰 **Automatic currency formatting** — salary figures are formatted as `Rs. X,XXX.XX`.
- 📦 **One-click access to results** — an "Open File Location" button appears as soon as processing finishes.
- 🧾 **Master PDF** — every individual payslip is merged into one file named `Payslip - <Month> <Year>.pdf`, ready to archive or share.
- ⚠️ **Clear error reporting** — if something goes wrong, you get a readable error message instead of a crash.


## Requirements

- **Windows**, with **Microsoft Word installed** (used to preserve formatting when converting DOCX → PDF)
- **Python 3.9+**
- Python packages:
  - `openpyxl`
  - `docxtpl`
  - `docx2pdf`
  - `pymupdf`

Install dependencies:

```bash
pip install openpyxl docxtpl docx2pdf pymupdf
```


## Folder structure

```
Payslip Processor/
├── main.py                 # Entry point — launches the GUI
├── gui.py                  # GUI window, file picker, threading, status updates
├── excel_reader.py         # Loads the Excel file, finds matching rows
├── employee_parser.py      # Locates employee blocks and extracts field values
├── docx_generator.py       # Fills templates and generates DOCX payslips
├── pdf_converter.py        # Converts DOCX → PDF and merges into a master PDF
├── file_utils.py           # Clears output folders before each run
├── config.py                # Defines the employee data structure
├── Algorithm.md             # Step-by-step technical description of the pipeline
├── README.md                 # You are here
└── Files/
    ├── Templates/
    │   ├── Template_id.docx      # Used when Employee ID is present
    │   └── Template_no_id.docx   # Used when Employee ID is blank
    ├── Docs/                     # Generated individual DOCX payslips
    └── PDFs/
        ├── Individual PDFs/      # Generated individual PDF payslips
        └── Master PDF/           # Final merged PDF for the month
```

> The `Docs`, `Individual PDFs`, and `Master PDF` folders are cleared automatically at the start of every run — don't store anything else in them.


## How to use

1. **Run the app**

   ```bash
   python main.py
   ```

   A window titled **"Payslip Processor"** opens.

2. **Click "Browse"** and select the payroll Excel file (`.xlsx`).

3. **Wait for processing.** The status label will show:
   - `Processing...` while the pipeline runs
   - `Processed!` when it finishes successfully
   - `Failed!` (with an error popup) if something went wrong

4. **Click "Open File Location"** to jump straight to the folder containing the generated PDFs.

5. **Click "Exit"** to close the app.


## Excel file format

The input workbook needs one block per employee, structured like this:

- A cell containing the text **`EMPLOYEE INFORMATION`** marks the start of an employee's block.
- A cell containing the text **`Net Salary Paid`** marks the end of that block.
- Within the block, each field (e.g. `Employee Name`, `Basic Salary`, `PAN`, `Bank Name`, ...) appears as a label in one cell, with its value in the **cell immediately to the right**.
- The full list of recognized fields is defined in `config.py`.

The sheet can contain any number of employee blocks — one payslip is generated per block found.


## Output

For each employee, you'll get:

- A DOCX payslip named `<Employee_Name>_<Month>_<Year>[_<Employee ID>].docx`
- A matching PDF with the same name

Plus one combined file:

- `Payslip - <Month> <Year>.pdf` — every employee's payslip merged into a single document, in the same order they were found in the sheet.


## Troubleshooting

| Problem | Likely cause |
|---|---|
| "Failed!" popup on every run | Excel file doesn't have the expected `EMPLOYEE INFORMATION` / `Net Salary Paid` markers, or a field is misspelled |
| PDFs look unformatted or broken | Microsoft Word isn't installed, or Word is being used by another process during conversion |
| "Open File Location" doesn't work | The app currently uses `os.startfile`, which is Windows-only |
| Wrong template used for an employee | Check whether their `Employee ID` cell is genuinely blank vs. containing whitespace |


## Notes for developers

See [`Algorithm.md`](./Algorithm.md) for a detailed, step-by-step breakdown of exactly how the pipeline processes the spreadsheet, generates documents, and merges PDFs.