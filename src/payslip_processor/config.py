class Employee():
    
    def __init__(self):
        
        emp_details_list = [
            "SSF Contribution by Employer",
            "Employee ID",
            "Employee Name",
            "Designation",
            "PAN",
            "Contact Number",
            "Basic Salary",
            "Allowances",
            "Gross Salary",
            "Gross Salary as per working hours",
            "Upper SSF Contribution by Employer",
            "Lower SSF Contribution by Employer",
            "Bonus",
            "Total",
            "SSF Contribution by Employee",
            "TDS for the month",
            "Total Deduction",
            "Net Salary Paid",
            "Account Number",
            "Bank Name",
            "Branch",
            "Marital Status",
            "Annual Taxable Salary",
            "Annual SSF deposit",
            "Annual TDS Payment",
            "Annual Net Salary",
            "Month",
            "Financial_Year_Note",
            "Month_year"
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