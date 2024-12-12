import pytesseract
from PIL import Image
import re
# Ensure Tesseract-OCR is installed and its path is configured
# Example for Windows: pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_nutritional_info(image_path):
    # Open the image
    image = Image.open(image_path)
    
    # Use Tesseract OCR to extract text
    ocr_text = pytesseract.image_to_string(image)
    print(ocr_text)
    # Initialize a dictionary to store the extracted information
    nutrition_info = {
        "Serving Size": None,
        "Servings Per Container": None,
        "Calories Per Serving": None,
        "Calories Per Container": None,
        "Nutrients": {}
    }
    
    # Extract serving size
    serving_size_match = re.search(r"Serving size\s+([\d/]+\s\w+|\w+ \w+)", ocr_text, re.IGNORECASE)
    if serving_size_match:
        nutrition_info["Serving Size"] = serving_size_match.group(1).strip()
    
    # Extract servings per container
    servings_match = re.search(r"(\d+)\s+servings? per container", ocr_text, re.IGNORECASE)
    if servings_match:
        nutrition_info["Servings Per Container"] = servings_match.group(1).strip()
    
    # Extract calories per serving and per container
    calories_match = re.findall(r"Calories[^\d]*(\d+)", ocr_text)
    if calories_match:
        if len(calories_match) >= 2:
            nutrition_info["Calories Per Serving"] = calories_match[0].strip()
            nutrition_info["Calories Per Container"] = calories_match[1].strip()
        elif len(calories_match) == 1:
            nutrition_info["Calories Per Serving"] = calories_match[0].strip()
    
    # Extract nutrient details
    nutrient_lines = ocr_text.splitlines()
    for line in nutrient_lines:
        # Match patterns like "Total Fat 5g 13%"
        nutrient_match = re.match(r"([\w\s]+)\s+([\d\.]+)(\w+)\s+(\d+)%?", line.strip(), re.IGNORECASE)
        if nutrient_match:
            nutrient_name = nutrient_match.group(1).strip()
            nutrient_amount = nutrient_match.group(2).strip() + nutrient_match.group(3).strip()
            daily_value = nutrient_match.group(4).strip() + "%"
            nutrition_info["Nutrients"][nutrient_name] = {
                "Amount": nutrient_amount,
                "Daily Value": daily_value
            }
    
    # Extract additional nutrients (Vitamin D, Calcium, etc.)
    vitamin_matches = re.findall(r"([\w\s]+)\s+([\d\.]+)(\w+)\s+(\d+)%?", ocr_text, re.IGNORECASE)
    for vitamin in vitamin_matches:
        nutrient_name, nutrient_amount, unit, daily_value = vitamin
        if nutrient_name not in nutrition_info["Nutrients"]:
            nutrition_info["Nutrients"][nutrient_name.strip()] = {
                "Amount": nutrient_amount.strip() + unit.strip(),
                "Daily Value": daily_value.strip() + "%"
            }

    return nutrition_info


    
# Use this if you want to hardcode
# info = extract_nutritional_info(f"static\\uploads\\label.png")
# with open("extracted.txt", "w") as file:
#     file.write(info)

# print("Text saved")
