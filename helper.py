import streamlit as st


def get_ellipse_coords(point: tuple[int, int]) -> tuple[int, int, int, int]:
    center = point
    radius = 10
    return (
        center[0] - radius,
        center[1] - radius,
        center[0] + radius,
        center[1] + radius,
    )

def flip_court(current_court):
    print('fliing court')
    if current_court == "img/bball_court_north.png":
        st.session_state['current_court'] = "img/bball_court_south.png"
    else:
        st.session_state['current_court'] = "img/bball_court_north.png"


def flip_coordinates(image_size, original_coords):
    center_x = image_size[0] / 2
    center_y = image_size[1] / 2

    # Calculate the new flipped coordinates
    flipped_x = center_x - (original_coords[0] - center_x)
    flipped_y = center_y - (original_coords[1] - center_y)

    return flipped_x, flipped_y