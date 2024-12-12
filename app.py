import torch
from transformers import BertTokenizer, BertForSequenceClassification
from flask import Flask, render_template, request, redirect, url_for
import os
from process_image import extract_nutritional_info
import json
from groq import Groq
import requests

# Load PubMedBERT tokenizer and model
MODEL_NAME = "microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract"
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)  # Binary classification

# API credentials and paths
GROQ_API_KEY = "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"
UPLOAD_FOLDER = 'static/uploads'
url = "https://nutrition-calculator.p.rapidapi.com/api/nutrition-info"
headers = {
    "X-Rapidapi-Key": "b059a5abb8mshfd6f704ddfdc7bcp119fa8jsnabb5c6ab216f",
    "X-Rapidapi-Host": "nutrition-calculator.p.rapidapi.com"
}
ideal = []
client = Groq(api_key=GROQ_API_KEY)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
health_data = {}

with open("sample_diabetic_patient_medical_record.json", 'r') as file:
    patient_data = json.load(file)

# Flask app
app = Flask(__name__)

# Function to predict food item quality
def predict_food_item(food_description):
    inputs = tokenizer(food_description, return_tensors="pt", truncation=True, padding="max_length", max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    return "Bad" if predicted_class == 1 else "Good"

@app.route('/', methods=['GET', 'POST'])
def health_info():
    global health_data
    if request.method == 'POST':
        height = request.form.get('height')
        sex = request.form.get('sex')
        weight = request.form.get('weight')
        age = request.form.get('age')
        conditions = request.form.get('conditions')

       
        health_data = {
            "measurement_units": "std",
            "sex": "male", #input from user
            "age_value": "12", #input from user
            "age_type": "yrs",
            "feet": "5", #input from user
            "inches": "7", #input from user
            "lbs": "160", #input from user
            "activity_level": "Active"
        }

        return redirect(url_for('upload_page'))

    return render_template('health_info.html', health_data=None)

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    global ideal
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Extract nutritional information
            print("check1")
            result = extract_nutritional_info(filepath)
            print("check2")

            food_quality = predict_food_item(result)
            print("check3")
            try:
                print("Making the API request...")
                response = requests.get(url, headers=headers, params=health_data)
                response.raise_for_status()  # Raise an error for bad status codes
                ideal = response.json()

            except requests.exceptions.RequestException as e:
                print("An error occurred while making the API request:")
                print(e)

            chat_completion = client.chat.completions.create(
            messages=[
                    {
                        "role": "user",
                        "content": f"Extract and organize information from this: \n {result}",
                    }
                ],
                model="llama3-8b-8192",
            )
            result = chat_completion.choices[0].message.content
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"Judge the food product with following details: {result} based on the ideal standards: {ideal} and patients medical history: {patient_data} and give a brief judgement in 100 words or less. Also give a healthy score out of 100. Think step by step."
                    }
                ],
                model="llama3-8b-8192",
            )
            # print(f"Judge the food product with following details: {result} based on the ideal standards: {ideal} and patients medical history: {patient_data} and give a brief judgement in 100 words or less. Also give a healthy score out of 100. Think step by step.")
            print("check4")
            judgment = chat_completion.choices[0].message.content

            return render_template('index.html', result=result, food_quality=food_quality, judgment=judgment)

    return render_template('index.html', result=None, food_quality=None, judgment=None)

if __name__ == '__main__':
    app.run(debug=True)
