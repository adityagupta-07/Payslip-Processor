# Payslip Processor

A desktop tool that turns a single payroll Excel sheet into individual employee payslips (DOCX and PDF) and one merged master PDF, using a simple point and click interface.

No scripting, no command line. Select the Excel file, click a button, and collect the finished payslips.


## What it does

1. You give it a payroll Excel workbook containing a block of data per employee.
2. It reads every employee's details out of the sheet.
3. It fills each one into a Word template (payslip layout).
4. It converts every payslip to PDF.
5. It stitches all the individual PDFs into a single master PDF for the month.

All output, the DOCX files, the individual PDFs, and the master PDF, is organized automatically into folders you can open with one click.


## Features

- 🖱️ **Simple GUI**: browse for a file, click once, done. No terminal required.
- 🧵 **Non blocking processing**: the app stays responsive while it works, with a live status indicator.
- 📄 **Two payslip layouts**: automatically picks a template depending on whether the employee has an Employee ID.
- 💰 **Automatic currency formatting**: salary figures are formatted as `Rs. X,XXX.XX`.
- 📦 **One click access to results**: an "Open File Location" button appears as soon as processing finishes.
- 🧾 **Master PDF**: every individual payslip is merged into one file named `Payslip - <Month> <Year>.pdf`, ready to archive or share.
- 🧹 **Clean runs**: output folders are cleared automatically at the start of each run so results never mix between months.
- ⚠️ **Clear error reporting**: if something goes wrong, you get a readable error message instead of a crash.


## Requirements

- **Windows**, with **Microsoft Word installed** (used to preserve formatting when converting DOCX to PDF)
- **Python 3.9+**
- Python packages listed in `requirements.txt`:
  - `openpyxl`
  - `docxtpl`
  - `docx2pdf`
  - `pymupdf`

Install dependencies:

```bash
pip install -r requirements.txt
```


## Project structure

```
Payslip Processor/
├── data/
│   ├── input/
│   │   └── payslip_may.xlsx        # Source payroll workbook (per run input)
│   └── output/                     # Generated each run, cleared automatically beforehand
│       ├── docx/                   # Individual DOCX payslips
│       └── pdf/
│           ├── individual/         # Individual PDF payslips
│           ├── master/             # Final merged PDF for the month
│           └── protected_individuals/
├── docs/
│   ├── algorithm.md                # Step by step technical description of the pipeline
│   └── architecture.md
├── src/
│   └── payslip_processor/
│       ├── __init__.py             # Package entry point, exposes the public API
│       ├── config.py               # Defines the employee data structure
│       ├── directories.py          # Central place for all input, output, and template paths
│       ├── excel_reader.py         # Loads the Excel file, finds matching rows
│       ├── employee_parser.py      # Locates employee blocks and extracts field values
│       ├── docx_generator.py       # Fills templates and generates DOCX payslips
│       ├── pdf_converter.py        # Converts DOCX to PDF and merges into a master PDF
│       ├── file_utils.py           # Clears output folders before each run
│       ├── gui.py                  # GUI window, file picker, threading, status updates
│       └── main.py                 # Orchestrates the full pipeline
├── templates/
│   ├── docx/
│   │   ├── template_id.docx        # Used when Employee ID is present
│   │   └── template_no_id.docx     # Used when Employee ID is blank
│   └── pdf/                        # Reference PDF versions of the templates
├── .gitignore
├── README.md                       # You are here
└── requirements.txt
```

All paths used by the pipeline are centralized in `directories.py`, so moving folders around only requires updating that one file.


## How to use

1. **Run the app**

   ```bash
   python -m src.payslip_processor.main
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

- A specific marker cell signals the start of an employee's block, and another marker cell signals its end.
- Within the block, each field (for example `Employee Name`, `Basic Salary`, `PAN`, `Bank Name`) appears as a label in one cell, with its value in the **cell immediately to the right**.
- The full list of recognized fields is defined in `config.py`.

The sheet can contain any number of employee blocks. One payslip is generated per block found.


## Output

For each employee, you'll get:

- A DOCX payslip named `<Employee_Name>_<Month>_<Year>[_<Employee ID>].docx`
- A matching PDF with the same name

Plus one combined file:

- `Payslip - <Month> <Year>.pdf`, every employee's payslip merged into a single document, in the same order they were found in the sheet.


## Troubleshooting

| Problem | Likely cause |
|---|---|
| "Failed!" popup on every run | Excel file doesn't match the expected block layout, or a field is misspelled |
| PDFs look unformatted or broken | Microsoft Word isn't installed, or Word is being used by another process during conversion |
| "Open File Location" doesn't work | The app currently uses `os.startfile`, which is Windows only |
| Wrong template used for an employee | Check whether their `Employee ID` cell is genuinely blank vs. containing whitespace |


## Notes for developers

See [`docs/algorithm.md`](./docs/algorithm.md) for a detailed, step by step breakdown of exactly how the pipeline processes the spreadsheet, generates documents, and merges PDFs. See [`docs/architecture.md`](./docs/architecture.md) for how the modules fit together.