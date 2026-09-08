from .constants import *

class Employee():
    
    def __init__(self):

        emp_details_list = [
            SSF_EMPLOYER,
            SSF_EMPLOYER_UPPER,
            SSF_EMPLOYER_LOWER,
            EMPLOYEE_ID,
            EMPLOYEE_NAME,
            DESIGNATION,
            PAN,
            CONTACT_NUMBER,
            BASIC_SALARY,
            ALLOWANCES,
            GROSS_SALARY,
            GROSS_SALARY_AS_PER_WORKING_HOURS,
            BONUS,
            TOTAL,
            SSF_EMPLOYEE,
            TDS_FOR_THE_MONTH,
            TOTAL_DEDUCTION,
            NET_SALARY_PAID,
            ACCOUNT_NUMBER,
            BANK_NAME,
            BRANCH,
            MARITAL_STATUS,
            ANNUAL_TAXABLE_SALARY,
            ANNUAL_SSF_DEPOSIT,
            ANNUAL_TDS_PAYMENT,
            ANNUAL_NET_SALARY,
            MONTH,
            FINANCIAL_YEAR_NOTE,
            MONTH_YEAR,
        ]

        for key in emp_details_list:
            setattr(self, key, "")

    def check_attribute(self, attr) -> bool:
        if hasattr(self, attr):
            return True

    def set_atr(self, attr_name, value):
        setattr(self, attr_name, value)

    def get_atr(self, key):
        return getattr(self, key)