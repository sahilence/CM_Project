from flask import Flask, render_template, request, redirect, url_for
import os
from process_image import extract_nutritional_info

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def health_info():
    if request.method == 'POST':
        # Collect health information from the form
        height = request.form.get('height')
        weight = request.form.get('weight')
        age = request.form.get('age')
        conditions = request.form.get('conditions')

        # Example: Process the information or store it in a database
        health_data = {
            'Height': height,
            'Weight': weight,
            'Age': age,
            'Medical Conditions': conditions
        }

        # Redirect to the upload page
        return redirect(url_for('upload_page'))

    return render_template('health_info.html', health_data=None)

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Extract nutritional information from the uploaded image
            result = extract_nutritional_info(filepath)

            # Pass the extracted information to the template
            return render_template('index.html', result=result)

    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)
