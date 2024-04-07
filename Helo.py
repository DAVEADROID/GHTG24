import random
from typing import Dict, List
from llama_cpp import Llama
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk

class Clep:
    def __init__(self, log_file):
        self.model = Llama(model_path="./llama-2-13b.Q2_K.gguf")
        self.responses = {
            "greeting": ["Hello! How are you feeling today?", "Hi there! What's on your mind?"],
            "good_feeling": ["That's great to hear!", "I'm glad you're feeling good."],
            "bad_feeling": ["I'm sorry to hear that. Would you like to talk about it?", "It's okay to not feel okay. I'm here to listen."],
            "end_conversation": ["It seems like we've made some progress today. Feel free to reach out whenever you need to talk.", "Thank you for sharing. Remember, I'm here whenever you need to talk."],
            "fallback": ["Could you please elaborate?", "I'm not sure I understand. Can you provide more details?"]
        }
        self.conversations: Dict[str, List[str]] = {"greeting": [], "good_feeling": [], "bad_feeling": [], "end_conversation": [], "fallback": []}
        self.log_file = log_file

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

    def chat(self, user_input: str) -> str:
        response = self.generate_response(user_input)
        self.update_conversations(user_input, response)
        self.log_file.write("You: " + user_input + "\n")
        self.log_file.write("Clep: " + response + "\n\n")
        return response

def send_message(event=None):
    user_input = input_text.get()
    if user_input.strip():
        response = clep.chat(user_input)
        output_text.config(state='normal')
        output_text.insert(tk.END, "You: " + user_input + "\n")
        output_text.insert(tk.END, "Clep: " + response + "\n")
        output_text.config(state='disabled')
        input_text.delete(0, tk.END)

if __name__ == "__main__":
    log_file = open('log.txt', 'a+')
    log_file.write(datetime.now().strftime("%a %b %d %H:%M:%S %Y") + '\n')
    clep = Clep(log_file)

    root = tk.Tk()
    root.title("Mental Health Chatbot")

    # Set window size
    root.geometry("1000x750")  # Width x Height

    # Load background image
    background_image_pil = Image.open("R.jpg")
    background_image = ImageTk.PhotoImage(background_image_pil)

    # Create and place background label
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Customizing input text box
    input_text = tk.Entry(root, font=("Arial", 12, "bold"), bg="black", fg="#00FF00", bd=2, relief=tk.SOLID)
    input_text.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    input_text.insert(0, 'Type here to ask a question')
    input_text.bind("<FocusIn>", lambda event: input_text.delete(0, tk.END))

    # Customizing output text box
    output_text = tk.Text(root, height=10, width=40, state='disabled', font=("Arial", 12, "bold"), bg="black", fg="#00FF00", bd=2, relief=tk.SOLID)
    output_text.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    # Create and place text box for the quote
    quote_box = tk.Text(root, width=25, height=3, wrap=tk.WORD, font=("Arial", 12, "bold"), bg="black", fg="#00FF00",bd=0)
    quote_box.insert(tk.END, "Sometimes the best form of therapy is learning how bad other people's lives are.")
    quote_box.config(state='disabled')
    quote_box.place(relx=0.85, rely=0.2, anchor=tk.CENTER)

    # Title
    quote_box = tk.Text(root, width=12, height=1, wrap=tk.WORD, font=("Arial", 50, "bold"), bg="black", fg="#00FF00",bd=0)
    quote_box.insert(tk.END, "Therapy BOT.")
    quote_box.config(state='disabled')
    quote_box.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    # Load and resize send button image
    send_button_image = tk.PhotoImage(file="button.png").subsample(7, 7)  # Adjust the subsample factors as needed
    send_button = tk.Button(root, image=send_button_image, bd=0, command=send_message, bg="black", width=50, height=50)  # Adjust width and height as needed
    send_button.grid(row=0, column=1, padx=10, pady=10)

    root.bind("<Return>", send_message)  # Allow pressing Enter to send message

    root.mainloop()

    log_file.close()
