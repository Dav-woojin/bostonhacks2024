from openai import OpenAI
from dotenv import load_dotenv
from server import database
import sys, os
load_dotenv()
OPENAI_SECRET_KEY = os.getenv('OPENAI_SECRET_KEY')
client = OpenAI(api_key=OPENAI_SECRET_KEY)
pref = database.get_pref()
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a motivational helper that is helping someone improve their emotional, phyiscal, and social health."},
        {
            "role": "user",
            "content": "Generate a small task for the user to do based on these {} preferences. Make 5 bullet points and keep each bullet point at 7 words".format(pref)
        }
    ]
)

print(completion.choices[0].message.content)