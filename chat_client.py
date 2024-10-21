import pika
import threading
from datetime import datetime

class ChatClient:
    def __init__(self, username, host='localhost'):
        self.username = username
        self.host = host
        self.connection = None
        self.channel = None
        self.queue_name = None

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
            self.channel = self.connection.channel()
            self.channel.exchange_declare(exchange='chat_global', exchange_type='fanout')
            result = self.channel.queue_declare(queue='', exclusive=True)
            self.queue_name = result.method.queue
            self.channel.queue_bind(exchange='chat_global', queue=self.queue_name)
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Erro ao conectar ao RabbitMQ: {e}")
            raise

    def start_receiving(self, display_callback):
        threading.Thread(target=self.receive_messages, args=(display_callback,), daemon=True).start()

    def receive_messages(self, display_callback):
        try:
            for method_frame, properties, body in self.channel.consume(self.queue_name, auto_ack=True):
                message = body.decode()
                timestamp, username, text = message.split('|', 2)
                display_callback(f"[{timestamp}] {username}: {text}")
        except pika.exceptions.ConnectionClosed:
            print("Conexão fechada enquanto recebia mensagens.")
        except Exception as e:
            print(f"Erro ao receber mensagens: {e}")

    def send_message(self, message):
        if message:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            full_message = f"{timestamp}|{self.username}|{message}"
            self.channel.basic_publish(exchange='chat_global', routing_key='', body=full_message)

    def close_connection(self):
        if self.connection:
            try:
                self.connection.close()
            except pika.exceptions.ConnectionClosed:
                pass  # Conexão já foi fechada, ignorar
            except Exception as e:
                print(f"Erro ao fechar a conexão: {e}")