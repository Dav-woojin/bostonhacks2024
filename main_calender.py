import customtkinter as ctk
import calendar
from datetime import datetime
from tkinter import PhotoImage 
from tkinter import messagebox
from server import database
import response

root = ctk.CTk()
root.title("MindOrbit")
root.geometry("1000x1000")

current_date = datetime.today()
year = current_date.year
month = current_date.month

tasks = {}
selected_date = None  

# Space-themed colors
bg_color = "#1B1B2B"  # Dark background for space
task_bg_color = "#2E2E3A"  # Slightly lighter background for tasks
button_fg_color = "#3E4C6D"  # Soft grayish-blue for buttons
text_color = "#FFFFFF"  # White text for contrast
label_color = "#A0A0C0"  # Soft lavender for labels


# Load the background image for the calendar frame
bg_image = PhotoImage(file="night_sky.png")  # Ensure the image path is correct

def show_selected_date(selected_day):
    global selected_date
    selected_date = f"{year}-{month:02d}-{selected_day:02d}" 
    task_list = tasks.get(selected_date, [])

    for widget in tasks_frame.winfo_children():
        widget.destroy()

    # Display the title for left frame
    ctk.CTkLabel(tasks_frame, text="Tasks", font=("Arial", 18), text_color=text_color).pack(pady=10)

    if task_list:
       for task in task_list:
           ctk.CTkLabel(tasks_frame, text=task, text_color=text_color).pack(pady=5)
    else:
       ctk.CTkLabel(tasks_frame, text="No tasks for this date.", text_color=text_color).pack(pady=5)

    # Clear and update right frame
    for widget in push_yourself_frame.winfo_children():
        widget.destroy()

    # Display the title for the push yourself section (right frame)
    ctk.CTkLabel(push_yourself_frame, text="Push Yourself!", font=("Arial", 18), text_color=text_color).pack(pady=10)

    # Add task entry and button in the right frame
    task_entry = ctk.CTkEntry(push_yourself_frame, placeholder_text="Enter task")
    task_entry.pack(pady=5)
    add_task_button = ctk.CTkButton(push_yourself_frame, text="Add Task",
                                    command=lambda: add_task_to_date(task_entry.get()))
    add_task_button.pack(pady=5)

    pref = database.get_pref()
    suggestions = response.generate_response(pref)
    suggestion_label = ctk.CTkLabel(tasks_frame, text=suggestions)
    suggestion_label.pack(pady=5)

    title_label.configure(text=f"{calendar.month_name[month]} {selected_day}, {year}", text_color=text_color)

    # Hide the calendar and show the split frame
    calendar_frame.pack_forget()
    split_frame.pack(expand=True, fill="both", padx=10, pady=10)

# Function to update the calendar grid
def update_calendar():
    # Clear the previous grid
    for widget in calendar_frame.winfo_children():
        widget.destroy()

    bg_label = ctk.CTkLabel(calendar_frame, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)  # Fill the entire calendar frame with the image

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
               ctk.CTkLabel(calendar_frame, text="", fg_color="transparent").grid(row=row, column=col, padx=5, pady=5)
           elif day > days_in_month:
               break  # Days end when month end
           else:
               # Buttons for each day
               day_button = ctk.CTkButton(calendar_frame, text=str(day), width=80, height=80,
                                          corner_radius=10, fg_color=button_fg_color,
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

# Function to return to the month view
def return_to_month_view():
    # Hide the split frame and show the calendar again
    split_frame.pack_forget()
    calendar_frame.pack(expand=True, fill="both", padx=10, pady=10)

# Function to add a task to the selected date
def add_task_to_date(task):
    if not selected_date:
        messagebox.showerror("Error", "Please select a date first.")
        return
    
    if task:
        # Add task to the selected date in the tasks dictionary
        if selected_date in tasks:
            tasks[selected_date].append(task)
        else:
            tasks[selected_date] = [task]

        # Update the task list in the left frame
        show_selected_date(int(selected_date.split('-')[2]))
        messagebox.showinfo("Task Added", f"Task '{task}' added for {selected_date}")

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

# Create a frame for the tasks and the push yourself section
split_frame = ctk.CTkFrame(root)

# Left frame for tasks
tasks_frame = ctk.CTkFrame(split_frame)
tasks_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

# Vertical line separator
separator = ctk.CTkFrame(split_frame, width=2, bg_color="gray")
separator.pack(side="left", fill="y")

# Right frame for push yourself section
push_yourself_frame = ctk.CTkFrame(split_frame)
push_yourself_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

# Add a back button to return to the month view
back_button = ctk.CTkButton(split_frame, text="Back to Month View", command=return_to_month_view)
back_button.pack(pady=10)

root.mainloop()
