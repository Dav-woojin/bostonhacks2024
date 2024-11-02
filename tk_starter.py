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


