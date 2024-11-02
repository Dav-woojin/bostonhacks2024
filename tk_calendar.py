import tkinter as tk
from tkinter import messagebox

# Function to fetch data from the Flask API
"""def fetch_data():
    try:
        response = requests.get('http://127.0.0.1:5000/data')  # Adjust if your server is hosted elsewhere
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()  # Parse the JSON response
        
        # Clear existing data
        for widget in data_frame.winfo_children():
            widget.destroy()
        
        # Display the data in the Tkinter window
        for item in data:
            label = tk.Label(data_frame, text=item)  # Display each item
            label.pack()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")
"""
# Set up the main Tkinter window
root = tk.Tk()
root.title("Calendar")

# Create a frame to hold data
data_frame = tk.Frame(root)
data_frame.pack(pady=10)

# Create a button to fetch data
"""fetch_button = tk.Button(root, text="Fetch Data", command=fetch_data)
fetch_button.pack(pady=10)"""

import tkinter as tk
from tkcalendar import Calendar
from tkinter import messagebox

# Function to handle date selection
def show_selected_date():
    selected_date = calendar.get_date()
    # Replace this part with your code to fetch/display tasks for the selected date
    messagebox.showinfo("Selected Date", f"You selected {selected_date}")

# Function to add a task to a selected date (this is a placeholder function)
def add_task():
    selected_date = calendar.get_date()
    # Code to add a task (e.g., interact with MongoDB or any other database)
    # For demonstration, we'll just show a message
    task = task_entry.get()
    if task:
        messagebox.showinfo("Task Added", f"Task '{task}' added for {selected_date}")
        task_entry.delete(0, tk.END)  # Clear the entry field after adding
    else:
        messagebox.showwarning("No Task", "Please enter a task to add.")


# Set up the main Tkinter window
root = tk.Tk()
root.title("Tkinter Calendar")

# Create a calendar widget
calendar = Calendar(root, selectmode="day", year=2024, month=11, day=2)
calendar.pack(pady=20)

# Button to show selected date's tasks
select_button = tk.Button(root, text="Show Selected Date", command=show_selected_date)
select_button.pack(pady=5)

# Entry and button to add tasks
task_entry = tk.Entry(root, width=30)
task_entry.pack(pady=5)
add_button = tk.Button(root, text="Add Task to Selected Date", command=add_task)
add_button.pack(pady=5)

# Run the Tkinter main loop
root.mainloop()


