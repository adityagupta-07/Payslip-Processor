import tkinter as tk
import time   
import threading

def on_button_click():
    print("Task started…")
    def long_running_task():
        time.sleep(5) # Simulating a long task
        print("Task finished!")
    threading.Thread(target=long_running_task).start()

root = tk.Tk()

root.title("Basic Tkinter App")
root.geometry('500x500')

button = tk.Button(root, text="Click Me", command=on_button_click)

button.pack(pady=20)

root.mainloop()