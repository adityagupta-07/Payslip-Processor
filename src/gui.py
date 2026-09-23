import threading, os, tkinter as tk
from tkinter import filedialog, messagebox
from .directories import PathConfig

def browse_file(main_function, exit_button, paths):
    initial_dir = "/host_home" if os.path.exists("/host_home") else "/home/aditya/Coding/Python/Payslip_Processor/data/input"
    input_excel_file_path = filedialog.askopenfilename(
        initialdir=initial_dir,
        title="Select a File",
        filetypes=(("Excel files", "*.xlsx*"), ("all files", "*.*"))
    )
    if not input_excel_file_path:
        return
    status_label.config(text="Processing...")
    button.config(state="disabled")
    exit_button.config(state="disabled")
    open_location_button.pack_forget()
    threading.Thread(target=process_file, args=(main_function, input_excel_file_path, exit_button, paths)).start()

def process_file(main_function, input_excel_file_path, exit_button, paths):
    try:
        main_function(input_excel_file_path, paths)
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

def show_file_location(pdfs_folder):
    # Inside Docker, show the real host path (set via -e HOST_OUTPUT_DIR=...)
    location = os.environ.get("HOST_OUTPUT_DIR", str(pdfs_folder))
    messagebox.showinfo("Output Location", f"Your files are saved in:\n\n{location}")

def launch_gui(main_function, paths: PathConfig):
    global root, button, status_label, open_location_button

    root = tk.Tk()
    root.title("Payslip Processor")
    root.geometry('500x500')

    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)

    button = tk.Button(button_frame, text="Browse", command=lambda: browse_file(main_function, exit_button, paths))
    button.grid(row=0, column=0, padx=10)

    exit_button = tk.Button(button_frame, text="Exit", command=root.destroy)
    exit_button.grid(row=0, column=1, padx=10)

    status_label = tk.Label(root, text="Please select an excel file", wraplength=450)
    status_label.pack(pady=10)

    open_location_button = tk.Button(root, text="Show File Location", command=lambda: show_file_location(paths.output_folder_path))

    root.mainloop()