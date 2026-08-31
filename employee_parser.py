def get_employee_block(string1, string2, sheet, matching_row_numbers):
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

def get_details_per_employee(sheet, block, data_dict):
    found_ssf_contribution_by_employer = False
    for r in range(block[0], block[1] + 1): # r loops from 1 to 20 (exclusive)
        for target_cell in sheet[r]: # target_cell loops through all the cells in row(r), means row(1), row(2), row(3), ...
            target_value = target_cell.value.strip() if isinstance(target_cell.value, str) else target_cell.value            
            if target_value in data_dict:
                next_cell = sheet.cell(row=r, column=(target_cell.column+1))
                if found_ssf_contribution_by_employer is True and "SSF Contribution by Employer" in target_value:
                    data_dict["duplicates"][target_value] = f"Rs. {next_cell.value:,.2f}"
                    break
                if "SSF Contribution by Employer" in target_value:
                    found_ssf_contribution_by_employer = True
                    data_dict["specials"]["Financial_Year_Note"] = sheet.cell(row=r, column=(target_cell.column+2)).value
                if isinstance(next_cell.value, (int, float)) and (r > block[1]-13 and r < block[1]+1):
                    data_dict[target_value] = f"Rs. {next_cell.value:,.2f}"
                else:
                    data_dict[target_value] = next_cell.value
                if r == (block[1]-2) and target_cell.column == 3:
                    # next_cell.value is returning <class 'datetime.datetime'> (2026-05-01 00:00:00) so we can change the format (%B = August, %Y = 2026)
                    data_dict["specials"]["Month_year"] = next_cell.value
                    data_dict[target_value] = next_cell.value.strftime("%b %Y")
    return data_dict
