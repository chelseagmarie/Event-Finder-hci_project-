import streamlit as st
import requests
from streamlit_folium import folium_static
import folium

secret_key = "b4f78a34007609b69962e3e8257e1a80958f2db331713cc455e4e1253d13838b"
client_ID = "MzMxMjE3NDd8MTY4MTY5MDQwMS4yMzM1MjE1"

'''
color_picker = st.color_picker('Pick A Color')
'''

st.sidebar.title("Sidebar")

page_bg_color = """
        <style>
         [data-testid='stAppViewContainer'] > .main {
         background-color: #7EA884;}
         [data-testid="stSidebar"] > div:first-child {
         background-color: #000000;}
         [data-testid="stHeader"] {
         background: rgba(0,0,0,0);
         }
         </style>
         """
st.markdown(page_bg_color, unsafe_allow_html= True)




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

@st.cache_data
def genres_available():
    genres_set = set()
    url = f"https://api.seatgeek.com/2/genres?client_id={client_ID}"
    request = requests.get(url).json()
    for i in range(0,len(request["genres"])):
        genres_set.add(request["genres"][i]["name"])

    genres_list = list(genres_set)
    genres_list.sort()
    return genres_list

'''
@st.cache_data
def filter_perfomers_by_genre(genre):
    performers_set = set()
    url = f"https://api.seatgeek.com/2/performers?client_id={client_ID}&genres[primary].slug={genre}"
    request = requests.get(url).json()
    for i in range(0,len(request["performers"])):
        performers_set.add(request["performers"][i]["name"])
    return performers_set
'''

@st.cache_data
def concerts_happening_for_your_genre(genre):
    '''have yet to add part about location'''
    dude_set = set()
    url = f"https://api.seatgeek.com/2/events?client_id={client_ID}&type=concert&genres[primary].slug={genre}"
    request = requests.get(url).json()
    for i in range(0,len(request["events"])):
        dude_set.add(request["events"][i]["title"])
    return dude_set


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


st.write("Check Genre(s) of Interest")
check0 = st.checkbox(genres_available()[0])
check1 = st.checkbox(genres_available()[1])
check2 = st.checkbox(genres_available()[2])
check3 = st.checkbox(genres_available()[3])
check4 = st.checkbox(genres_available()[4])
check5 = st.checkbox(genres_available()[5])
check6 = st.checkbox(genres_available()[6])
check7 = st.checkbox(genres_available()[7])
check8 = st.checkbox(genres_available()[8])
check9 = st.checkbox(genres_available()[9])
check10 = st.checkbox(genres_available()[10])
check11 = st.checkbox(genres_available()[11])
check12 = st.checkbox(genres_available()[12])
check13 = st.checkbox(genres_available()[13])
check14 = st.checkbox(genres_available()[14])
check15 = st.checkbox(genres_available()[15])
check16 = st.checkbox(genres_available()[16])
check17 = st.checkbox(genres_available()[17])
check18 = st.checkbox(genres_available()[18])
check19 = st.checkbox(genres_available()[19])
check20 = st.checkbox(genres_available()[20])

selected = []
if check0:
    selected.append(genres_available()[0])
if check1:
    selected.append(genres_available()[1])
if check2:
    selected.append(genres_available()[2])
if check3:
    selected.append(genres_available()[3])
if check4:
    selected.append(genres_available()[4])
if check5:
    selected.append(genres_available()[5])
if check6:
    selected.append(genres_available()[6])
if check7:
    selected.append(genres_available()[7])
if check8:
    selected.append(genres_available()[8])
if check9:
    selected.append(genres_available()[9])
if check10:
    selected.append(genres_available()[10])
if check11:
    selected.append(genres_available()[11])
if check12:
    selected.append(genres_available()[12])
if check13:
    selected.append(genres_available()[13])
if check14:
    selected.append(genres_available()[14])
if check15:
    selected.append(genres_available()[15])
if check16:
    selected.append(genres_available()[16])
if check17:
    selected.append(genres_available()[17])
if check18:
    selected.append(genres_available()[18])
if check19:
    selected.append(genres_available()[19])
if check20:
    selected.append(genres_available()[20])

st.write("Concerts happening for your genre!")

for genre in selected:
    st.write(concerts_happening_for_your_genre(genre))




    