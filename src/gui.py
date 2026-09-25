import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Callable

from .directories import PathConfig

DEFAULT_INPUT_DIR = "/home/aditya/Coding/Python/Payslip_Processor/data/input"
DOCKER_INPUT_DIR = "/host_home"


def get_initial_directory() -> str:
    if os.path.exists(DOCKER_INPUT_DIR):
        return DOCKER_INPUT_DIR

    return DEFAULT_INPUT_DIR


def get_output_location(pdfs_folder, environ=None) -> str:
    environ = os.environ if environ is None else environ
    return environ.get("HOST_OUTPUT_DIR", str(pdfs_folder))


def select_excel_file(file_dialog: Callable) -> str:
    return file_dialog(
        initialdir=get_initial_directory(),
        title="Select a File",
        filetypes=(
            ("Excel files", "*.xlsx*"),
            ("all files", "*.*"),
        )
    )


def process_excel(main_function: Callable, input_file: str, paths: PathConfig) -> None:
    main_function(input_file, paths)


class PayslipGUI:
    def __init__(self, root: tk.Tk, main_function: Callable, paths: PathConfig) -> None:
        self.root = root
        self.main_function = main_function
        self.paths = paths

        self.root.title("Payslip Processor")
        self.root.geometry("500x500")

        self.create_widgets()

    def create_widgets(self) -> None:
        self.create_buttons()
        self.create_status_label()
        self.create_open_location_button()

    def create_buttons(self) -> None:
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        self.browse_button = tk.Button(
            button_frame,
            text="Browse",
            command=self.browse_file,
        )
        self.browse_button.grid(row=0, column=0, padx=10)

        self.exit_button = tk.Button(
            button_frame,
            text="Exit",
            command=self.root.destroy,
        )
        self.exit_button.grid(row=0, column=1, padx=10)

    def create_status_label(self) -> None:
        self.status_label = tk.Label(
            self.root,
            text="Please select an excel file",
            wraplength=450,
        )
        self.status_label.pack(pady=10)

    def create_open_location_button(self) -> None:
        self.open_location_button = tk.Button(
            self.root,
            text="Show File Location",
            command=self.show_file_location,
        )

    def browse_file(self) -> None:
        input_file = select_excel_file(filedialog.askopenfilename)

        if not input_file:
            return

        self.start_processing(input_file)

    def start_processing(self, input_file: str) -> None:
        self.show_processing_message()

        thread = threading.Thread(
            target=self.run_processing,
            args=(input_file,),
        )
        thread.start()

    def show_file_location(self) -> None:
        location = get_output_location(self.paths.output_folder_path)

        messagebox.showinfo(
            "Output Location",
            f"Your files are saved in:\n\n{location}",
        )

    def run_processing(self, input_file: str) -> None:
        try:
            process_excel(self.main_function, input_file, self.paths)
        except Exception as exc:
            self.root.after(0, lambda: self.show_error_message(exc))
        else:
            self.root.after(0, self.show_success_message)

    def show_processing_message(self) -> None:
        self.status_label.config(text="Processing...")
        self.disable_buttons()
        self.open_location_button.pack_forget()

    def show_success_message(self) -> None:
        self.status_label.config(text="Processed!")
        self.enable_buttons()
        self.open_location_button.pack(pady=10)

    def show_error_message(self, error: Exception) -> None:
        self.status_label.config(text="Failed!")
        self.enable_buttons()
        messagebox.showerror("Error", str(error))

    def disable_buttons(self) -> None:
        self.browse_button.config(state="disabled")
        self.exit_button.config(state="disabled")

    def enable_buttons(self) -> None:
        self.browse_button.config(state="normal")
        self.exit_button.config(state="normal")


def launch_gui(main_function: Callable, paths: PathConfig) -> None:
    root = tk.Tk()

    PayslipGUI(
        root=root,
        main_function=main_function,
        paths=paths,
    )

    root.mainloop()