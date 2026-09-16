from .constants import ExcelConstants

class Employee():
    
    def __init__(self):
        reader = ExcelConstants()
        for key, value in vars(reader).items():
            setattr(self, value, "")

    def check_attribute(self, key) -> bool:
        if hasattr(self, key):
            return True

    def set_atr(self, key, value):
        setattr(self, key, value)

    def get_atr(self, key):
        return getattr(self, key)