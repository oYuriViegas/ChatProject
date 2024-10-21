import tkinter as tk
from tkinter import scrolledtext

class ChatGUI:
    def __init__(self, root, chat_client):
        self.root = root
        self.chat_client = chat_client
        self.root.title("Chat")
        
        self.chat_display = scrolledtext.ScrolledText(root, state='disabled', wrap=tk.WORD)
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.message_entry = tk.Entry(root)
        self.message_entry.pack(padx=10, pady=10, fill=tk.X)
        self.message_entry.bind("<Return>", self.send_message)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.chat_client.start_receiving(self.display_message)

    def display_message(self, message):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, message + '\n')
        self.chat_display.config(state='disabled')
        self.chat_display.yview(tk.END)

    def send_message(self, event=None):
        message = self.message_entry.get()
        self.message_entry.delete(0, tk.END)
        self.chat_client.send_message(message)

    def on_closing(self):
        self.chat_client.close_connection()
        self.root.quit()  # Close the GUI window