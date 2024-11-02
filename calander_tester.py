# TESTING customtkinter to make boxes around number so 
# they are actually clickable and easier to make look good

#import tkinter as tk                          
import customtkinter as ctk
from tkcalendar import Calendar
import calendar
from datetime import datetime


# Create main application window
root = ctk.CTk()
root.title("MindOrbit")
root.geometry("1000x1000") #NEED TO MAKE FLEXABLE FOR FULL SCREEN

# Today's month and year for calender
current_date = datetime.today()
year = current_date.year
month = current_date.month

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

    # Calender physical
    day = 1
    for row in range(6): 
        for col in range(7):  
            if row == 0 and col < first_weekday:
                ctk.CTkLabel(calendar_frame, text="").grid(row=row, column=col, padx=5, pady=5)
            elif day > days_in_month:
                break #Days end when month end
            else:
                # Buttons for each day
                day_label = ctk.CTkButton(calendar_frame, text=str(day), width=80, height=80,
                                          corner_radius=10, fg_color="gray",
                                          command=lambda d=day: print(f"Selected day: {d}"))
                day_label.grid(row=row, column=col, padx=5, pady=5)
                day += 1

# Figuring out the previous month
def prev_month():
    global month, year
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1
    update_calendar()

# Figuring out the next month
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

#Go back month arrow button
prev_button = ctk.CTkButton(title_frame, text="<", width=50, command=prev_month)
prev_button.grid(row=0, column=0, padx=5)

# Month between arrow buttons
title_label = ctk.CTkLabel(title_frame, text=f"{calendar.month_name[month]} {year}", font=("Arial", 24))
title_label.grid(row=0, column=1, padx=20)

# Go up month arrow button
next_button = ctk.CTkButton(title_frame, text=">", width=50, command=next_month)
next_button.grid(row=0, column=2, padx=5)

# Create a frame to hold the calendar grid NEED TO MAKE FLEXABLE
calendar_frame = ctk.CTkFrame(root)
calendar_frame.pack(expand=True, fill="both", padx=10, pady=10)

# Initial calendar display
update_calendar()

#NEED: to add back task adding feature to each month. 

root.mainloop()
