import pika
import time
import random

insultos = [
    "Tonto",
    "Gilipollas",
    "Maricon"
]

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='insultos')

print("Broadcaster iniciado...")

while True:
    insulto = random.choice(insultos)
    channel.basic_publish(exchange='', routing_key='insultos', body=insulto)
    print(f"[Broadcaster] Enviado: {insulto}")
    time.sleep(5)
