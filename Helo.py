import random
from typing import Dict, List
from llama_cpp import Llama
from datetime import datetime

class Clep:
    def __init__(self):
        self.model = Llama(model_path="./llama-2-13b.Q2_K.gguf")
        self.responses = {
            "greeting": ["Hello! How are you feeling today?", "Hi there! What's on your mind?"],
            "good_feeling": ["That's great to hear!", "I'm glad you're feeling good."],
            "bad_feeling": ["I'm sorry to hear that. Would you like to talk about it?", "It's okay to not feel okay. I'm here to listen."],
            "end_conversation": ["It seems like we've made some progress today. Feel free to reach out whenever you need to talk.", "Thank you for sharing. Remember, I'm here whenever you need to talk."],
            "fallback": ["Could you please elaborate?", "I'm not sure I understand. Can you provide more details?"]
        }
        self.conversations: Dict[str, List[str]] = {"greeting": [], "good_feeling": [], "bad_feeling": [], "end_conversation": [], "fallback": []}

    def generate_response(self, user_input: str) -> str:
        user_input = user_input.lower()
        if any(word in user_input for word in ["hello", "hi", "hey"]):
            return random.choice(self.responses["greeting"])
        if any(word in user_input for word in ["good", "great", "awesome"]):
            return random.choice(self.responses["good_feeling"])
        if any(word in user_input for word in ["bad", "sad", "not good"]):
            return random.choice(self.responses["bad_feeling"])
        if any(word in user_input for word in ["thank", "appreciate", "bye", "goodbye"]):
            return random.choice(self.responses["end_conversation"])
        return self.generate_ml_response(user_input)

    def generate_ml_response(self, user_input: str) -> str:
        output = self.model(user_input, max_tokens=100)
        response = output['choices'][0]['text']
        return response

    def update_conversations(self, user_input: str, response: str) -> None:
        user_input = user_input.lower()
        for key in self.conversations:
            if response in self.responses[key]:
                self.conversations[key].append(user_input)

    def chat(self) -> None:
        print("Clep: Hello! I'm Clep, your therapy chatbot. How can I help you today?")
        while True:
            user_input = input("You: ")
            log_file.write("You: " + user_input + "\n\n")
            response = self.generate_response(user_input)
            print("Clep: ", response)
            log_file.write("Clep: " + response + "\n\n")
            self.update_conversations(user_input, response)
            if user_input.lower() == 'goodbye' or user_input.lower() == 'bye':
                break

if __name__ == "__main__":
    log_file = open('log.txt', 'a+')
    log_file.write(datetime.now().strftime("%a %b %d %H:%M:%S %Y") + '\n')
    clep = Clep()
    clep.chat()
    log_file.close()