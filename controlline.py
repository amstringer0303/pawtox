import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# converting zip code to coordinates 
def get_coordinates_from_zip(zip_code):
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "key": API_KEY,  
        "address": zip_code
    }
    response = requests.get(endpoint, params=params)
    
    if response.status_code == 200:
        results = response.json().get("results")
        if results:
            location = results[0]["geometry"]["location"]
            return location["lat"], location["lng"]
        else:
            print("No location found for zip code.")
            return None
    else:
        print("Error with Geocoding API request:", response.status_code, response.text)
        return None

# finding nearest open vet clinics based on coordinates 
def find_open_vet_clinics(latitude, longitude):
    location = f"{latitude},{longitude}"
    radius = 10000  # Search radius in meters
    endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": "YOUR_GOOGLE_PLACES_API_KEY",
        "location": location,
        "radius": radius,
        "type": "veterinary_care",
        "opennow": True
    }
    
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        clinics = response.json().get("results", [])
        
        # Print debug information
        print("Response from Google Places API:", response.json())
        
        if clinics:
            clinic_info = [{"name": clinic["name"], "address": clinic["vicinity"]} for clinic in clinics]
            print("Open Clinics Nearby:", clinic_info)
            return clinic_info
        else:
            print("No open clinics found.")
            return []
    else:
        print("Error in API request:", response.status_code, response.text)
        return []

# function to fetch open vet clinics based on zip code
def get_open_vet_clinics_by_zip(zip_code):
    coordinates = get_coordinates_from_zip(zip_code)
    if coordinates:
        latitude, longitude = coordinates
        return find_open_vet_clinics(latitude, longitude)
    else:
        print("Could not retrieve coordinates for the provided zip code.")
        return []


zip_code = input("Please provide your zip code: ")
open_clinics = get_open_vet_clinics_by_zip(zip_code)
print("Open Clinics Nearby:", open_clinics)