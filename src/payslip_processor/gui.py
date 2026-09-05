import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import subprocess
import sys

file_path = None

def browse_file(main_function, exit_button):
    global file_path
    file_path = filedialog.askopenfilename(
        initialdir="/",
        title="Select a File",
        filetypes=(("Excel files", "*.xlsx*"), ("all files", "*.*"))
    )
    if not file_path:
        return
    status_label.config(text="Processing...")
    button.config(state="disabled")
    exit_button.config(state="disabled")
    open_location_button.pack_forget()
    threading.Thread(target=process_file, args=(main_function, file_path, exit_button)).start()
    # root.after(1, on_processing_done)

def process_file(main_function, file_path, exit_button):
    try:
        main_function(file_path)
        root.after(1, lambda: on_processing_done(exit_button))
    except Exception as e:
        error_message = str(e)
        root.after(1, lambda: on_processing_failed(error_message, exit_button))

def on_processing_done(exit_button):
    status_label.config(text="Processed!")
    button.config(state="normal")
    exit_button.config(state="normal")
    open_location_button.pack(pady=10)

def on_processing_failed(error_message, exit_button):
    status_label.config(text="Failed!")
    button.config(state="normal")
    exit_button.config(state="normal")
    messagebox.showerror("Error", str(error_message))

def open_file_location(pdfs_folder):
    os.startfile(pdfs_folder)
    # if not file_path:
    #     return
    # folder = os.path.dirname(file_path)

    # if sys.platform == "win32":
    #     subprocess.Popen(f'explorer /select,"{file_path}"')
    # elif sys.platform == "darwin":
    #     subprocess.Popen(["open", "-R", file_path])
    # else:
    #     subprocess.Popen(["xdg-open", folder])

def launch_gui(main_function, pdfs_folder):
    global root, button, status_label, open_location_button

    root = tk.Tk()
    root.title("Payslip Processor")
    root.geometry('500x500')

    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)

    button = tk.Button(button_frame, text="Browse", command=lambda: browse_file(main_function, exit_button))
    button.grid(row=0, column=0, padx=10)

    exit_button = tk.Button(button_frame, text="Exit", command=root.destroy)
    exit_button.grid(row=0, column=1, padx=10)

    status_label = tk.Label(root, text="Please select an excel file", wraplength=450)
    status_label.pack(pady=10)

    open_location_button = tk.Button(root, text="Open File Location", command=lambda: open_file_location(pdfs_folder))

    root.mainloop()