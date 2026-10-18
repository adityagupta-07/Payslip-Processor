from . import excel_constants

class Employee():

    def __init__(self):
        setattr(self, excel_constants.SSF_EMPLOYER, "")
        setattr(self, excel_constants.SSF_EMPLOYER_UPPER, "")
        setattr(self, excel_constants.SSF_EMPLOYER_LOWER, "")
        setattr(self, excel_constants.EMPLOYEE_ID, "")
        setattr(self, excel_constants.EMPLOYEE_NAME, "")
        setattr(self, excel_constants.DESIGNATION, "")
        setattr(self, excel_constants.PAN, "")
        setattr(self, excel_constants.CONTACT_NUMBER, "")
        setattr(self, excel_constants.BASIC_SALARY, "")
        setattr(self, excel_constants.ALLOWANCES, "")
        setattr(self, excel_constants.GROSS_SALARY, "")
        setattr(self, excel_constants.GROSS_SALARY_AS_PER_WORKING_HOURS, "")
        setattr(self, excel_constants.BONUS, "")
        setattr(self, excel_constants.TOTAL, "")
        setattr(self, excel_constants.SSF_EMPLOYEE, "")
        setattr(self, excel_constants.TDS_FOR_THE_MONTH, "")
        setattr(self, excel_constants.TOTAL_DEDUCTION, "")
        setattr(self, excel_constants.NET_SALARY_PAID, "")
        setattr(self, excel_constants.ACCOUNT_NUMBER, "")
        setattr(self, excel_constants.BANK_NAME, "")
        setattr(self, excel_constants.BRANCH, "")
        setattr(self, excel_constants.MARITAL_STATUS, "")
        setattr(self, excel_constants.ANNUAL_TAXABLE_SALARY, "")
        setattr(self, excel_constants.ANNUAL_SSF_DEPOSIT, "")
        setattr(self, excel_constants.ANNUAL_TDS_PAYMENT, "")
        setattr(self, excel_constants.ANNUAL_NET_SALARY, "")
        setattr(self, excel_constants.MONTH, "")
        setattr(self, excel_constants.FINANCIAL_YEAR_NOTE, "")
        setattr(self, excel_constants.MONTH_YEAR, "")
        setattr(self, excel_constants.MONTH_YEAR_UPPER, "")

    def check_attribute(self, key) -> bool:
        if hasattr(self, key):
            return True

    def set_atr(self, key, value):
        setattr(self, key, value)

    def get_atr(self, key):
        return getattr(self, key)