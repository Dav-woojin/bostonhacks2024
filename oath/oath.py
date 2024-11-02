import tkinter as tk
from tkinter import messagebox
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
import json, os
from dotenv import load_dotenv
load_dotenv()

def google_sign_in():

    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    print(client_id)
    client_config = {
        "web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [redirect_uri]
        }
    }

    # Step 1: Set up the OAuth 2.0 flow
    print("hello")
    print(client_config)
    flow = InstalledAppFlow.from_client_config(
        client_config = client_config,
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
    )
    flow.redirect_uri = redirect_uri
    #authorization_url, _ = flow.authorization_url(prompt='conset')

    # Step 2: Open the browser for authentication
    credentials = flow.run_local_server(port=0)
    
    # Step 3: Retrieve user profile information if authenticated
    if credentials:
        # Obtain the ID token and access token
        access_token = credentials.token
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        # Get user info from Google APIs
        response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo', headers=headers)
        user_info = response.json()
        
        # Display user info in a Tkinter messagebox
        if response.ok:
            messagebox.showinfo("Login Successful", f"Welcome, {user_info['name']}!\nEmail: {user_info['email']}")
        else:
            messagebox.showerror("Login Failed", "Unable to retrieve user information")
    else:
        messagebox.showerror("Login Failed", "Could not sign in with Google")

# Tkinter GUI
root = tk.Tk()
root.title("Mental Health App")

sign_in_button = tk.Button(root, text="Sign in with Google", command=google_sign_in)
sign_in_button.pack(pady=20)

root.mainloop()
