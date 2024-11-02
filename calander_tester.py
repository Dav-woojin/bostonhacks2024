import customtkinter as ctk
import calendar
from datetime import datetime
from tkinter import messagebox

# Create main application window
root = ctk.CTk()
root.title("MindOrbit")
root.geometry("1000x1000")  # NEED TO MAKE FLEXIBLE FOR FULL SCREEN

# Today's month and year for calendar
current_date = datetime.today()
year = current_date.year
month = current_date.month

# Dictionary to store tasks by date
tasks = {}

# Function to show tasks for the selected date
def show_selected_date(selected_day):
    selected_date = f"{year}-{month:02d}-{selected_day:02d}"  # Format as YYYY-MM-DD
    task_list = tasks.get(selected_date, [])
    if task_list:
        tasks_str = "\n".join(task_list)
        messagebox.showinfo("Tasks for " + selected_date, f"Tasks:\n{tasks_str}")
    else:
        messagebox.showinfo("Tasks for " + selected_date, "No tasks for this date.")

# Function to update the calendar grid
def update_calendar():
    # Clear the previous grid
    for widget in calendar_frame.winfo_children():
        widget.destroy()
  
    # Update title label
    title_label.configure(text=f"{calendar.month_name[month]} {year}")

    # Get the number of days in the month and the starting weekday
    days_in_month = calendar.monthrange(year, month)[1]
    first_weekday = calendar.monthrange(year, month)[0]

    # Calendar physical
    day = 1
    for row in range(6):
        for col in range(7): 
            if row == 0 and col < first_weekday:
                ctk.CTkLabel(calendar_frame, text="").grid(row=row, column=col, padx=5, pady=5)
            elif day > days_in_month:
                break  # Days end when month end
            else:
                # Buttons for each day
                day_button = ctk.CTkButton(calendar_frame, text=str(day), width=80, height=80,
                                           corner_radius=10, fg_color="gray",
                                           command=lambda d=day: show_selected_date(d))
                day_button.grid(row=row, column=col, padx=5, pady=5)
                day += 1

# Function to go to the previous month
def prev_month():
    global month, year
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1
    update_calendar()

# Function to go to the next month
def next_month():
    global month, year
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
    update_calendar()

# Create title and navigation buttons
title_frame = ctk.CTkFrame(root)
title_frame.pack(pady=10)

# Go back month arrow button
prev_button = ctk.CTkButton(title_frame, text="<", width=50, command=prev_month)
prev_button.grid(row=0, column=0, padx=5)

# Month between arrow buttons
title_label = ctk.CTkLabel(title_frame, text=f"{calendar.month_name[month]} {year}", font=("Arial", 24))
title_label.grid(row=0, column=1, padx=20)

# Go up month arrow button
next_button = ctk.CTkButton(title_frame, text=">", width=50, command=next_month)
next_button.grid(row=0, column=2, padx=5)

# Create a frame to hold the calendar grid
calendar_frame = ctk.CTkFrame(root)
calendar_frame.pack(expand=True, fill="both", padx=10, pady=10)

# Initial calendar display
update_calendar()

# Optional: Add a way to add tasks to a specific date
def add_task(selected_day):
    task = ctk.CTkEntry(root, placeholder_text="Enter task")
    task.pack(pady=5)
    task_button = ctk.CTkButton(root, text="Add Task", command=lambda: add_task_to_date(selected_day, task.get()))
    task_button.pack(pady=5)

def add_task_to_date(selected_day, task):
    selected_date = f"{year}-{month:02d}-{selected_day:02d}"
    if selected_date in tasks:
        tasks[selected_date].append(task)
    else:
        tasks[selected_date] = [task]
    messagebox.showinfo("Task Added", f"Task '{task}' added for {selected_date}")

# Add a button to allow adding tasks
add_task_button = ctk.CTkButton(root, text="Add Task to Selected Date", command=lambda: add_task(selected_day=1))
add_task_button.pack(pady=5)

root.mainloop()