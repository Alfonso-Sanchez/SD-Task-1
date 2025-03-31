import pika
import uuid
import threading
import time

class InsultoClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None
        self.count = 0

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body.decode()
            self.count += 1

    def pedir_insulto(self):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='solicitudes_insulto',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id
            ),
            body='Dame insulto'
        )
        while self.response is None:
            self.connection.process_data_events(time_limit=0.01)
        return self.response

def mostrar_stats(cliente):
    while True:
        time.sleep(1)
        print(f"[Cliente] Respuestas por segundo: {cliente.count}")
        cliente.count = 0

if __name__ == '__main__':
    client = InsultoClient()
    threading.Thread(target=mostrar_stats, args=(client,), daemon=True).start()

    while True:
        client.pedir_insulto()
