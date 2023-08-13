import streamlit as st
from streamlit_pills import pills
import pandas as pd
from PIL import Image, ImageDraw
from helper import get_ellipse_coords, flip_court, flip_coordinates

from streamlit_image_coordinates import streamlit_image_coordinates

st.set_page_config(
    page_title="Shot + Rebound Location Tracker",
    page_icon="🏀",
    layout="wide"
)

"# :basketball: Shot & Rebound Location Tracker"

if 'shot_location' not in st.session_state:
    st.session_state['shot_location'] = ()

if 'rebound_location' not in st.session_state:
    st.session_state['rebound_location'] = ()

if 'data' not in st.session_state:
    data = pd.DataFrame(columns=['shot_x', 'shot_y', 'rebound_x', 'rebound_y'])
    st.session_state['data'] = data

if 'old_value' not in st.session_state:
    st.session_state['old_value'] = None

if 'current_court' not in st.session_state:
    st.session_state['current_court'] = "img/bball_court_north.png"

data = st.session_state['data']

selected = pills("Shot or Rebound", ["Shot", "Rebound"])

# if st.button('🔄'):
#     flip_court(st.session_state['current_court'])

# bball_court_north.png is 765×722
with Image.open(st.session_state['current_court']) as img:
    draw = ImageDraw.Draw(img)

    if st.session_state['shot_location']:
        coords = get_ellipse_coords(st.session_state['shot_location'])
        draw.ellipse(coords, fill="red")
        draw.text((coords[0], coords[1] + 25),
                  '({}, {})'.format(st.session_state['shot_location'][0], st.session_state['shot_location'][1]),
                  fill="black")
    if st.session_state['rebound_location']:
        coords = get_ellipse_coords(st.session_state['rebound_location'])
        draw.ellipse(coords, fill="blue")
        draw.text((coords[0], coords[1] + 25),
                  '({}, {})'.format(st.session_state['rebound_location'][0], st.session_state['rebound_location'][1]),
                  fill="black")

    value = streamlit_image_coordinates(img, key='pil')

    if value != st.session_state['old_value']:
        st.session_state['old_value'] = value
        point = value["x"], value["y"]

        if point != st.session_state["shot_location"] and point != st.session_state["rebound_location"]:
            if selected == "Shot":
                st.session_state["shot_location"] = point
            elif selected == "Rebound":
                st.session_state["rebound_location"] = point
            st.experimental_rerun()

if st.button('Clear'):
    st.session_state['shot_location'] = ()
    st.session_state['rebound_location'] = ()
    st.experimental_rerun()

if st.button('Add Row', type="primary"):
    if st.session_state['shot_location'] and st.session_state['rebound_location']:
        row = pd.DataFrame({'shot_x': [st.session_state['shot_location'][0]],
                            'shot_y': [st.session_state['shot_location'][1]],
                            'rebound_x': [st.session_state['rebound_location'][0]],
                            'rebound_y': [st.session_state['rebound_location'][1]]})
        st.session_state['data'] = pd.concat([st.session_state['data'], row])
        st.session_state['data'].reset_index(drop=True, inplace=True)

        # Clear shot and rebound location
        st.session_state['shot_location'] = ()
        st.session_state['rebound_location'] = ()
        st.experimental_rerun()
    else:
        st.error("Please select a shot and a rebound location")

st.data_editor(data, width=1000, num_rows='dynamic')

st.download_button(
    "⬇️ Download Data",
    data.to_csv().encode('utf-8'),
    "data.csv",
    "text/csv",
    key='download-csv'
)
