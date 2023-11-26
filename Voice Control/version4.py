import random
import speech_recognition as sr
import pyttsx3
from queue import Queue
# import main.py

r = sr.Recognizer()
q_green = Queue(maxsize=10)
q_amber = Queue(maxsize=10)
q_red = Queue(maxsize=10)

def SpeakText(command):
    print(command)
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def classify_pain_level(pain_response):
    word_to_number = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
    }

    try:
        pain_rating = int(pain_response)
    except ValueError:
        lower_response = pain_response.lower()
        if lower_response in word_to_number:
            pain_rating = word_to_number[lower_response]
        else:
            pain_rating = None

    if 1 <= pain_rating <= 3:
        return "green"
    elif 4 <= pain_rating <= 7:
        return "amber"
    elif 8 <= pain_rating <= 10:
        return "red"
    else:
        return "unknown"

def check_for_concerning_keywords(symptoms):
    concerning_keywords = ["emergency", "severe", "urgent", "critical", "intense", "bleed", "broke", "kill", "dy"]
    return any(keyword in symptoms for keyword in concerning_keywords)

def ask_question(question, source):
    while True:
        SpeakText(question)
        audio_response = r.listen(source)
        response = r.recognize_google(audio_response).lower()
        print(response)
        if response:
            return response
        else:
            print(f"Couldn't understand the response. Please try again.")
            SpeakText(f"Couldn't understand the response. Please try again.")

def create_new_appointment():
    appnum = q_green.qsize() + q_amber.qsize() + q_red.qsize() + 1
    SpeakText(f"Your appointment number is {appnum}.")
    return appnum

def process_existing_appointment():
    SpeakText("Existing appointment confirmed.")

def pain_ranking():
    pain_question = "On a scale from 1 to 10, how would you rate your pain, with 1 being mild and 10 being severe?"
    pain_response = ask_question(pain_question, source2)
    

    while len(pain_response) > 6 or not pain_response:
            pain_response = ask_question(pain_question, source2)

            if len(pain_response) > 6 or not pain_response:
                SpeakText("Couldn't understand the response. Please try again.")
    return pain_response

def process_new_appointment():
    symptom_question = "Thank you for coming in. Can you briefly describe your symptoms?"
    symptoms_response = ask_question(symptom_question, source2)

    while not symptoms_response:
        symptoms_response = ask_question("Please describe your symptoms.", source2)

    if check_for_concerning_keywords(symptoms_response):
        SpeakText("Concerning symptoms detected. Assigning to the red queue.")
        q_red.put(create_new_appointment())
        SpeakText("You are assigned to the red queue.")
    else:
        pain_response = pain_ranking()
        pain_category = classify_pain_level(pain_response)

        if pain_category == "green":
            q_green.put(create_new_appointment())
            SpeakText("You are assigned to the green queue.")
        elif pain_category == "amber":
            q_amber.put(create_new_appointment())
            SpeakText("You are assigned to the amber queue.")
        elif pain_category == "red":
            q_red.put(create_new_appointment())
            SpeakText("You are assigned to the red queue.")
        else:
            SpeakText("Invalid input. Unable to classify pain level.")
        
        rating = int(pain_response)
        
        patient_id = random.randint(1,100)
        # main.insert_symptom_data(patient_id, symptoms_response, rating)
        

while True:
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)

            # Activation loop
            while True:
                activation_response = ask_question("Speak to activate me. Please include 'yes' or 'no' in your responses.", source2)
                if "yes" in activation_response:
                    SpeakText("Activation confirmed. Welcome to the Health Clinic.")
                    SpeakText("Let's create a new appointment.")
                    process_new_appointment()

                else:
                    SpeakText("Activation not confirmed. Please try again.")


    except Exception as e:
        print(f"Unexpected error: {e}")
        SpeakText("An unexpected error occurred. Please try again.")
