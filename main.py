import streamlit as st
import requests
from random import sample
import re
from streamlit_star_rating import st_star_rating
from sqlalchemy import create_engine

import psycopg2

conn = psycopg2.connect(st.secrets["DATABASE_URL"])

# Initialize session state
if 'restaurants' not in st.session_state:
    st.session_state['restaurants'] = None

# Streamlit interface
st.title('SG Restaurant Suggester')
input_postal_code = st.text_input('Enter postal code:', key='postal_code')

# Clean and validate postal code
cleaned_postal_code = re.sub(r'\D', '', input_postal_code)

if len(cleaned_postal_code) != 6 and input_postal_code != '':
    st.warning("Postal code must be 6 digits.")
    cleaned_postal_code = None  # Invalidate if not 6 digits
elif input_postal_code != cleaned_postal_code:
    st.info(
        f"You have input {input_postal_code} but it has been cleaned as {cleaned_postal_code}")

# for users planning to fork this + replace with their own DB, this ensures that the  table is created


# Function to execute a query
def execute_query(query, params=None, is_select=False):
    with conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if is_select:
                return cur.fetchall()


def create_ratings_table():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS ratings (
        id SERIAL PRIMARY KEY,
        rating INT NOT NULL
    )
    '''
    execute_query(create_table_query)


# this function runs to ensure that the table ratings exist
create_ratings_table()


# Function to insert a rating
def insert_rating(rating):
    execute_query('INSERT INTO ratings (rating) VALUES (%s)', (rating,))

# Function to get the average rating


def get_average_rating():
    result = execute_query('SELECT AVG(rating) FROM ratings', is_select=True)
    return result[0][0] if result else None

# function to get decompose postal code and use Google Maps API key


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

    # Use the Places API to find restaurants within 1km of the coordinates
    places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={coordinates}&radius=1000&type=restaurant&key={api_key}"

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
        # Get Place ID
        place_id = restaurant['place_id']
        profile_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
        st.markdown(f"[{restaurant['name']}]({profile_url})",
                    unsafe_allow_html=True)

        # Display rating and number of reviews if available
        rating = restaurant.get('rating')
        num_reviews = restaurant.get('user_ratings_total', 'Not available')
        if rating:
            st.write(f"Rating: {rating} / 5 ⭐ ({num_reviews})")
        else:
            st.write("Rating: Not available")

        # Display hyperlink


# Button to fetch and display restaurants
if cleaned_postal_code and st.button('Find Restaurants'):
    try:
        st.session_state['restaurants'] = get_restaurants(cleaned_postal_code)
    except Exception as e:
        st.error(f"Error: {e}")

if st.session_state['restaurants']:
    display_restaurants(st.session_state['restaurants'])
    st.markdown("""---""")
    # Use a callback mechanism or check for change in value
    rating = st_star_rating("Please rate your experience",
                            maxValue=10, defaultValue=0, key="rating")

    # Check if a rating is selected
    if rating:
        # Insert the rating into the database
        insert_rating(rating)
        avg_rating = get_average_rating()
        if avg_rating is not None:
            st.success(
                f'Thank you for your review! The average rating is {avg_rating:.2f}/10.')
        else:
            st.info("No ratings available yet.")
