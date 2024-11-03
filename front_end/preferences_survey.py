from tkinter import *
import customtkinter
from pymongo import MongoClient
import sys, os
from dotenv import load_dotenv
load_dotenv()
# MongoDB setup (use your correct MongoDB URI and database/collection name)

MONGO_USER = os.getenv('MONGO_USER')
MONGO_PW = os.getenv('MONGO_PW')

mongo_url = "mongodb+srv://{}:{}@cluster0.30uxb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0".format(MONGO_USER, MONGO_PW)
client = MongoClient(mongo_url)
db = client['mind_orbit_db']
collection = db['users']

# Initialize CustomTkinter app
customtkinter.set_appearance_mode("light")
app = customtkinter.CTk()
app.geometry("500x400")
app.title("Multi-Page Survey")

# Survey data structured by sections
survey_data = {
    "Physical": [
        {"question": "Select your favorite physical activities:", "options": ["Running", "Swimming", "Cycling"], "key": "exercise"},
        {"question": "How often do you exercise?", "options": ["Once a week", "Twice a week", "Three times a week"], "key": "frequency"},
        {"question": "What is your main fitness goal?", "options": ["Weight Loss", "Muscle Gain", "Endurance"], "key": "goal"},
    ],
    "Mental": [
        {"question": "Select your preferred mental activities:", "options": ["Reading", "Meditation", "Puzzles"], "key": "hobbies"},
    ],
    "Social": [
        {"question": "How often do you socialize with friends?", "options": ["Daily", "Weekly", "Monthly"], "key": "socialize"},
    ],
}

# Initialize variables
page_index = 0
current_section = "Physical"
responses = {section: {} for section in survey_data}  # Organize responses by section and question

# Function to load a page
def load_page():
    global page_index, current_section

    # Clear the current frame
    for widget in page_frame.winfo_children():
        widget.destroy()

    # Get the current question data
    question_data = survey_data[current_section][page_index]
    question = question_data["question"]
    options = question_data["options"]

    # Display section header
    section_header = customtkinter.CTkLabel(page_frame, text=current_section, font=("Arial", 16, "bold"))
    section_header.pack(pady=10)

    # Display the question
    question_label = customtkinter.CTkLabel(page_frame, text=question, font=("Arial", 14))
    question_label.pack(pady=10)

    # Display the options as checkboxes
    checkbox_vars = []
    for option in options:
        var = customtkinter.BooleanVar(value=responses[current_section].get(question_data["key"], {}).get(option, False))
        checkbox = customtkinter.CTkCheckBox(page_frame, text=option, variable=var)
        checkbox.pack(anchor="w", padx=20)
        checkbox_vars.append((option, var))

    # Save checkbox variables to responses
    responses[current_section][question_data["key"]] = {option: var for option, var in checkbox_vars}

    # Update navigation buttons
    back_button.pack_forget() if page_index == 0 and current_section == "Physical" else back_button.pack(side="left", padx=10)
    if current_section == "Social" and page_index >= len(survey_data[current_section]) - 1:
        next_button.pack_forget()
        submit_button.pack(pady=20)
    else:
        next_button.pack(side="right", padx=10)
        submit_button.pack_forget()

# Function to save responses
def save_responses():
    global page_index, current_section
    question_data = survey_data[current_section][page_index]
    key = question_data["key"]

    # Update responses with the current page's answers
    responses[current_section][key] = {option: var.get() for option, var in responses[current_section][key].items()}

# Navigation functions
def next_page():
    global page_index, current_section
    save_responses()  # Save current page responses
    page_index += 1

    if page_index >= len(survey_data[current_section]):
        if current_section == "Physical":
            current_section = "Mental"
        elif current_section == "Mental":
            current_section = "Social"
        page_index = 0

    load_page()  # Load the next page

def prev_page():
    global page_index, current_section
    save_responses()  # Save current page responses
    page_index -= 1

    if page_index < 0:
        if current_section == "Social":
            current_section = "Mental"
            page_index = len(survey_data["Mental"]) - 1
        elif current_section == "Mental":
            current_section = "Physical"
            page_index = len(survey_data["Physical"]) - 1
        else:
            page_index = 0

    load_page()  # Load the previous page

# Submit function to save data to MongoDB
def submit():
    save_responses()  # Save last page responses
    formatted_responses = {
        section: {key: [option for option, selected in options.items() if selected]
                  for key, options in questions.items()}
        for section, questions in responses.items()
    }
    collection.insert_one({"survey_responses": formatted_responses})  # Insert into MongoDB
    result_label.configure(text="Responses submitted!")  # Confirmation message

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
