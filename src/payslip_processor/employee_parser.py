from src.payslip_processor import Employee

def get_employee_block(sheet, string1, string2, matching_row_numbers):
    string1_rows = matching_row_numbers(string1, sheet)
    string2_rows = matching_row_numbers(string2, sheet)
    return list(zip(string1_rows, string2_rows))

def empty_nested_dict(dictionary):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            empty_nested_dict(value)
        else:
            dictionary[key] = ""
    return dictionary

def get_details_per_employee(sheet, block, employee_obj: Employee):

    found_ssf_contribution_by_employer = False

    for r in range(block[0], block[1] + 1): # r loops from 1 to 20 (exclusive)
        for target_cell in sheet[r]: # target_cell loops through all the cells in row(r), means row(1), row(2), row(3), ...

            target_value = (
                target_cell.value.strip() 
                if isinstance(target_cell.value, str) 
                else target_cell.value
            )

            if not employee_obj.check_attribute(str(target_value)): # Checks if target_value is present as atr in obj
                continue

            next_cell = sheet.cell(row=r, column=(target_cell.column+1))

            if "SSF Contribution by Employer" in target_value:
                if found_ssf_contribution_by_employer is True:
                    employee_obj.set_atr(
                        "Lower SSF Contribution by Employer", f"Rs. {next_cell.value:,.2f}"
                    )
                    break
                else:
                    found_ssf_contribution_by_employer = True
                    employee_obj.set_atr(
                        "Upper SSF Contribution by Employer", f"Rs. {next_cell.value:,.2f}"
                    )
                    employee_obj.set_atr(
                        "Financial_Year_Note", sheet.cell(row=r, column=(target_cell.column+2)).value
                    )

            if isinstance(next_cell.value, (int, float)) and (r > block[1]-13 and r < block[1]+1):
                employee_obj.set_atr(target_value, f"Rs. {next_cell.value:,.2f}")
            else:
                employee_obj.set_atr(target_value, next_cell.value)

            if r == (block[1]-2) and target_cell.column == 3:
                # next_cell.value is returning <class 'datetime.datetime'> (2026-05-01 00:00:00) so we can change the format (%B = August, %Y = 2026)
                employee_obj.set_atr("Month_year", next_cell.value)
                employee_obj.set_atr(target_value, next_cell.value.strftime("%b %Y"))

    return employee_obj
