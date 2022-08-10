import streamlit as st
import random
import pandas as pd
import pydeck as pdk

df_data = pd.read_csv('../techlabs_merging/merged_data.csv', index_col=0)
df_data = df_data.loc[:, ['x', 'y', 'type']]
st.title("Easy Parking")

address_query = st.text_input("Enter your destination", value='Cologne')

selected_types = st.multiselect(
     'What do you want to see around your destination?',
     df_data.type.unique(), default=df_data.type.unique())
    
type_mask = df_data.type.isin(selected_types)

# Filter data for selected types
df_data = df_data[type_mask]

@st.cache
def generate_random_hexcolor(type):
    return "#%06x" % random.randint(0, 0xFFFFFF)

def hex_color_to_rgb_list(hex_color):
    """
    Given a hex color like #00FF33, returns an array with decimal numbers like [0, 256, 0]
    """
    return list(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

colors = {}

if df_data.type.nunique() > 0: # If user deselects all options, ignore showing color pickers for data points to avoid crash
    cols = st.columns(df_data.type.nunique())
    for i, type in enumerate(df_data.type.unique()):
        with cols[i]:
            hex_color = st.color_picker(type, value=generate_random_hexcolor(type))
            rgb_list = hex_color_to_rgb_list(hex_color)
            rgba_list = rgb_list + [200] # add fixed alpha value as last element
            colors[type] = rgba_list

layers = [
         pdk.Layer(
             'ScatterplotLayer',
             data=df_data[df_data['type']==type],
             get_position='[x, y]',
             get_color=f'{color}',
             get_radius=15,
         )
         for type, color in colors.items()
     ]

@st.cache # Don't query the geocode service for the same address again and again
def get_address_coordinate(query):
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent='map')

    location = geolocator.geocode(query)
    return (location.longitude, location.latitude)

queried_location = get_address_coordinate(address_query)
df_queried_location = pd.DataFrame(queried_location , index=['x','y']).T

user_input_address = pdk.Layer(
    'ScatterplotLayer',
    data=df_queried_location,
    get_position='[x, y]',
    get_color='[100, 100, 100, 200]',
    get_radius=100,
)
layers.append(user_input_address)

st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         longitude=queried_location[0],
         latitude=queried_location[1],
         zoom=14,
         pitch=0,
     ),
     layers=layers,
 ))