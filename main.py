import os
import tkinter as tk
from tkinter import simpledialog
from chat_client import ChatClient
from chat_gui import ChatGUI

def main():
    username = simpledialog.askstring("Nome de Usuário", "Digite seu nome ou apelido:")
    if not username:
        return

    chat_client = ChatClient(username=username, host=os.getenv('RABBITMQ_HOST', 'localhost'))
    try:
        chat_client.connect()
        root = tk.Tk()
        gui = ChatGUI(root, chat_client)
        root.mainloop()
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        chat_client.close_connection()

if __name__ == '__main__':
    main()