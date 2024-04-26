import speech_recognition as sr
import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai
import pyttsx3 

# Initialize the recognizer
r = sr.Recognizer()

# Function to convert text to speech
def speak(command):
	
	# Initialize the engine
	engine = pyttsx3.init()
	engine.say(command) 
	engine.runAndWait()

# Function to recognize speech
"""def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except:
            print("Sorry, I did not get that")
            return None"""

# Function to get response from Gemini API
def get_gemini_response(text):
    def remove_characters(string):
        return string.replace('*', '').replace('.', '')



    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    # Setting up the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

    convo = model.start_chat(history=[
    ])

    convo.send_message(text)
    text = str(convo.last.text)
    final_text =  remove_characters(text)
    return final_text

# Main loop
def start():
	while(1): 
	
		try:
			
			# using microphone as source for input.
			with sr.Microphone() as source2:
				
				r.adjust_for_ambient_noise(source2, duration=0.2)
				
				#listens  user's input 
				audio2 = r.listen(source2)
				
				# Using google to recognize audio
				MyText = r.recognize_google(audio2)
				MyText = MyText.lower()
				print("start")
				if MyText == "over and out":
					print("Thankyou for using the service")
					return

				print("Did you say ",MyText)
				response = get_gemini_response(MyText)
				speak(response)
				
		except sr.RequestError as e:
			print("Could not request results; {0}".format(e))
			
		except sr.UnknownValueError:
			print("unknown error occurred")
start()
"""while True:
    text = listen()
    if text:
        response = get_gemini_response(text)
        speak(response)"""