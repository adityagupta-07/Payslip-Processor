class ExcelConstants():

    def __init__(self):
        self.SSF_EMPLOYER = "SSF Contribution by Employer"
        self.SSF_EMPLOYER_UPPER = "Upper SSF Contribution by Employer"
        self.SSF_EMPLOYER_LOWER = "Lower SSF Contribution by Employer"
        self.EMPLOYEE_ID = "Employee ID"
        self.EMPLOYEE_NAME = "Employee Name"
        self.DESIGNATION = "Designation"
        self.PAN = "PAN"
        self.CONTACT_NUMBER = "Contact Number"
        self.BASIC_SALARY = "Basic Salary"
        self.ALLOWANCES = "Allowances"
        self.GROSS_SALARY = "Gross Salary"
        self.GROSS_SALARY_AS_PER_WORKING_HOURS = "Gross Salary as per working hours"
        self.BONUS = "Bonus"
        self.TOTAL = "Total"
        self.SSF_EMPLOYEE = "SSF Contribution by Employee"
        self.TDS_FOR_THE_MONTH = "TDS for the month"
        self.TOTAL_DEDUCTION = "Total Deduction"
        self.NET_SALARY_PAID = "Net Salary Paid"
        self.ACCOUNT_NUMBER = "Account Number"
        self.BANK_NAME = "Bank Name"
        self.BRANCH = "Branch"
        self.MARITAL_STATUS = "Marital Status"
        self.ANNUAL_TAXABLE_SALARY = "Annual Taxable Salary"
        self.ANNUAL_SSF_DEPOSIT = "Annual SSF deposit"
        self.ANNUAL_TDS_PAYMENT = "Annual TDS Payment"
        self.ANNUAL_NET_SALARY = "Annual Net Salary"
        self.MONTH = "Month"
        self.FINANCIAL_YEAR_NOTE = "Financial_year_note"
        self.MONTH_YEAR = "Month_year"
        self.MONTH_YEAR_UPPER = "Month_year_upper"

    def get_atr(self, key):
        return getattr(self, key)

    
class DocxConstants():

    def __init__(self):
        self.MONTH_YEAR_UPPER = "MONTH_YEAR_UPPER"
        self.EMPLOYEE_ID = "EMPLOYEE_ID1"
        self.EMPLOYEE_NAME = "EMPLOYEE_NAME"
        self.DESIGNATION = "DESIGNATION"
        self.PAN = "PAN_number"
        self.CONTACT_NUMBER = "CONTACT_NUMBER"
        self.BASIC_SALARY = "BASIC_SALARY"
        self.ALLOWANCES = "ALLOWANCES"
        self.GROSS_SALARY = "GROSS_SALARY"
        self.GROSS_SALARY_WORKING_HOURS = "GROSS_SALARY_WORKING_HOURS"
        self.UPPER_SSF_EMPLOYER = "UPPER_SSF_EMPLOYER"
        self.BONUS = "BONUS"
        self.TOTAL = "TOTAL"
        self.LOWER_SSF_EMPLOYER = "LOWER_SSF_EMPLOYER"
        self.SSF_EMPLOYEE = "SSF_EMPLOYEE"
        self.TDS_FOR_MONTH = "TDS_FOR_MONTH"
        self.TOTAL_DEDUCTION = "TOTAL_DEDUCTION"
        self.NET_SALARY_PAID = "NET_SALARY_PAID"
        self.ACCOUNT_NUMBER = "ACCOUNT_NUMBER"
        self.BANK_NAME = "BANK_NAME"
        self.BRANCH = "BRANCH"
        self.MARITAL_STATUS = "MARITAL_STATUS"
        self.ANNUAL_TAXABLE_SALARY = "ANNUAL_TAXABLE_SALARY"
        self.ANNUAL_SSF_DEPOSIT = "ANNUAL_SSF_DEPOSIT"
        self.ANNUAL_TDS_PAYMENT = "ANNUAL_TDS_PAYMENT"
        self.ANNUAL_NET_SALARY = "ANNUAL_NET_SALARY"
        self.FINANCIAL_YEAR_NOTE = "FINANCIAL_YEAR_NOTE"
        self.MONTH_YEAR = "MONTH_YEAR"

    def get_atr(self, key):
        return getattr(self, key)

    