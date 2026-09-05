# Payslip Generation — Algorithm

High-level steps the pipeline follows, from launching the GUI to producing a single merged PDF.

## 0. Resolve paths

Before anything else runs, `directories.py` resolves every path the pipeline needs — template locations and the three output folders (DOCX, individual PDFs, master PDF) — as `pathlib.Path` objects built relative to the project root (derived from the module's own file location via `__file__`). Every other module asks `directories.py` for a path rather than hardcoding one, so the app works regardless of which folder it's launched from.

## 1. Launch the GUI

1. `main.py` calls `launch_gui(main, pdfs_folder)` on startup (instead of running `main()` directly)
2. Build the window:
   - **Browse** button → opens the file picker
   - **Exit** button → closes the app
   - Status label → shows current state ("Please select an excel file", "Processing...", "Processed!", "Failed!")
   - **Open File Location** button → hidden until a run succeeds
3. Enter the Tkinter main loop and wait for user interaction


## 2. Select the input file

1. User clicks **Browse**
2. Open a file-picker dialog filtered to `.xlsx` files
3. If the user cancels (no file chosen) → do nothing, return to idle state
4. Otherwise:
   - Set status label to "Processing..."
   - Disable **Browse** and **Exit** buttons
   - Hide **Open File Location** button
   - Kick off `process_file()` on a background thread, passing the selected file path

> Note: the old terminal prompt (`user_input()`, strip stray quote characters) only runs if `main()` is ever called with `None` directly, bypassing the GUI — not part of the normal GUI flow.


## 3. Run the pipeline on a background thread

1. Background thread calls `main(file_path)`
2. On success → schedule `on_processing_done()` on the main thread
3. On any exception → capture the error message and schedule `on_processing_failed()` on the main thread

   This keeps the GUI responsive while the Excel/DOCX/PDF work happens.


## 4. Load the sheet

1. Open the workbook with openpyxl (`data_only=True`, so formulas resolve to values)
2. Grab the active worksheet
3. Return the worksheet object


## 5. Locate employee blocks

1. Scan every cell in the sheet
2. Record row numbers where cell value == "EMPLOYEE INFORMATION" → block start
3. Record row numbers where cell value == "Net Salary Paid" → block end
4. Zip start with end pairwise
   → produces a list of (start_row, end_row) tuples, one per employee, e.g. (1, 19)


## 6. Clear output folders

FOR each folder in [Docs, Individual PDFs, Master PDF]:
    Delete all contents and recreate the empty folder

> Runs once, right after blocks are located and before any employee dict is built.


## 7. Reset the employee dict template

1. Create a fresh copy of the employee dict shape
   (all fields blank, including nested "duplicates" and "specials" dicts)
2. Do this once per employee block — never reuse the same dict instance


## 8. Extract employee details per block

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


## 9. Build placeholder map per employee

FOR each employee in employee_details:
    Map every employee field to its corresponding template placeholder key
    (e.g. "Employee Name" → "EMPLOYEE_NAME", "Basic Salary" → "BASIC_SALARY", ...)


## 10. Generate individual DOCX payslips

FOR each employee:
    1. Choose template:
         - Template_no_id.docx   IF Employee ID is blank
         - Template_id.docx      OTHERWISE
    2. Build output filename from: Name + Month + Year (+ Employee ID if present)
    3. Copy the chosen template to Docs/<filename>.docx
    4. Load it with DocxTemplate
    5. Render it with the placeholder map from Step 8
    6. Save


## 11. Convert DOCX → PDF (batch)

Convert every DOCX in the Docs folder to PDF, saved into the Individual PDFs folder.

> Two interchangeable strategies exist in `pdf_converter.py`:
> - **Word-dependent** (`docx2pdf.convert`, via `batch_convert_docx_to_pdf1`) — preserves formatting, requires MS Word installed. **This is the one currently used.**
> - **Word-independent** (`dxpdf.convert`, via `batch_convert_docx_to_pdf`) — portable, but messes up formatting. Defined but unused.


## 12. Merge into a master PDF

1. Open a new blank PDF document
2. FOR each PDF in the Individual PDFs folder:
       Insert its pages into the master document
3. Save merged file as:
   "Master PDF/Payslip - <Month> <Year>.pdf"


## 13. Report result back to the GUI

- **On success:**
  1. Status label → "Processed!"
  2. Re-enable **Browse** and **Exit** buttons
  3. Show the **Open File Location** button
     - Clicking it opens the PDFs output folder (`os.startfile`)
- **On failure:**
  1. Status label → "Failed!"
  2. Re-enable **Browse** and **Exit** buttons
  3. Show an error message box with the exception text


---

## Pipeline order (main.py + gui.py)

```
launch_gui(main, pdfs_folder)
  → user clicks Browse → file dialog → picks .xlsx
    → background thread: main(file_path)
        → load_excel_file()
          → get_employee_block()
            → delete_contents([Docs, Individual PDFs, Master PDF])
              → FOR each block: new_employee_dict() → get_details_per_employee() → deepcopy → append
                → FOR each employee: fill_placeholders_in_docx() → docx_creation()
                  → batch_convert_docx_to_pdf1()
                    → master_pdf_creation()
    → success → on_processing_done()  [status: "Processed!", show Open File Location]
    → failure → on_processing_failed() [status: "Failed!", show error dialog]
```