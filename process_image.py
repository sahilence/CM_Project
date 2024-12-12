import pytesseract
from PIL import Image

# Ensure Tesseract-OCR is installed and its path is configured
# Example for Windows: pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_nutritional_info(image_path):
    # Open the image
    image = Image.open(image_path)
    
    # Use Tesseract OCR to extract text
    extracted_text = pytesseract.image_to_string(image)
    print(extracted_text)
    # Process the extracted text to find nutritional information
    nutritional_info = {}
    for line in extracted_text.splitlines():
        line = line.strip()
        if "Calories" in line:
            nutritional_info["Calories"] = line
        elif "Protein" in line:
            nutritional_info["Protein"] = line
        elif "Fat" in line:
            nutritional_info["Fat"] = line
        elif "Carbohydrate" in line or "Carbs" in line:
            nutritional_info["Carbohydrates"] = line

    # If no nutritional info is found, provide feedback
    if not nutritional_info:
        nutritional_info["Error"] = "No nutritional information could be extracted."

    return extracted_text


info = extract_nutritional_info(f"static\\uploads\\label.png")
with open("extracted.txt", "w") as file:
    file.write(info)

print("Text saved")