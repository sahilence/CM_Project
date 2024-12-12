import os
from groq import Groq

GROQ_API_KEY= "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"

client = Groq(
    api_key=GROQ_API_KEY,
)

with open("extracted.txt", "r") as file:
    extracted = file.read()
with open("ideal.txt", "r") as file:
    ideal = file.read()

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Judge the food product with following details: "+extracted+" based on the ideal standards: "+ideal+" and give a brief judgement in 100 words or less. Also give a healthy score out of 100.",
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)