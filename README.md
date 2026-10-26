# Payslip Processor

Turn one Excel workbook into payslips for every employee. The tool creates:

- a **password-protected PDF** for each employee, locked with their own PAN number
- an **unprotected PDF** and a **Word file** for each employee
- one **master PDF** containing every payslip
- a copy of each protected PDF placed in the employee's own **SharePoint folder**, which get synced to Sharepoint online

It runs in Docker and is reachable as a small web page in the browser.

## Requirements

- Docker
- Google Chrome or Microsoft Edge

## Installation

```
docker pull aadityagupta077/payslip-processor:latest
```

## Usage

**1. Start the container**

```
docker run --rm -p 127.0.0.1:8000:8000 aadityagupta077/payslip-processor:latest
```

**2. Open the page**

Go to **http://localhost:8000** in Chrome or Edge.

**3. Choose the files:**

| Button | What to choose |
|---|---|
| **Select Excel File** | The workbook with the employee payslip data (`.xlsx`) |
| **Select Output Folder** | The folder where the generated files will be saved |
| **Select SharePoint Payslips Folder** | The local Payslips folder that contains the `Emp_...` folders |
| **Year folder name** | The year folder inside each employee folder, for example `2083-84` |

Chrome asks for permission to write into each folder. The permission lasts until the tab is closed.

**4. Click Process**

The status line shows each step. When **Processed!**, is displayed, the process is complete.

Any employee whose payslip could not be placed in SharePoint is listed under the status line, for example *'No destination folder found for Rohit Sharma'*.

> Chrome does not allow choosing a few top-level system folders (such as Desktop, Documents, Downloads, etc.) for writing. Choose a folder inside them.

## SharePoint folder layout

Employee folders are matched by their names. If two employees share a same name, the ID in the folder name is checked.

```
Payslips/
├── Emp_11 - Rohit Sharma/
│   └── 2083-84/
│       └── May.pdf        ← the protected payslip is placed here
└── Emp_12 - Sulav Pokharel/
    └── 2083-84/
        └── May.pdf
```

OneDrive or SharePoint then syncs the new files by itself to online Sharepoint.

## Output

Everything is saved inside an `Ultra Payslips` folder into the chosen output folder:

| Folder | Contents |
|---|---|
| `docx/` | The generated Word file for each employee |
| `pdf/individual_pdfs/` | Each employee's PDF, unprotected |
| `pdf/protected_individual_pdfs/` | The same PDFs, password-protected with each employee's PAN |
| `pdf/master_pdf/` | One combined PDF of all employees, for example `Payslip - May 2026.pdf` |

## How it works

```
Browser                                    Container
───────                                    ─────────
select the Excel file and 2 folders
Excel file & employee folder names   ──►   processes the payslips and save in a temporary folder
                                          (Word → PDF → master PDF → PAN protected PDFs)
files are saved into chosen folders  ◄──   returns the files, then deletes the temporary folders
```

## Development

Run the web app locally:

```
pip install -r requirements.txt
python -m src
```
