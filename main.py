import streamlit as st
import requests
from random import sample
import re

# Streamlit interface
st.title('SG Restaurant Suggester')
input_postal_code = st.text_input('Enter postal code:', key='postal_code')

# Clean and validate postal code
# Remove non-numeric characters
cleaned_postal_code = re.sub(r'\D', '', input_postal_code)

if len(cleaned_postal_code) != 6 and input_postal_code != '':
    st.warning("Postal code must be 6 digits.")
    cleaned_postal_code = None  # Invalidate if not 6 digits
elif input_postal_code != cleaned_postal_code:
    st.info(
        f"You have input {input_postal_code} but it has been cleaned as {cleaned_postal_code}")

# function to get decompose postal code and use Google Maps API key

print(cleaned_postal_code)


def geocode_postal_code(cleaned_postal_code, api_key):
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={cleaned_postal_code}&key={api_key}"

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


def get_restaurants(cleaned_postal_code):
    # Convert postal code to coordinates (latitude and longitude)
    # This can be done using a geocoding API or a service
    api_key = st.secrets["google_api_key"]
    coordinates = geocode_postal_code(cleaned_postal_code, api_key)

    # Use the Places API to find restaurants within 2km of the coordinates
    places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={coordinates}&radius=2000&type=restaurant&key={api_key}"

    response = requests.get(places_url)
    results = response.json()['results']

    # Sample up to 5 restaurants, or fewer if not enough results
    num_restaurants_to_sample = min(5, len(results))
    restaurant_sample = sample(results, num_restaurants_to_sample)

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
