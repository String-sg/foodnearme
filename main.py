import streamlit as st
import requests
from random import sample
import re

# Streamlit interface
st.title('SG Restaurant Suggester')
postal_code = st.text_input('Enter postal code:', key='postal_code')


# Function to clean and validate postal code
def clean_postal_code(postal_code):
    # Remove non-numeric characters
    cleaned_code = re.sub(r'\D', '', postal_code)

    # Check if cleaned code has 6 digits
    if len(cleaned_code) == 6:
        return cleaned_code
    else:
        raise ValueError("Postal code must be 6 digits.")


try:
    cleaned_postal_code = clean_postal_code(postal_code)
    if postal_code != cleaned_postal_code:
        st.info(
            f"You have input {postal_code} but it has been cleaned as {cleaned_postal_code}")
except ValueError as e:
    st.warning(str(e))
    cleaned_postal_code = None

# function to get decompose postal code and use Google Maps API key


def geocode_postal_code(postal_code, api_key):
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={postal_code}&key={api_key}"

    response = requests.get(geocode_url)
    if response.status_code == 200:
        results = response.json()['results']
        if results:
            location = results[0]['geometry']['location']
            return f"{location['lat']},{location['lng']}"
        else:
            raise ValueError("No location found for the given postal code.")
    else:
        raise ConnectionError(
            f"Failed to connect to the Geocoding API: {response.status_code}")

# Function to get restaurants


def get_restaurants(postal_code):
    # Convert postal code to coordinates (latitude and longitude)
    # This can be done using a geocoding API or a service
    api_key = st.secrets["google_api_key"]
    coordinates = geocode_postal_code(postal_code, api_key)

    # Use the Places API to find restaurants within 2km of the coordinates
    places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={coordinates}&radius=2000&type=restaurant&key={api_key}"

    response = requests.get(places_url)
    results = response.json()['results']

    # Randomly select 5 restaurants
    restaurant_sample = sample(results, 5)

    return restaurant_sample

# Function to display restaurants


def display_restaurants(restaurant_list):
    # Sort the list by rating in descending order
    sorted_restaurants = sorted(
        restaurant_list, key=lambda x: x.get('rating', 0), reverse=True)

    for restaurant in sorted_restaurants:
        st.subheader(restaurant['name'])
        # Display rating if available
        rating = restaurant.get('rating')
        if rating:
            st.write(f"Rating: {rating} / 5 ⭐ ")
        else:
            st.write("Rating: Not available")


# Button to fetch and display restaurants
if cleaned_postal_code and st.button('Find Restaurants'):
    try:
        restaurants = get_restaurants(cleaned_postal_code)
        display_restaurants(restaurants)
    except Exception as e:
        st.error(f"Error: {e}")
