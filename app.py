from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# -----------------------------------
# DATABASE SETUP
# -----------------------------------

def init_db():

    conn = sqlite3.connect('chatbot.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS conversations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_message TEXT,

            bot_response TEXT,

            timestamp TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# -----------------------------------
# INTENT DATABASE
# -----------------------------------

responses = {

    "greeting": {

        "keywords": ["hello", "hi", "hey"],

        "response": "Hello! Welcome to AI Customer Support. How may I help you today?"
    },

    "refund": {

        "keywords": ["refund", "return", "money back"],

        "response": "Please enter your Order ID starting with ORD."
    },

    "delivery": {

        "keywords": ["delivery", "shipment", "track order"],

        "response": "Your order is currently in transit and will arrive within 3-5 business days."
    },

    "payment": {

        "keywords": ["payment", "upi", "transaction", "card"],

        "response": "We detected a payment-related query. Please verify your transaction status."
    },

    "cancel": {

        "keywords": ["cancel", "stop order"],

        "response": "Your cancellation request has been submitted successfully."
    },

    "support": {

        "keywords": ["agent", "human", "support", "help"],

        "response": "Connecting you to a live customer support executive..."
    },

    "thanks": {

        "keywords": ["thanks", "thank you"],

        "response": "You're welcome! Happy to assist you."
    },

    "bye": {

        "keywords": ["bye", "goodbye"],

        "response": "Thank you for using our AI chatbot service."
    }
}

# -----------------------------------
# HOME PAGE
# -----------------------------------

@app.route('/')

def home():

    return render_template('index.html')

# -----------------------------------
# CHATBOT API
# -----------------------------------

@app.route('/get', methods=['POST'])

def chatbot():

    user_message = request.form['msg'].lower()

    bot_response = "I'm unable to understand your request. Connecting to live support..."

    # -----------------------------------
    # ORDER ID DETECTION
    # -----------------------------------

    if "ord" in user_message or "order id" in user_message:

        bot_response = f"Your request for Order ID {user_message.upper()} has been registered successfully."

    # -----------------------------------
    # INTENT MATCHING
    # -----------------------------------

    else:

        for intent in responses.values():

            for keyword in intent['keywords']:

                if keyword in user_message:

                    bot_response = intent['response']

                    break

    # -----------------------------------
    # STORE CHAT IN DATABASE
    # -----------------------------------

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('chatbot.db')

    c = conn.cursor()

    c.execute(

        'INSERT INTO conversations (user_message, bot_response, timestamp) VALUES (?, ?, ?)',

        (user_message, bot_response, timestamp)
    )

    conn.commit()

    conn.close()

    # -----------------------------------
    # RETURN RESPONSE
    # -----------------------------------

    return jsonify({

        'response': bot_response,

        'time': datetime.now().strftime('%I:%M %p')
    })

# -----------------------------------
# MAIN
# -----------------------------------

if __name__ == '__main__':

    app.run(debug=True)