#April  is a speech llm that uses gemini api to accept user's input as speech and returns it as speech 
#it uses pyttsx3 to deliever the speech and speech_recognition to accept the speech

import speech_recognition as sr
import os
from dotenv import load_dotenv
import google.generativeai as genai
import pyttsx3 

# Initialize the recognizer
r = sr.Recognizer()
load_dotenv()

#initializing the api key and setting up the mode
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
generation_config = {
        "temperature": 0.8,
        "top_p": 0.6,
        "top_k": 8,
        "max_output_tokens": 500,
    }
model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)

#this model can help us store the history of current conversation
convo = model.start_chat()

# Function to convert text to speech
def speak(command):
    # Initialize the engine
    try:
        engine = pyttsx3.init()
        engine.say(command) 
        engine.runAndWait()
    except Exception as e:
        print(f"Exception {e} has occured")
        start()

# Function to get response from Gemini API
def get_gemini_response(query):
    #To minimize the size of output
    query = query + "reply in not more than 100 characters"
    try:
        print("Assistance: ")
        response = convo.send_message(query, stream=True)

        #streaming the response 
        for chunks in response:
            print(chunks.text)
            speak(str(chunks.text).replace("*", ""))
        print("Say Something: ")
        return
    except Exception as e:
        text = f"exception {e} has occured"
        print(text)
        speak(text)
        return 

# Main loop
def start():
    while True: 
        try:
            # using microphone as source for input.
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                
                # listens user's input 
                audio2 = r.listen(source2)
                
                # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
                print("start")

                #Final Command to terminate the loop
                if MyText == "over and out":
                    final_text = "Thank you for using the service"
                    print(final_text)
                    speak(final_text)
                    return

                print("Did you say ", MyText)
                get_gemini_response(MyText)
                
                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            
        except sr.UnknownValueError:
            print("unknown error occurred")

if __name__ == "__main__":
    print("WELCOME TO APRIL")
    start()
