import tkinter as tk
from tkcalendar import Calendar
from tkinter import messagebox

# Dictionary to store tasks by date
tasks = {}

# Function to handle date selection
def show_selected_date():
    selected_date = calendar.get_date()
    task_list = tasks.get(selected_date, [])
    if task_list:
        tasks_str = "\n".join(task_list)
        messagebox.showinfo("Tasks for " + selected_date, f"Tasks:\n{tasks_str}")
    else:
        messagebox.showinfo("Tasks for " + selected_date, "No tasks for this date.")

# Function to add a task to a selected date
def add_task():
    selected_date = calendar.get_date()
    task = task_entry.get()
    if task:
        if selected_date in tasks:
            tasks[selected_date].append(task)
        else:
            tasks[selected_date] = [task]
        messagebox.showinfo("Task Added", f"Task '{task}' added for {selected_date}")
        task_entry.delete(0, tk.END)  # Clear the entry field after adding
    else:
        messagebox.showwarning("No Task", "Please enter a task to add.")

# Set up the main Tkinter window
root = tk.Tk()
root.title("Tkinter Calendar")
root.geometry("1000x1000")  # Set the window size

# Create a calendar widget
calendar = Calendar(root, selectmode="day", year=2024, month=11, day=2)
calendar.pack(pady=20)

# Label for selecting a date
label = tk.Label(root, text="Select a date:")
label.pack(pady=10)

# Button to show selected date's tasks
select_button = tk.Button(root, text="Show Selected Date", command=show_selected_date)
select_button.pack(pady=5)

# Entry to add tasks
task_entry = tk.Entry(root)
task_entry.pack(pady=5)

add_button = tk.Button(root, text="Add Task to Selected Date", command=add_task)
add_button.pack(pady=5)

# Run the Tkinter main loop
root.mainloop()
