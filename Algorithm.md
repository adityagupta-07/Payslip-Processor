# Payslip Generation — Algorithm

High-level steps the pipeline follows, from raw Excel sheet to a single merged PDF.

## 1. Get input file

1. Prompt user for Excel file path
2. Strip any stray quote characters from the path
3. Return path as a dict: {"file_path": <path>}


## 2. Load the sheet

1. Open the workbook with openpyxl (data_only=True, so formulas resolve to values)
2. Grab the active worksheet
3. Return the worksheet object


## 3. Locate employee blocks

1. Scan every cell in the sheet
2. Record row numbers where cell value == "EMPLOYEE INFORMATION"  → block start
3. Record row numbers where cell value == "Net Salary Paid"       → block end
4. Zip start with end pairwise
   → produces a list of (start_row, end_row) tuples, one per employee like (1, 19)


## 4. Reset the employee dict template

1. Create a fresh copy of the employee dict shape
   (all values blank, values of nested "duplicates" and "specials" dicts also blank)
2. Do this once per employee block — never reuse the same dict instance


## 5. Extract employee details per block

FOR each (start_row, end_row) block:
    FOR each row r in range(start_row, end_row + 1):
        FOR each cell in row r:
            IF cell value matches a known field name in the employee dict:
                next_cell = cell to the right

                IF this is a second "SSF Contribution by Employer" match:
                    store it under data["duplicates"]
                    stop scanning this row

                IF this is the first "SSF Contribution by Employer" match:
                    mark it as found
                    capture the "Financial Year Note" from two columns over

                IF next_cell is numeric AND row is near the end of the block:
                    format and store as currency ("Rs. X,XXX.XX")
                ELSE:
                    store raw value

                IF this is the specific "Month/Year" cell:
                    capture as a date object (for filenames later)
                    store formatted display string ("Aug 2026") in the dict

    Append a DEEP COPY of the filled dict to employee_details list


## 6. Clear output folders

FOR each folder in [Tmp, PDFs, Master Pdf]:
    Delete all contents


## 7. Build placeholder map per employee

FOR each employee in employee_details:
    Map every employee field to its corresponding template placeholder key
    (e.g. "Employee Name" → "EMPLOYEE_NAME", "Basic Salary" → "BASIC_SALARY", ...)


## 8. Generate individual DOCX payslips

FOR each employee:
    1. Choose template:
         - Template_no_id.docx   IF Employee ID is blank
         - Template_id.docx      OTHERWISE
    2. Build output filename from: Name + Month + Year (+ Employee ID if present)
    3. Copy the chosen template to Tmp/<filename>.docx
    4. Load it with DocxTemplate
    5. Render it with the placeholder map from Step 7
    6. Save


## 9. Convert DOCX → PDF (batch)

FOR each .docx file in Tmp (skip temp files starting with "~$"):
    Convert to PDF, save into PDFs folder

> Two interchangeable strategies:
> - **Word-dependent** (`docx2pdf.convert`) — preserves formatting, requires MS Word installed
> - **Word-independent** (`dxpdf.convert`) — portable, messes up formatting

## 10. Merge into a master PDF

1. Open a new blank PDF document
2. FOR each PDF in the PDFs folder:
       Insert its pages into the master document
3. Save merged file as:
   "Master Pdf/Payslip - <Month> <Year>.pdf"


---

## Pipeline order (main.py)


user_input()
  → load_excel_file()
    → get_employee_block()
      → delete_contents([Tmp, PDFs, Master Pdf])
        → FOR each block: new_employee_dict() → get_details_per_employee() → deepcopy → append
          → FOR each employee: fill_placeholders_in_docx() → docx_creation()
            → batch_convert_docx_to_pdf1()
              → master_pdf_creation()
