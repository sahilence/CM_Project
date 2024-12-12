import requests

# API endpoint and headers
url = "https://nutrition-calculator.p.rapidapi.com/api/nutrition-info"
headers = {
    "X-Rapidapi-Key": "b059a5abb8mshfd6f704ddfdc7bcp119fa8jsnabb5c6ab216f",  # Replace with your actual RapidAPI key
    "X-Rapidapi-Host": "nutrition-calculator.p.rapidapi.com"
}

# Query parameters
params = {
    "measurement_units": "std",
    "sex": "male",
    "age_value": "21",
    "age_type": "yrs",
    "feet": "5",
    "inches": "7",
    "lbs": "160",
    "activity_level": "Active"
}

# Make the GET request
try:
    print("Making the API request...")
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise an error for bad status codes
    data = response.json()  # Parse the JSON response
    print("API response received successfully!")

    # Print the response
    print("\nNutritional Information:")
    for key, value in data.items():
        print(f"{key}: {value}")

    with open("ideal.txt", "w", encoding="utf-8") as text_file:
        for key, value in data.items():
            text_file.write(f"{key}: {value}\n")

    print("\nData saved to 'ideal.txt'.")

except requests.exceptions.RequestException as e:
    print("An error occurred while making the API request:")
    print(e)
