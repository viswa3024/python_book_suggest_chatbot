# -*- coding: utf-8 -*-
"""Chatbot_Hackathon.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZsnKNqh9eo8or77slliRgjlLy09vx7Oy

# Advanced Certification in AIML
## A Program by IIIT-H and TalentSprint

## Problem Statement

Build a conversational bot to interact with the user using 2 approaches (Alexa Chatbot and Python Chatbot) for the given skill and achieve desired outcomes through the conversation.

### It is recommended to watch the chatbot code explanation video before start working on the Hackathon
"""

#@title Chatbot Code Explanation Video
from IPython.display import HTML

HTML("""<video width="854" height="480" controls>
  <source src="https://cdn.iiith.talentsprint.com/aiml/Experiment_related_data/Walkthrough/b17_hackathon_1_chatbot_walkthrough.mp4" type="video/mp4">
</video>
""")

"""## Skill to be developed as per the intents allocation

**Zodiac Sign:** The bot should give the Zodiac Sign of the user, based on the date of birth (day, month and year) provided by the user **(This intent is common for everyone)**

**Suggest a Movie:** The bot should suggest a movie based on user preferences: Language, Actor, Genre and other details

**Find the Restaurant:**  Find the restaurants based on Cuisine, Cost type (cheap, medium, expensive), location and other parameters

**Suggest a Book:** The bot should suggest the book based on user preferences: Author, language, genre and other parameters

**Recommend a Store:** The bot should search a store based on preferences: Store type (medical clinics, food store, dry cleaning and more), location, availability (Open, Close) and other parameters

Teams will be creating a conversational chatbot for the intents allocated to them

> Team A =	Group		1, 5, 9, 13, 17, 21  => Suggest a Movie & Zodiac Sign

> Team B =  Group   2, 6, 10, 14, 18, 22 => Find a Restaurant & Zodiac Sign

> Team C =  Group   3, 7, 11, 15, 19, 23  => Suggest a Book & Zodiac Sign

> Team D =  Group   4, 8, 12, 16, 20, 24 =>  Recommend a Store & Zodiac Sign

* For Zodiac sign Intent, all the required utterances, slots and params (JSON) files are provided for your reference. A csv file is also provided to perform the action


* For the another allocated intent, create all the required files (utterances, slots and params) and perform the action by creating a csv file.

# Alexa Chatbot (Total Marks = 20)

**Note:**
- Complete all of the tasks mentioned below from the [link](https://developer.amazon.com/alexa/console/ask) to work on the Alexa chatbot.
- Go through the Pre-Hackathon for Alexa ChatBot material to understand Alexa Chatbot’s code and it's architecture.

### **Criteria for evaluation**

**Task1 (2Marks)** - Create a skill and provide intents based on team allocation
- **Note:** You should create multiple intents under one skill, so that you can use that skill for testing

**Task2 (4Marks)** - Create at least 50 utterances for each intent

**Task3 (2Marks)** - Create at least 3 slots with the slot types for each intent
- Hint: [Slot type references](https://developer.amazon.com/en-US/docs/alexa/custom-skills/slot-type-reference.html#list-slot-types)

**Task4 (4Marks)** - Create a database with all possible combinations of all attributes (can be a CSV ﬁle) along with possible outcome for each combination. This database will be used for performing an action. Minimum 10 combinations
  - Create a CSV file for the allocated intent other than Zodiac sign

**Task5 (4Marks)** - Update the lambda_function.py and requirements.txt in the Code section - Refer PRE-HACKATHON Alexa ChatBot material


**Task6 (4Marks)** - Run and test the Alexa chatbot for both the intents with the following:
  - Alexa Chatbot should identify the user requirement.
  - Gather the data from user input and get the relevant output.
  - It should prompt the user with different prompts if the required input is not fulfilled.
  - It should shift between the intents and maintain the dialogue flow.

# Python Chatbot (Total Marks = 20)

**Note:** Complete all of the tasks mentioned below in this colab notebook to work on the Python chatbot.

### **Criteria for evaluation**

**Task1 (6Marks)** - Create .dat files for your intent (as the .dat files of Zodiac intent is already provided) based on the team allocation. Also, configure file in the params folder (Refer the given zodiac sign file for more information).

   * Give minimum 50 utterances for each intent. Give the details in the **intent folder** -> *intent_name.dat* file. (Hint: You can use the same utterances which was created for Alexa chatbot)

   * Give minimum 3 slots for each intent. Create a different *.dat* file for each slot under the **Slots folder** (Hint: You can use the same slots which was created for Alexa chatbot)

   * Conﬁgure *params.cfg* ﬁle for the skill given to you under the **params folder**. Setup the intents in the same file with its required elements like Parameters, actions, etc. Refer to Zodiac Sign files for more information.

**Task2 (2Marks)** - Create a database for the intent with all possible combinations of all attributes (can be a CSV ﬁle) along with possible outcome for each combination. Minimum 10 combinations. (Hint: You can use the same database which was created for Alexa chatbot)

  * Create a CSV file for the allocated intent other than Zodiac sign

**Task3 (5Marks)** - Text Representation and Classifications for both the intents

* Create a numerical representation of the text data (utterances) by using **any one** of the following process:

  - [Countvectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html)

    OR

  - [TFIDFVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)

* Perform a classification using the extracted features and classify the intent.

**Task4 (4Marks)** - Compare the attributes with the CSV file and get the final selection of that particular intent.

* Action function for the zodiac sign is already given. Similarly create action function for your intent and give the function name as mentioned in the params.cfg file.

**Task5 (3Marks)** - Run and test the Python chatbot for both the intents with the following:
  - Python Chatbot should identify the user requirement.
  - Gather the data from user input and get the relevant output.
  - It should prompt the user with different prompts if the required input is not fulfilled.
  - It should shift between the intents and maintain the dialogue flow.

### Below is the code for updating the Python Chatbot
"""

#@title Run this cell to download the data
!wget -qq https://cdn.iiith.talentsprint.com/aiml/Hackathon_data/Chatbot_Hackathon.zip
!unzip -qq Chatbot_Hackathon.zip
print("Data downloaded successfully")

# Import Libraries
import json
import random
import os
import re
import datetime
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

# Importing context and .py script files
from Context import *
from Intent import *

"""### Chatbot Architecture

Defining functions for Loading Intent, Collecting params, Checking actions, Getting Attributes and Identifying Intents
"""

def loadIntent(path, intent):
    with open(path) as fil:
        dat = json.load(fil)
        intent = dat[intent]
        return Intent(intent['intentname'],intent['Parameters'], intent['actions'])

def check_required_params(current_intent, attributes, context):
    '''Collects attributes pertaining to the current intent'''
    for para in current_intent.params:
        if para.required:
            if para.name not in attributes:
                return random.choice(para.prompts), context
    return None, context

def check_actions(current_intent, attributes, context):
    '''This function performs the action for the intent as mentioned
    in the intent config file. Performs actions pertaining to current intent '''
    context = IntentComplete()
    if current_intent.action.endswith('()'):
        return eval(current_intent.action), context
    return current_intent.action, context

def getattributes(uinput,context,attributes, intent):
    '''This function marks the slots in user input, and updates
    the attributes dictionary'''
    uinput = " "+uinput.lower()+" "
    if context.name.startswith('IntentComplete'):
        return attributes, uinput
    else:
        files = os.listdir(path_slots)
        slots = {}
        for fil in files:
            if fil == ".ipynb_checkpoints":
                continue
            lines = open(path_slots+fil).readlines()
            for i, line in enumerate(lines):
                line = line.strip()
                if len(uinput.split(" "+line.lower()+" ")) > 1:
                    slots[line] = fil[:-4]
        for value, slot in slots.items():
            if intent != None and slot in " ".join([param.name for param in intent.params]):
                uinput = re.sub(value,r'$'+slot,uinput,flags=re.IGNORECASE)
                attributes[slot] = value
            else:
                uinput = re.sub(value,r'$'+slot,uinput,flags=re.IGNORECASE)
                attributes[slot] = value
        return attributes, uinput

def input_processor(user_input, context, attributes, intent):
    '''Update the attributes, abstract over the slots in user input'''
    attributes, cleaned_input = getattributes(user_input, context, attributes, intent)
    return attributes, cleaned_input

def intentIdentifier(clean_input, context,current_intent):
    clean_input = clean_input.lower()
    if (current_intent==None):
        return loadIntent(path_param,intentPredict(clean_input))
    else:
        #If current intent is not none, stick with the ongoing intent
        #return current_intent
        intent = loadIntent(path_param,intentPredict(clean_input))
        if current_intent != intent:
            for para in current_intent.params:
                if para.name in clean_input:
                    return current_intent
        return loadIntent(path_param,intentPredict(clean_input))

"""Session class is one active session of the chatbot which the user interacts with. Let's go into the details:

**reply( )** is the important one in our session object it takes user_input as a parameter and calls different modules of the chatbot architecture:


*   **input_processor( )** - It helps in preprocessing and fetching the slots that can identify in the ready state
    
    - **getattributes( )** - It helps in identifying all the slots in the user utterance. Identify and map them to the parameters
    
    
*   **intentIdentifier( )**

  -  **intentPredict()** - Task to complete

*   **check_required_params( )** - Based on the current intents, it goes over it's parameters

*   **check_actions( )** - This function performs the action for the intent

**Note:** Refer the *Chatbot_Reading_Material.pdf* for more information on the conversation flow


       

"""

class Session:
    def __init__(self, attributes=None, active_contexts=[FirstGreeting(), IntentComplete() ]):
        '''Initialise a default session'''
        # Active contexts not used yet, can use it to have multiple contexts
        self.active_contexts = active_contexts

        # Contexts are flags which control dialogue flow
        self.context = FirstGreeting()

        # Intent tracks the current state of dialogue
        self.current_intent = None

        # attributes hold the information collected over the conversation
        self.attributes = {}

    def reply(self, user_input):
        '''Generate response to user input'''
        self.attributes, clean_input = input_processor(user_input, self.context, self.attributes, self.current_intent)

        self.current_intent = intentIdentifier(clean_input, self.context, self.current_intent)

        prompt, self.context = check_required_params(self.current_intent, self.attributes, self.context)

        # prompt being None means all parameters satisfied, perform the intent action
        if prompt is None and self.context.name!='IntentComplete':
            prompt, self.context = check_actions(self.current_intent, self.attributes, self.context)

        return prompt, self.attributes

"""### Task1 (6Marks)

Create .dat files for your intent based on the team allocation. Also, configure file in the params folder (Refer the given zodiac sign file for more information).

   * Give minimum 50 utterances for each intent. You can use the same utterances which were created for Alexa chatbot. Give the details in the **intent folder** -> *intent_name.dat* file

   * Give minimum 3 slots for each intent. You can use the same slots which were created for Alexa chatbot. Create a different *.dat* file for each slot under the **Slots folder**

   * Conﬁgure *params.cfg* ﬁle for the skill given to you under the **params folder**. Setup the intents in the same file with its required elements like Parameters, actions, etc. Refer to Zodiac Sign file for more information.

Once dat files are created, you can upload them in colab as path details given in the below code
"""

path_param = 'Chatbot/params/params.cfg'
path_utterances = 'Chatbot/utterances/'
path_slots = 'Chatbot/slots/'



"""### Task2 (2Marks)

Create a database with all possible combinations of all attributes (can be a CSV ﬁle) along with possible outcome for each combination for your intent. Provide at least 10 combinations. (Hint: You can use the same database which was created for Alexa chatbot)

  * Create a CSV file for the allocated intent other than Zodiac sign.

Upload the file and give the path in the below code
"""

path_csv_zodiac = 'Chatbot/Zodiac_sign.csv'

# YOUR CODE HERE for updating the path of csv file
path_csv = 'Chatbot/books.csv'

"""### Task3 (5Marks)
Text Representation and Classifications for both the intents

To classify the intents based on user input, model must be trained on all the utterances given.
- Iterate through the files from folder of utterances which ends with `.dat` extension
- Create an array of train data and labels with respective class names (intent names)
- Create a vector representation of train data (utterances) by using **any one** of the following process for the task:

  - [Countvectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html)

    OR

  - [TFIDFVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)

- Perform a classification using the extracted features and classify the intent.
    - ### **Expected Accuracy above 90%**

- Predict the user_input using the trained model using intent_predict() method

**Data Loading:** Read all the utterances and extract the data (text) and labels for each intent.
"""

# YOUR CODE HERE for loading and preparing the data
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os
import json

def load_utterances_from_files(folder_path):
    utterances = []
    labels = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".dat"):
            with open(os.path.join(folder_path, file_name), "r") as file:
                lines = file.readlines()
                for line in lines:
                    utterances.append(line.strip())
                    labels.append(file_name[:-4])  # Remove the ".dat" extension to get the intent label

    return utterances, labels

utterances, labels = load_utterances_from_files('Chatbot/utterances/')

labels

utterances

X_train, X_test, y_train, y_test = train_test_split(utterances, labels, test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer()

X_train_vectorized = vectorizer.fit_transform(X_train)

classifier = MultinomialNB()
classifier.fit(X_train_vectorized, y_train)

X_test_vectorized = vectorizer.transform(X_test)

y_pred = classifier.predict(X_test_vectorized)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

from sklearn.neighbors import KNeighborsClassifier

neigh = KNeighborsClassifier(n_neighbors=5)  # You can adjust the number of neighbors as needed
neigh.fit(X_train_vectorized, y_train)

y_pred = neigh.predict(X_test_vectorized)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

from sklearn.linear_model import LogisticRegression

lr = LogisticRegression(max_iter=1000)  # You can adjust other parameters as needed
lr.fit(X_train_vectorized, y_train)

y_pred = lr.predict(X_test_vectorized)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

from sklearn.tree import DecisionTreeClassifier

dtree = DecisionTreeClassifier(max_depth=3,criterion='entropy')  # You can adjust other parameters as needed
dtree.fit(X_train_vectorized, y_train)

y_pred = dtree.predict(X_test_vectorized)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

from sklearn.svm import SVC

clf = SVC(kernel='linear')  # You can adjust other parameters as needed
clf.fit(X_train_vectorized, y_train)

y_pred = clf.predict(X_test_vectorized)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier

clf = BaggingClassifier(estimator=SVC(kernel='linear'),n_estimators=10,random_state=32)

clf.fit(X_train_vectorized, y_train)

y_pred = clf.predict(X_test_vectorized)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

rf = RandomForestClassifier(n_estimators=100,criterion='entropy')

rf.fit(X_train_vectorized, y_train)

y_pred = rf.predict(X_test_vectorized)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

est = [('Lr',LogisticRegression(max_iter=100)),('DT',DecisionTreeClassifier()),('sv',SVC(kernel='linear'))]

hard_vot = VotingClassifier(estimators=est,voting='hard')

hard_vot.fit(X_train_vectorized, y_train)

y_pred_h = hard_vot.predict(X_test_vectorized)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred_h)
print(f"Accuracy: {accuracy}")

"""**Features extraction:** Fit the extracted text data with vectorizer to get the features."""

# YOUR CODE HERE to extract the features

"""**Classification:**

* Identify the features and labels
* Use train_test_split for splitting the train and test data
* Fit your model on the train set using fit() and perform prediction on the test set using predict()
* Get the accuracy of the model

        Expected Accuracy above 90%

"""

# YOUR CODE HERE for classifying the intent

"""Predict the user_input using the trained model

**Note:** intentPredict() function call is specified in the Conversation Flow
- vectorize the given user_input
- reshape the vectorized array using `reshape(1,-1)` as the user_input is only a single utterance
- predict the label on the vectorized array
- return the respective class (intent_name)
"""

def intentPredict(user_input):
    # Vectorize the user input
    user_input_vectorized = vectorizer.transform([user_input])

    # Reshape the vectorized array
    user_input_vectorized_reshaped = user_input_vectorized.reshape(1, -1)

    # Predict the label on the vectorized array
    prediction = lr.predict(user_input_vectorized_reshaped)

    # Return the respective class (intent_name)
    return prediction[0]

user_input_example = "open my zodiac sign"
predicted_intent = intentPredict(user_input_example)
print(f"Predicted Intent: {predicted_intent}")

# Take the user input as test data and predict using the model.

def intentPredict(user_input):  # Do not change the function name

    # YOUR CODE HERE for the prediction

    return predicted_intent

"""### Task4 (4Marks):

Compare the attributes with the CSV file and get the final selection of that particular intent.

  * Action function for the zodiac sign is already given. Similarly create action function for your intents and give the function name as mentioned in the params.cfg file.
  * Use session object to take user inputs. (ex: `session.attributes`)

Below are the 2 action functions to be performed:
  1. Zodiac Sign Action
  2. Your allocated Intent Action

1. Below Action function is given for
Zodiac_Sign intent
"""

# Note: Zodiac_sign.csv records are taken from the internet; however it is open to adding multiple records.

# Performs action for zodiac sign with csv file as source
def zodiacSign_Action():
    # global session
    attr = session.attributes
    year = int(attr['year'])
    month = attr['month'] # month is a string, convert it to a month index
    day = int(attr['day'])
    df = pd.read_csv(path_csv_zodiac)
    zodiac = ""

    try:
        month = int(datetime.datetime.strptime(month,'%b').strftime('%m'))
    except:
        month = int(datetime.datetime.strptime(month,'%B').strftime('%m'))

    try:
        usr_dob = (month,day)
        datetime.datetime(year, month, day)
        for index, row in df.iterrows():
          if filter(row['Start']) <= usr_dob <= filter(row['End']):
            zodiac = row['Zodiac']
        return "Your Zodiac sign is " + zodiac
    except ValueError:
        return "This is not a valid date"

def filter(X):
    date = X.split()
    month = int(datetime.datetime.strptime(date[0],'%B').strftime('%m'))
    day = int(datetime.datetime.strptime(date[1],'%d').strftime('%d'))
    return (month,day)

def get_books_list(df):
  books = []
  for _, row in df.iterrows():
    book = {
        'Title': row['Title'],
        'Author': row['Author'].lower(),
        'Language': row['Language'].lower(),
        'Genre': row['Genre'].lower()
      }
    books.append(book)
  return books

def recommend_book(preferences, books):
  filtered_books = [book for book in books if all(book[key] == value for key, value in preferences.items())]

  if filtered_books:
    return random.choice(filtered_books)
  else:
    return "No matching books found."

"""2. Define Action function for your allocated Intent"""

# YOUR CODE HERE: Define a function to perform action using CSV file

# Note: books.csv records are taken from the internet; however it is open to adding multiple records.

# Performs action for suggest book with csv file as source
def suggestBook_Action():
    # global session
    attr = session.attributes

    if attr["author"]:
      author = attr["author"].lower()
    else:
      author = None

    if attr["language"]:
      language = attr["language"].lower()
    else:
      language = None

    if attr["genre"]:
      genre = attr["genre"].lower()
    else:
      genre = None

    user_preferences = {}
    if author and author != 'author':
      user_preferences["Author"] = author
    if language and language != 'language':
      user_preferences["Language"] = language
    if genre and genre != 'genre':
      user_preferences["Genre"] = genre

    df = pd.read_csv(path_csv)
    books_list = get_books_list(df)
    recommended_book = recommend_book(user_preferences,books_list)

    try:
      if isinstance(recommended_book, dict):
        author_name = recommended_book['Author'].title()
        return f"Recommended Book: {recommended_book['Title']} by {author_name}"
      else:
        return "author is  {author}, language is {language}, genre is {genre}, No matching books found.".format(author=author,language=language,genre=genre)
    except ValueError:
        return "This is not a valid date"

"""### Task5 (3Marks)

Run and test the Python chatbot for both the intents with the following:
  - Python Chatbot should identify the user requirement.
  - Gather the data from user input and get the relevant output.
  - It should prompt the user with different prompts if the required input is not fulfilled.
  - It should shift between the intents and maintain the dialogue flow.

Chatbot configuration class
"""

class BOT_config():
    def __init__(self, session):
        self.welcome='BOT: Hi! Welcome to Talentsprint Hackathon, How may i assist you?'
        self.exits=["finish","exit","end","quit","stop","close", "Bye"]
        if session.context.name == 'IntentComplete':
            session.attributes = {}
            session.context = FirstGreeting()
            session.current_intent = None

"""#### Conversational Chatbot

Interact with bot by giving any utterance

Ex:  `find zodiac sign`
"""

session = Session()
print(BOT_config(session).welcome)
while (True):
    inp = input('User: ')
    if inp in BOT_config(session).exits:
        break
    prompt = session.reply(inp)
    print ('BOT:', prompt)

from google.colab import drive
drive.mount('/content/drive')