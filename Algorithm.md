ULTRA PAYSLIP PRO - ALGORITHM

1. Ask user for Excel file path, month, year, and optional custom title.
2. Validate all required inputs are provided; stop with error if not.
3. Open Excel file and read row by row:
   - If column A = "EMPLOYEE INFORMATION", save current employee (if any) and start new one.
   - Store column A->B pairs and column C->D pairs as employee info.
   - If column C looks like a financial year note and D is empty, save it separately.
4. Save the last employee after the loop ends.
5. If no employees found, stop with error.
6. Check template.docx and template_no_id.docx both exist; stop with error if either missing.
7. For each employee, prepare data:
   - Name, employee ID, bank details, basic salary, allowances, deductions, total salary, annual salary.
   - Clean numbers (remove commas) and format amounts as Rs. X,XXX.XX.
   - Extract financial year range from note, if available.
   - Set heading = custom title if given, else month + year.
   - Keep plain month and year separately too.
8. For each employee, pick template:
   - Has employee ID -> template.docx
   - No employee ID -> template_no_id.docx
9. For each employee, fill template:
   - Extract docx (as zip) into temp folder.
   - Find XML files inside, replace placeholders with actual data.
   - Repack as new docx named Employee_1, Employee_2, etc.
10. Merge all individual docx files into one master docx:
    - Use first employee's docx as base, keep its section settings.
    - For each remaining employee, add page break then append content, skipping their section settings.
    - Keep only one final section setting at the end.
11. Convert master docx to PDF (only once):
    - Try Microsoft Word first.
    - If that fails, try LibreOffice headless.
    - If both fail, stop with error asking to install LibreOffice.
12. Split master PDF page by page:
    - Read each page's text to get name, employee ID (if any), month, year.
    - Build filename: Name_Month_Year_ID.pdf (or Name_Month_Year.pdf without ID).
    - Replace spaces with underscores, save each page as its own PDF.
13. Zip all individual PDFs together (no folders) as "Ultra Payslips {Month Year}.zip".
14. Rename master PDF to "Pay Slip - {Month Year}.pdf".
15. Create final zip containing renamed master PDF and individual payslips zip.
16. Save final zip to Downloads:
    - If a file with same name exists, try appending (1), (2), (3)... until a free name is found.
17. Report success: number of employees processed and final zip location.
18. If an error occurs at any step, stop immediately and report what went wrong.