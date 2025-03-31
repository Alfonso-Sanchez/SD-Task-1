import pika
import time
import random

insultos = [
    "Tonto.",
    "Gilipollas.",
    "Maricon"
]

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel1 = connection.channel()
channel2 = connection.channel()
channel1.queue_declare(queue='insultos')
channel2.queue_declare(queue='insultos2')

print("Broadcaster iniciado...")

while True:
    insulto = random.choice(insultos)
    channel1.basic_publish(exchange='', routing_key='insultos1', body=insulto)
    channel2.basic_publish(exchange='', routing_key='insultos2', body=insulto)
    print(f"[Broadcaster] Enviado: {insulto}")
    time.sleep(5)
