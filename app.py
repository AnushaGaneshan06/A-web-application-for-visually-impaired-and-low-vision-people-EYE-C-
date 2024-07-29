from random import choices
import streamlit as st
import pyttsx3
import os
import streamlit as st
import webbrowser
import cv2
import pyttsx3
import os
import subprocess
import pyjokes
import speech_recognition as sr
import datetime
import cvzone
import math
from ultralytics import YOLO

# Global variable to control the object detection loop
stop_object_detection = False

# Function to run object detection
def run_object_detection():
    text_speech = pyttsx3.init()
    global stop_object_detection
    st.title("Object Detection")
    st.write("Starting object detection...")
    model = YOLO("../Yolo-weights/yolov8n.pt")
    classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                  "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                  "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                  "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                  "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                  "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                  "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                  "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                  "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                  "teddy bear", "hair drier", "toothbrush", "pen"
                  ]

    # Open webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 320)

    while not stop_object_detection:
        success, img = cap.read()
        results = model(img, stream=True)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                cvzone.cornerRect(img, (x1, y1, w, h))
                conf = math.ceil(box.conf[0] * 100) / 100
                cls = int(box.cls[0])
                cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)
                answer = classNames[cls]
                newVoiceRate = 30
                text_speech.setProperty('rate', newVoiceRate)
                text_speech.say(answer)
                text_speech.runAndWait()
                text_speech.stop()
        cv2.imshow("Images", img)
        cv2.waitKey(1)

        st.image(img, channels="BGR", use_column_width=True)

# Function to stop object detection
def stop_object_detection_func():
    global stop_object_detection
    stop_object_detection = True

# Function to run voice assistant
def run_voice_assistant():
    st.title("Voice Assistant")
    st.write("Starting voice assistant...")
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    def speak(audio):
        engine.say(audio)
        engine.runAndWait()

    def wishMe():
        hour = int(datetime.datetime.now().hour)
        if hour>= 0 and hour<12:
            speak("Good Morning!")
        elif hour>= 12 and hour<18:
            speak("Good Afternoon!") 
        else:
            speak("Good Evening!") 
        speak("I am your Assistant EYE C. What can I do for you?")

    def takeCommand():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            st.write("Recognizing...") 
            query = r.recognize_google(audio, language='en-in')
            st.write(f"User said: {query}\n")
        except Exception as e:
            st.error("Unable to Recognize your voice.") 
            return "None"

        return query

    wishMe()

    while st.button("Stop Voice Assistant", key=''.join(choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=10))) == False:
        query = takeCommand().lower()
        if 'exit' in query:
            speak("Thank you for using the voice assistant.")
            break
        elif "see me" in query:
            wishMe()
        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
        elif 'search in google' in query:
            speak("What do you want to search?")
            search_query = takeCommand()
            speak(f"Searching {search_query} on Google")
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
        elif 'tell me a joke' in query:
            joke = pyjokes.get_joke()
            speak(joke)

# Function to read out text using text-to-speech engine
def read_out_text(text):
    speak_me = pyttsx3.init()
    speak_me.say(text)
    speak_me.runAndWait()

def main():
    st.title("EYE -C")
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["HOME: 🏠", "Login:🔒", "Register:📝", "Object Detection:📷", "Voice Assistant:🎤", "Reader:📖"])
    #page = st.sidebar.radio("Go to", ["HOME", "Login", "Register", "Object Detection", "Voice Assistant", "Reader"])
   

    if page == "HOME: 🏠":
        st.title("HOME PAGE")
        st.markdown(
            
            """
            <div style='padding: 10px; border: 2px solid #d3d3d3; border-radius: 5px;'>
                <span style='font-size: 24px;'>🏠</span> Home
            </div>
            """,

            unsafe_allow_html=True)
        st.write("EYE -C uses computer vision to assist people with low vision or blindness get things done faster and more easily.Using web camera, EYE- C makes it easier to detect objects with voice features. It also has an extra feature where we can have a simple conversation with the help of an AI voice assistant.")



    if page == "Login:🔒":
        st.title("Login Page")
        st.markdown(
            
            """
            <div style='padding: 10px; border: 2px solid #d3d3d3; border-radius: 5px;'>
                <span style='font-size: 24px;'>🔒</span> 
            </div>
            """,

            unsafe_allow_html=True
        )
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            # Your login logic here
            st.success("Logged in successfully!")
        # Add login functionality

    elif page == "Register:📝":
        st.title("Register Page")
        st.markdown(
            
            """
            <div style='padding: 10px; border: 2px solid #d3d3d3; border-radius: 5px;'>
                <span style='font-size: 24px;'>📝</span> 
            </div>
            """,

            unsafe_allow_html=True
        )
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        if st.button("Register"):
            # Your registration logic here
            st.success("Registration successful! Please proceed to login.")
        # Add registration functionality
            
        

    elif page == "Object Detection:📷":
        st.title("Object Detection Page")
        st.markdown(
            
            """
            <div style='padding: 10px; border: 2px solid #d3d3d3; border-radius: 5px;'>
                <span style='font-size: 24px;'>📷</span> 
            </div>
            """,

            unsafe_allow_html=True
        )
        st.write("Detect your choice")
        stop_button = st.button("Stop Object Detection")
        if stop_button:
            stop_object_detection_func()
        if st.button("Start Object Detection"):
            run_object_detection()

    elif page == "Voice Assistant:🎤":
        st.title("Voice Assistant Page")
        st.markdown(
            
            """
            <div style='padding: 10px; border: 3px solid #d3d3d3; border-radius: 5px;'>
                <span style='font-size: 20px;'>🎤</span> 
            </div>
            """,

            unsafe_allow_html=True
        )
        st.write("make a simple conversation")
        if st.button("Start Voice Assistant"):
            run_voice_assistant()
        # Add voice assistant functionality

    elif page == "Reader:📖":
        st.title("File Reader Page")
        st.markdown(
            
            """
            <div style='padding: 10px; border: 2px solid #d3d3d3; border-radius: 5px;'>
                <span style='font-size: 24px;'>📖</span> 
            </div>
            """,

            unsafe_allow_html=True
        )
        st.write("Upload a text file and click the button to read out its content.")

        # File upload
        uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

        if uploaded_file is not None:
            # Read and display file content
            file_contents = uploaded_file.getvalue().decode("utf-8")
            st.write("File content:")
            st.write(file_contents)

            # Read out content button
            if st.button("Read Out Content"):
                read_out_text(file_contents)

if __name__ == "__main__":
    main()
