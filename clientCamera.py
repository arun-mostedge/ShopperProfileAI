import streamlit as st
import face_recognition as frg
import yaml
from utils import recognize, build_dataset,submitNew, get_info_from_id, deleteOne
from camera_input_live import camera_input_live
import numpy as np
import cv2

TOLERANCE = st.sidebar.slider("Tolerance",0.0,1.0,0.6,0.01)


FRAME_WINDOW = st.image([])
add_btn = st.button("Add", key="Add_btn")
stop_btn = st.button("Stop Tracking", key="Stop_btn")

image = camera_input_live(height= 530, width= 704,show_controls= False)

if image is not None:
    bytes_data = image.getvalue()
    image = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    # image = frg.load_image_file(image)
    image, name, id = recognize(image, TOLERANCE)
    # Display name and ID of the person

    #name_container.info(f"Name: {name}")
    #id_container.success(f"ID: {id}")
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    FRAME_WINDOW.image(image)

