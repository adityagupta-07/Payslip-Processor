import tkinter as tk
import time   

def on_button_click():
    print("Task started…")
    time.sleep(5) # Simulating a long task
    print("Task finished!")

root = tk.Tk()

root.title("Basic Tkinter App")
root.geometry('500x500')

button = tk.Button(root, text="Click Me", command=on_button_click)

button.pack(pady=20)

root.mainloop()