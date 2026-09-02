import tkinter
from tkinter import ttk
from tkinter.messagebox import showinfo

class App(tkinter.Tk):
  def __init__(self):
    super().__init__()

    self.title('Payslip Processor')
    self.geometry('500x500')

    # label
    self.label = ttk.Label(self, text='Please select input excel file.')
    self.label.pack()

    # button
    self.button = ttk.Button(self, text='Browse File')
    self.button.pack()
    

if __name__ == "__main__":
  app = App()
  app.mainloop()