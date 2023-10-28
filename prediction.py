import nltk
import numpy as np
import json
import pickle
import random
import tensorflow
from data_preprocessing import get_stem_words
# Function to register a new user

a = "boy"

import sys

# Define the myfunc function outside of the login_user function

def myfunc(result):

    global a

    a = result
 
def register_user():

    username = input("Enter a username: ")

    password = input("Enter a password: ")
 
    with open("user_data.txt", "a") as file:

        file.write(f"{username}:{password}\n")
 
    print("User registered successfully.")
 
# Function to check if a user's credentials are valid

def login_user():

    global a  # You don't need to redeclare global variable 'a' here

    username = input("Enter your username: ")

    password = input("Enter your password: ")
 
    with open("user_data.txt", "r") as file:

        for line in file:

            stored_username, stored_password = line.strip().split(":")

            if username == stored_username and password == stored_password:

                print("Login successful. Welcome, " + username + "!")

                myfunc("yes")

                return
 
        # Move this block outside of the loop

        print("Invalid username or password. Please try again.")

        myfunc("no")
 
while True:  # Change this to a while loop without the 'x' variable

    print("1. Register")

    print("2. Login")

    print("3. Exit")
 
    choice = input("Select an option: ")
 
    if choice == "1":

        register_user()

    elif choice == "2":

        login_user()

        if a == "yes":

            break

    elif choice == "3":

        print("Goodbye!")

        sys.exit()

    else:

        print("Invalid choice. Please select a valid option.")




ignore_words = ['?', '!',',','.', "'s", "'m"]
model=tensorflow.keras.models.load_model('chatbot_model.h5')

intents=json.loads(open('intents.json').read())
words=pickle.load(open('words.pkl','rb'))
classes=pickle.load(open('classes.pkl','rb'))

def preprocess_user_input(input):
    input_token1=nltk.word_tokenize(input)
    input_token2=get_stem_words(input_token1,ignore_words)
    token2=sorted(list(set(input_token2)))
    bag=[]
    bag_of_words=[]
    for word in words:
        
        if word in token2:
            bag_of_words.append(1)
        else:
            bag_of_words.append(0)
    bag.append(bag_of_words)
    return np.array(bag)

def class_prediction(input):
    input=preprocess_user_input(input)
    prediction=model.predict(input)
    predicted_class_label=np.argmax(prediction[0])
    return predicted_class_label

def bot_response(input):
    predicted_class_label=class_prediction(input)
    predicted_class=classes[predicted_class_label]
    for intent in intents['intents']:
        if intent['tag']==predicted_class:
            bot_response=random.choice(intent['responses'])
            return bot_response

print("Hi I am Baymax!Your personal healtcare companion, How can I help u?")
while True:
    user_input=input('Type your message here: ')
    print("user input: ",user_input)
    response=bot_response(user_input)
    print('Bot reponse: ',response)
    
