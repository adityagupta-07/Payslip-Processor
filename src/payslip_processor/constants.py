class ExcelReader():

    def __init__(self):
        emp_details = {
            "SSF_EMPLOYER": "SSF Contribution by Employer",
            "SSF_EMPLOYER_UPPER": "Upper SSF Contribution by Employer",
            "SSF_EMPLOYER_LOWER": "Lower SSF Contribution by Employer",
            "EMPLOYEE_ID": "Employee ID",
            "EMPLOYEE_NAME": "Employee Name",
            "DESIGNATION": "Designation",
            "PAN": "PAN",
            "CONTACT_NUMBER": "Contact Number",
            "BASIC_SALARY": "Basic Salary",
            "ALLOWANCES": "Allowances",
            "GROSS_SALARY": "Gross Salary",
            "GROSS_SALARY_AS_PER_WORKING_HOURS": "Gross Salary as per working hours",
            "BONUS": "Bonus",
            "TOTAL": "Total",
            "SSF_EMPLOYEE": "SSF Contribution by Employee",
            "TDS_FOR_THE_MONTH": "TDS for the month",
            "TOTAL_DEDUCTION": "Total Deduction",
            "NET_SALARY_PAID": "Net Salary Paid",
            "ACCOUNT_NUMBER": "Account Number",
            "BANK_NAME": "Bank Name",
            "BRANCH": "Branch",
            "MARITAL_STATUS": "Marital Status",
            "ANNUAL_TAXABLE_SALARY": "Annual Taxable Salary",
            "ANNUAL_SSF_DEPOSIT": "Annual SSF deposit",
            "ANNUAL_TDS_PAYMENT": "Annual TDS Payment",
            "ANNUAL_NET_SALARY": "Annual Net Salary",
            "MONTH": "Month",
            "FINANCIAL_YEAR_NOTE": "Financial_Year_Note",
            "MONTH_YEAR": "Month_year",
            "MONTH_YEAR_UPPER": "",
            }

        for key, value in emp_details.items():
            setattr(self, key, value)


# r = ExcelReader()
# print(vars(r))