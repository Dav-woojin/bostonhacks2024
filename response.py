from openai import OpenAI
from dotenv import load_dotenv
import sys, os
load_dotenv()
OPENAI_SECRET_KEY = os.getenv('OPENAI_SECRET_KEY')
client = OpenAI(api_key=OPENAI_SECRET_KEY)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message.content)