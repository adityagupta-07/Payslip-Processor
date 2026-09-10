# Payslip Processor

This program is a tool that generates a separate password protected PDF payslip for each employee, as well as a master PDF containing the individual payslips of all employees, using an Excel payslip file containing the employees’ data as input.

## Project structure

```
├── docs
│   └── algorithm.md
├── Payslip_Processor
│   ├── src
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── delete_contents.py
│   │   ├── directories.py
│   │   ├── docx_generator.py
│   │   ├── employee_parser.py
│   │   ├── excel_reader.py
│   │   ├── gui.py
│   │   ├── password_protect_pdf.py
│   │   ├── pdf_converter.py
│   │   └── pipeline.py
│   └── __main__.py
├── README.md
└── requirements.txt
```

## Installation

Clone the repo, then install the dependencies:

```
pip install -r requirements.txt
```

Make sure the two Word templates (with ID and without ID) are stored in `templates/docx/` in root directory.

## Usage

Run the module and the GUI will open:

```
python -m Payslip_Processor
```

From there, click on Browse, choose your Excel file and let it process the payslips. After it finishes, it shows a button to open the output folder directly.

## Output

Everything gets stored inside `data/output`:

- *`docx/` stores the generated Word files per employee.
- *`pdf/individual/` stores the converted and unprotected PDFs per employee.
- *`pdf/protected_individuals/` stores the same PDFs but password protected with their respective PAN numbers.
- *`pdf/master/` stores a single combined PDF of all the employees.
- ***Only `pdf/protected_individuals/` stores password protected PDF files.***

The output folder is wiped clean at the start of every run so that nothing conflicts from the previous batch.
