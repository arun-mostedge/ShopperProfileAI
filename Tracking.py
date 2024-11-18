
import streamlit as st
import cv2
import face_recognition as frg
import yaml 
from utils import recognize, build_dataset,submitNew, get_info_from_id, deleteOne
from camera_input_live import camera_input_live
import numpy as np

# Path: code\app.py

st.set_page_config(
    page_title="Mostedge Face Recognition Solution",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.mostedge.com/',
        'About': "# This is a *SaaS* based store monitoring solution app, developed by:orange[***Mostedge***]!",
    }
)
st.image('logo.png')
#Config
cfg = yaml.load(open('config.yaml','r'),Loader=yaml.FullLoader)
PICTURE_PROMPT = cfg['INFO']['PICTURE_PROMPT']
WEBCAM_PROMPT = cfg['INFO']['WEBCAM_PROMPT']



st.sidebar.title("Settings")
#Create a menu bar
menu = ["Webcam","Picture"]
choice = st.sidebar.selectbox("Input type",menu)
#Put slide to adjust tolerance
TOLERANCE = st.sidebar.slider("Tolerance",0.0,1.0,0.6,0.01)
st.sidebar.info("Tolerance is the threshold for face recognition. The lower the tolerance, the more strict the face recognition. The higher the tolerance, the more loose the face recognition.")

#Infomation section 
st.sidebar.title("Visitor Information")
name_container = st.sidebar.empty()
id_container = st.sidebar.empty()
name_container.info('Name: Unnknown')
id_container.success('ID: Unknown')
if choice == "Picture":
    st.title("Face Recognition App")
    st.write(PICTURE_PROMPT)
    uploaded_images = st.file_uploader("Upload",type=['jpg','png','jpeg'],accept_multiple_files=True)
    if len(uploaded_images) != 0:
        #Read uploaded image with face_recognition
        for image in uploaded_images:
            image = frg.load_image_file(image)
            image, name, id = recognize(image,TOLERANCE) 
            name_container.info(f"Name: {name}")
            id_container.success(f"ID: {id}")
            st.image(image)
    else: 
        st.info("Please upload an image")
    
elif choice == "Webcam":
    #st.title("Face Recognition App")
    #st.write(WEBCAM_PROMPT)

    accesspoint = st.selectbox(
        "What will be your favorite monitoring camera?",
        ("Webcam", "Static IP Camera", "Mobile IP Camera")
    )
    cam = None
    FRAME_WINDOW = st.image([])
    add_btn = st.button("Add", key="Add_btn")
    stop_btn = st.button("Stop Tracking", key="Stop_btn")
    if accesspoint == "Webcam":
        image = camera_input_live(height= 530, width= 704,show_controls= False)
        if image is not None and not stop_btn:
            bytes_data = image.getvalue()
            image = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            image, name, id = recognize(image, TOLERANCE)
            # Display name and ID of the person

            name_container.info(f"Name: {name}")
            id_container.success(f"ID: {id}")
            #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(image)

            if add_btn:
                ret = submitNew('Unknow', id, image)
                if ret == 1:
                    st.success("Person Added")
                elif ret == 0:
                    st.error("Person ID already exists")
                elif ret == -1:
                    st.error("There is no face in the picture")

        # if image:
        #     st.image(image)
        # webcamno = st.number_input('Number of webcam to add, incase you had multiple webcam attached with your device:',min_value=0,max_value=3,step=1)
        # if webcamno != None:
        #     cam = cv2.VideoCapture(int(webcamno))
        # else:
        #     cam = cv2.VideoCapture(1)

    elif (accesspoint == "Static IP Camera") or (accesspoint == "Mobile IP Camera"):
        #'https://192.168.1.41:8080/video'
        url = st.text_input('Input the IP address url:')
        #Camera Settings
        if len(url)>0:
           cam = cv2.VideoCapture(url)
        else:
            st.error('You had not enterd the IP address url. Cannot show you live feed.', icon="🚨")

        stop_button_pressed = st.button("Stop")
        while cam.isOpened() and not stop_button_pressed:
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, 740)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 780)
            ret, frame = cam.read()
            if not ret:
                st.error("Failed to capture frame from camera")
                st.info("Please turn off the other app that is using the camera and restart app")
                st.stop()

            image, name, id = recognize(frame,TOLERANCE)
            #Display name and ID of the person

            name_container.info(f"Name: {name}")
            id_container.success(f"ID: {id}")
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(image)

            if add_btn:
                ret = submitNew('Unknow', id, image)
                if ret == 1:
                    st.success("Person Added")
                elif ret == 0:
                    st.error("Person ID already exists")
                elif ret == -1:
                    st.error("There is no face in the picture")

with st.sidebar.form(key='my_form'):
    st.title("Developer Section")
    submit_button = st.form_submit_button(label='REBUILD DATASET')
    if submit_button:
        with st.spinner("Rebuilding dataset..."):
            build_dataset()
        st.success("Dataset has been reset")