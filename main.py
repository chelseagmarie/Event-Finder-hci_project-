import streamlit as st
import requests
from streamlit_folium import folium_static
import folium
import pandas as pd
import altair as alt

secret_key = "b4f78a34007609b69962e3e8257e1a80958f2db331713cc455e4e1253d13838b"
client_ID = "MzMxMjE3NDd8MTY4MTY5MDQwMS4yMzM1MjE1"
selected = []

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
def map_creator(locations):
    m = folium.Map(location=[locations[0][0], locations[0][1]], zoom_start=10)
    for lat, long in locations:
        folium.Marker([lat, long], popup="Venue", tooltip="Venue").add_to(m)
    folium_static(m)
    

@st.cache_data
def get_country():
    country_set = set()
    country_lst = [""]
    country_set.add("")
    url = f"https://api.seatgeek.com/2/venues?client_id={client_ID}"
    info = requests.get(url).json()
    for i in range(0, len(info["venues"])):
        if info["venues"][i]["country"] not in country_set:
            country_lst.append(info["venues"][i]["country"])
            country_set.add(info["venues"][i]["country"])

    return country_lst


@st.cache_data
def get_state(country_selected):
    state_set = set()
    state_set.add("")
    state_list = [""]
    url = f"https://api.seatgeek.com/2/venues?client_id={client_ID}&country={country_selected}"
    info = requests.get(url).json()
    for i in range(0, len(info["venues"])):
        if info["venues"][i]["state"] not in state_set:
            state_list.append(info["venues"][i]["state"])
            state_set.add(info["venues"][i]["state"])

    return state_list


@st.cache_data
def get_city(state_selected):
    city_set = set()
    city_list=[""]
    city_set.add("")
    url = f"https://api.seatgeek.com/2/venues?client_id={client_ID}&state={state_selected}"
    info = requests.get(url).json()
    for i in range(0, len(info["venues"])):
        if info["venues"][i]["city"] not in city_set:
            city_list.append(info["venues"][i]["city"])
            city_set.add(info["venues"][i]["city"])

    return city_list

@st.cache_data
def get_event_date(sort, month, year):
    events_set = set()
    url = f'https://api.seatgeek.com/2/events?client_id={client_ID}&{sort}.gte={year}-{month}-01&{sort}.lte={year}-{month}-30'
    info = requests.get(url).json()
    for i in range(0, len(info["events"])):
    
        events_set.add(info["events"][i]["name"])

    return events_set

@st.cache_data
def venues_setlist(city_selected):
    venues_set = set()
    venues_list=[]
    url = f"https://api.seatgeek.com/2/venues?client_id={client_ID}&city={city_selected}"
    info = requests.get(url).json()
    for i in range(0, len(info["venues"])):
        if info["venues"][i]["name"] not in venues_set:
            venues_set.add(info["venues"][i]["name"])
            venues_list.append(info["venues"][i]["name"])

    return venues_list

def venue_eventlist(venue_name):
    event_list=[]
    url = f"https://api.seatgeek.com/2/events?client_id={client_ID}&venue.name={venue_name}&sort=score.asc"
    info = requests.get(url).json()
    for i in range(0, len(info["events"])):
        event_list.append(info["events"][i]["title"])
    return event_list

def venue_eventscore(venue_name):
    score_list=[]
    url = f"https://api.seatgeek.com/2/events?client_id={client_ID}&venue.name={venue_name}&sort=score.asc"
    info = requests.get(url).json()
    for i in range(0, len(info["events"])):
        score_list.append(info["events"][i]["score"])
    return score_list

def table_chart(selected_city):
    venue_names=venues_setlist(selected_city)
    tabs=st.tabs(venue_names)
    hi=tabs[0]
    venue_events=[]
    scores=[]
    for i in venue_names:
        venue=[i]
        score=[i]
        for k in venue_eventlist(i):
            venue.append(k)
        for m in venue_eventscore(i):
            score.append(m)
        
        scores.append(score)
        venue_events.append(venue)
    #for i in venue_names:
            #st.write(venue_events)
    df=pd.DataFrame()
    #st.write(scores)


@st.cache_data
def venues_setlist_coord(city_selected):
    venues_set_coord = dict()
    url = f"https://api.seatgeek.com/2/venues?client_id={client_ID}&city={city_selected}"
    info = requests.get(url).json()
    for i in range(0, len(info["venues"])):
        venues_set_coord[(info["venues"][i]["location"]["lat"])] = info["venues"][i]["location"]["lon"]
    locations = [(lat, lon) for lat, lon in venues_set_coord.items()]
    
    return locations
    
@st.cache_data
def get_type(city_selected):
    category_set=set()
    url = f"https://api.seatgeek.com/2/events?client_id={client_ID}&venue.city={city_selected}"
    data = requests.get(url).json()
    for i in range(0, len(data["events"])):
        for k in range(0,len(data["events"][i]["taxonomies"])):
            category_set.add(data["events"][i]["taxonomies"][k]["name"])
    return category_set

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

@st.cache_data
def concerts_happening_for_your_genre(genre, miles, sort):
    dude_set = set()
    dude_list=[]
    url = f"https://api.seatgeek.com/2/events?client_id={client_ID}&geoip=true&type=concert&genres[primary].slug={genre}&sort={sort}"
    request = requests.get(url).json()
    #st.write(request)
    for i in range(0,len(request["events"])):
        if request["events"][i]["title"] not in dude_set:
            dude_set.add(request["events"][i]["title"])
            dude_list.append(request["events"][i]["title"])
    if not dude_list:
        st.error(f"Sorry. There are no events of {genre} in your area.")
        return ""
    st.info(genre)
    return st.success(f" The {genre} events are {dude_list}")


@st.cache_data
def filter_perfomers_by_genre(genre):
    performers_set = set()
    url = f"https://api.seatgeek.com/2/performers?client_id={client_ID}&genres[primary].slug={genre}"
    request = requests.get(url).json()
    for i in range(0,len(request["performers"])):
        performers_set.add(request["performers"][i]["name"])
    return performers_set


# Events
st.title("Events Near You!")

@st.cache_data
def display(selected):
    st.header("Concerts happening for your genre(s)!")
    
    for genre in selected:
        st.write(concerts_happening_for_your_genre(genre,miles=None,sort=sort))

    if selected:
        st.header("Number of Performances Happening in Your Area for Your Genres")
        st.altair_chart(bar_chart(selected), use_container_width=True)


miles = st.sidebar.slider(label="Select a distance (Mi.):",min_value=5,max_value=100,value=30,step=5)
loco=st.sidebar.selectbox("Search By",options={"","Location(Country,State,City)","Geolocation"})

radio = st.sidebar.radio("Sort by:", ("Popularity","Date"))

if radio == "Popularity":
    sort = "score.desc"
elif radio == "Date":
    sort = "datetime_local.desc"
    month = st.number_input("Insert Month in MM format:")
    year = st.number_input("Insert year in YYYY format:")
    url = f'https://api.seatgeek.com/2/events?client_id={client_ID}&{sort}.gte={year}-{month}-01&{sort}.lte={year}-{month}-30'

    st.info(f"Events during that month are {get_event_date(sort, month, year)}")


# bar chart
# number of performers in your area vs genre

@st.cache_data
def num_performers_in_area_per_genre(genre, miles):
    perf_set = set()
    url = f"https://api.seatgeek.com/2/events?client_id={client_ID}&geoip=true&type=concert&genres[primary].slug={genre}&sort={sort}"
    request = requests.get(url).json()
    #st.write(request)
    for i in range(0,len(request["events"])):
        if request["events"][i]["title"] not in perf_set:
            perf_set.add(request["events"][i]["title"])
    if not perf_set:
        return 0
    return len(perf_set)
  

def bar_chart(selected):
    num_lst = []
    genre_lst = []

    if selected:
        for genre in selected:
            genre_lst.append(genre)
            num_lst.append(num_performances_in_area_per_genre(genre, miles= None))

        df = pd.DataFrame({
            "Number of Performances in Your Area" : num_lst,
            "Genre" : genre_lst
        })

        chart = alt.Chart(df).mark_bar().encode(
            y = 'Number of Performances in Your Area:Q',
            x = "Genre:O",
        )

    
    return chart


st.sidebar.write("Check Genre(s) of Interest")
check0 = st.sidebar.checkbox(genres_available()[0])
check1 = st.sidebar.checkbox(genres_available()[1])
check2 = st.sidebar.checkbox(genres_available()[2])
check3 = st.sidebar.checkbox(genres_available()[3])
check4 = st.sidebar.checkbox(genres_available()[4])
check5 = st.sidebar.checkbox(genres_available()[5])
check6 = st.sidebar.checkbox(genres_available()[6])
check7 = st.sidebar.checkbox(genres_available()[7])
check8 = st.sidebar.checkbox(genres_available()[8])
check9 = st.sidebar.checkbox(genres_available()[9])
check10 = st.sidebar.checkbox(genres_available()[10])
check11 = st.sidebar.checkbox(genres_available()[11])
check12 = st.sidebar.checkbox(genres_available()[12])
check13 = st.sidebar.checkbox(genres_available()[13])
check14 = st.sidebar.checkbox(genres_available()[14])
check15 = st.sidebar.checkbox(genres_available()[15])
check16 = st.sidebar.checkbox(genres_available()[16])
check17 = st.sidebar.checkbox(genres_available()[17])
check18 = st.sidebar.checkbox(genres_available()[18])
check19 = st.sidebar.checkbox(genres_available()[19])
check20 = st.sidebar.checkbox(genres_available()[20])


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


if loco=="Location(Country,State,City)":
    country = st.selectbox("Select a country: ", options=get_country())

    if country:
        state = st.selectbox("Select a State: ", options=get_state(country))

        if state:
            city = st.selectbox("Select a City: ", options=get_city(state))

            if city:
                st.subheader("List of Venues Near you!")
                st.write(venues_setlist(city))
                st.info(get_type(city))
                st.selectbox("Event type: ", options=get_type(city))
                map_creator(venues_setlist_coord(city))
                display(selected)

if loco =="Geolocation":
    venues=[]
    venues_set=set()
    Location_Dict = dict()
    #miles=st.select_slider("Select a distance (Mi.)",options=[5,10,15,20,25,30,35,40,45,50,55,60])
    url=f"https://api.seatgeek.com/2/venues?client_id={client_ID}&geoip=true&range={miles}mi"
    request=requests.get(url).json()
    for i in range(0,len(request["venues"])):
        if request["venues"][i]["name"] not in venues_set:
            venues_set.add(request["venues"][i]["name"])
            venues.append(request["venues"][i]["name"])
            Location_Dict[request["venues"][i]["location"]["lat"]] = request["venues"][i]["location"]["lon"]
    st.info(f"The venues near you are {venues}")
    locations = [(lat, lon) for lat, lon in Location_Dict.items()]
    map_creator(locations)
    display(selected)

