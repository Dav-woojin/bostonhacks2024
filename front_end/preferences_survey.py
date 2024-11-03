from tkinter import *
import customtkinter
from pymongo import MongoClient
import sys, os
from dotenv import load_dotenv
load_dotenv()

# Initialize the CustomTkinter app
customtkinter.set_appearance_mode("dark")  # You can use "dark" if preferred
app = customtkinter.CTk()
app.geometry("400x300")
app.title("Survey")

# Survey questions and options (each item is a page)
categories = {
    "Exercise": "What type of exercise do you do?",
    "Sleep": "Average Sleep per Night",
    "Stress": "Select your preferred IDEs:"
    #"Hobbies",
}

survey_data = [
    {"question": categories['Exercise'], "options": ["Python", "JavaScript", "Java", "C++"]},
    {"question": categories['Sleep'], "options": ["VS Code", "PyCharm", "Jupyter", "Eclipse"]},
    {"question": categories['Stress'], "options": ["MongoDB", "MySQL", "PostgreSQL", "SQLite"]},
]

# Variables to track page index and responses
page_index = 0
responses = [{} for _ in range(len(survey_data))]  # List of dictionaries to store answers for each page

# Function to load a page
def load_page():
    global page_index

    # Clear the current frame if any widgets are there
    for widget in page_frame.winfo_children():
        widget.destroy()

    # Get question and options for the current page
    question = survey_data[page_index]["question"]
    options = survey_data[page_index]["options"]

    # Display the question
    question_label = customtkinter.CTkLabel(page_frame, text=question, font=("Arial", 14))
    question_label.pack(pady=10)

    # Display the options as checkboxes
    checkbox_vars = []
    for option in options:
        var = customtkinter.BooleanVar(value=responses[page_index].get(option, False))  # Pre-set previous responses
        checkbox = customtkinter.CTkCheckBox(page_frame, text=option, variable=var)
        checkbox.pack(anchor="w", padx=20)
        checkbox_vars.append((option, var))
    # Store the checkbox variables for later retrieval
    responses[page_index]["checkbox_vars"] = checkbox_vars

    # Update navigation buttons
    back_button.pack_forget() if page_index == 0 else back_button.pack(side="left", padx=10)
    next_button.pack_forget() if page_index == len(survey_data) - 1 else next_button.pack(side="right", padx=10)
    submit_button.pack_forget() if page_index != len(survey_data) - 1 else submit_button.pack(pady=20)

# Function to save current page responses
def save_responses():
    for option, var in responses[page_index]["checkbox_vars"]:
        responses[page_index][option] = var.get()  # Store the boolean value of each checkbox

# Navigation functions
def next_page():
    global page_index
    save_responses()  # Save current page responses
    page_index += 1
    load_page()  # Load the next page

def prev_page():
    global page_index
    save_responses()  # Save current page responses
    page_index -= 1
    load_page()  # Load the previous page


def submit():
    # create new user with these preferences
    save_responses()  # Ensure the last page responses are saved
    survey_response = [{option: selected for option, selected in response.items() if option != "checkbox_vars"} for response in responses]
    print(survey_response)
    exercise = [option for option, selected in survey_response[0].items() if selected == True]
    sleep = [option for option, selected in survey_response[1].items() if selected == True]
    stress = [option for option, selected in survey_response[2].items() if selected == True]
    hobbies = []
    survey_response = {'exercise': exercise, 'sleep': sleep, 'stress': stress}
    print(survey_response)

        

    #collection.insert_one({"survey_responses": survey_responses})
    #result_label.configure(text="Responses submitted!")  # Confirmation message

# Main frame to hold survey pages
page_frame = customtkinter.CTkFrame(app)
page_frame.pack(fill="both", expand=True, pady=20)

# Navigation buttons
back_button = customtkinter.CTkButton(app, text="Back", command=prev_page)
next_button = customtkinter.CTkButton(app, text="Next", command=next_page)
submit_button = customtkinter.CTkButton(app, text="Submit", command=submit)

# Result label for submission status
result_label = customtkinter.CTkLabel(app, text="")
result_label.pack(pady=10)

# Load the first page
load_page()

# Run the app
app.mainloop()
