"""CodeAlpha Task 3 — Basic Chatbot.

A rule-based text chatbot. Type 'quit' to exit.
Run:  python bot.py
"""
import random

RESPONSES = {
    "hello": ["Hi there!", "Hello! How can I help?", "Hey! Nice to see you."],
    "hi": ["Hi there!", "Hello! How can I help?"],
    "how are you": ["I'm just code, but running fine. How about you?",
                    "All systems go! How are you doing?"],
    "your name": ["I'm CodeBot, your friendly terminal chatbot.",
                  "They call me CodeBot."],
    "help": ["I can chat about simple things — try asking my name, "
             "how I am, the time, or a joke. Type 'quit' to exit."],
    "time": ["I don't wear a watch, but your system clock knows!"],
    "joke": ["Why do programmers prefer dark mode? Because light attracts bugs!",
             "I told a UDP joke once... you probably didn't get it."],
    "python": ["Python is a great language — you're running me on it right now!"],
    "bye": ["Goodbye!", "See you later!", "Bye! Come chat again soon."],
    "thank": ["You're welcome!", "Anytime!", "Happy to help!"],
}
FALLBACKS = [
    "Interesting — tell me more.",
    "I'm still learning. Can you rephrase that?",
    "Hmm, I don't know about that yet. Ask me something else!",
]


def get_reply(user_text):
    """Return a reply for user_text based on keyword matching."""
    text = user_text.lower()
    for key, replies in RESPONSES.items():
        if key in text:
            return random.choice(replies)
    return random.choice(FALLBACKS)


def chat():
    """Loop — read input, break on 'quit', print a reply."""
    while True:
        user_text = input("You: ").strip()
        if not user_text:
            continue
        if user_text.lower() in ("quit", "exit"):
            print("CodeBot:", random.choice(RESPONSES["bye"]))
            break
        print("CodeBot:", get_reply(user_text))


if __name__ == "__main__":
    print("CodeBot: Hi! Type 'quit' to exit.")
    chat()
