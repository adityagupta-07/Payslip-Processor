import tkinter as tk
import time   
import threading

def on_button_click():
    button.config(state="disabled")
    print("Task started...")
    threading.Thread(target=long_running_task).start()

def long_running_task():
    time.sleep(5)  # Simulating a long task
    ''''
    Still on the BACKGROUND thread here.
    root.after() does NOT run task_finished immediately or on this thread.
    It just registers task_finished, saying:
    "run this on the main thread, at least 1ms from now."
    it is counted from this exact line, right before the BACKGROUND thread ends
    '''
    root.after(1, task_finished)

def task_finished():
    # Runs on the MAIN thread (because it was scheduled via root.after)
    # Safe to update widgets here
    button.config(state="normal")
    print("Task finished!")


root = tk.Tk()
root.title("Basic Tkinter App")
root.geometry('500x500')

button = tk.Button(root, text="Click Me", command=on_button_click)
button.pack(pady=20)

root.mainloop()