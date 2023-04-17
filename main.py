import streamlit as st
import requests
from streamlit_folium import folium_static
import folium

secret_key = "b4f78a34007609b69962e3e8257e1a80958f2db331713cc455e4e1253d13838b"
client_ID = "MzMxMjE3NDd8MTY4MTY5MDQwMS4yMzM1MjE1"


@st.cache_data
def map_creator(latitude, longitude):
    # center on the station
    m = folium.Map(location=[latitude, longitude], zoom_start=10)

    # add marker for the station
    folium.Marker([latitude, longitude], popup="Venue", tooltip="Venue").add_to(m)

    folium_static(m)


@st.cache_data
def get_country():
    country_set = set()
    country_set.add("")
    ur_mom = f"https://api.seatgeek.com/2/venues?client_id={client_ID}"
    idk = requests.get(ur_mom).json()
    for i in range(0, len(idk["venues"])):
        country_set.add(idk["venues"][i]["country"])

    return country_set


@st.cache_data
def get_state(country_selected):
    state_set = set()
    state_set.add("")
    ur_mom = f"https://api.seatgeek.com/2/venues?client_id={client_ID}&country={country_selected}"
    idk = requests.get(ur_mom).json()
    for i in range(0, len(idk["venues"])):
        state_set.add(idk["venues"][i]["state"])

    return state_set


@st.cache_data
def get_city(state_selected):
    city_set = set()
    city_set.add("")
    ur_mom = f"https://api.seatgeek.com/2/venues?client_id={client_ID}&state={state_selected}"
    idk = requests.get(ur_mom).json()
    for i in range(0, len(idk["venues"])):
        city_set.add(idk["venues"][i]["city"])

    return city_set


@st.cache_data
def venues_setlist(city_selected):
    venues_set = set()
    ur_mom = f"https://api.seatgeek.com/2/venues?client_id={client_ID}&city={city_selected}"
    idk = requests.get(ur_mom).json()
    for i in range(0, len(idk["venues"])):
        venues_set.add(idk["venues"][i]["name"])

    return venues_set


# Events
st.title("Events Near You!")

country = st.selectbox("Select a country: ", options=get_country())

if country:
    state = st.selectbox("Select a State: ", options=get_state(country))

    if state:
        city = st.selectbox("Select a City: ", options=get_city(state))

        if city:
            st.subheader("List of Venues Near you!")
            st.write(venues_setlist(city))
            map_creator(26, -80.15)