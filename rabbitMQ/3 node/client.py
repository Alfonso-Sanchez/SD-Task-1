import pika
import uuid
import threading
import time
import random

entradas = [
    "insultame1",
    "insultame2",
    "insultame3"
]

channels = []

def enviar_y_recibir():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel1 = connection.channel()
    channel2 = connection.channel()
    channel3 = connection.channel()

    def callback(ch, method, properties, body):
            print(f"[Cliente_Insult] Insulto recibido: {body.decode()}")

    # Declarar las colas
    channel1.queue_declare(queue='insultame1')
    channel1.queue_declare(queue='insultar1')
    channel1.basic_consume(queue='insultar1', on_message_callback=callback, auto_ack=True)

    channel2.queue_declare(queue='insultame2')
    channel2.queue_declare(queue='insultar2')
    channel2.basic_consume(queue='insultar2', on_message_callback=callback, auto_ack=True)

    channel2.queue_declare(queue='insultame3')
    channel2.queue_declare(queue='insultar3')
    channel2.basic_consume(queue='insultar3', on_message_callback=callback, auto_ack=True)

    channels.append(channel1)
    channels.append(channel2)
    channels.append(channel3)

    try:
        i = 0
        while True:
            option = i % 3
            i += 1
            channel = channels[option]
            channel.basic_publish(exchange='', routing_key=entradas[option], body='Insultame!')
            print(f"[Cliente_Filter]: Insulto solicitado")

            # Escuchar la respuesta filtrada
            print("[Cliente_Filter] Esperando que me insulten...")
            channel.connection.process_data_events()  # Procesar mensajes entrantes con un límite de tiempo
    except KeyboardInterrupt:
        print("\n[Cliente_Filter] Interrumpido (enviar y recibir)")
        connection.close()

hilo = threading.Thread(target=enviar_y_recibir, daemon=True)

hilo.start()

try:
    while True:
        time.sleep(0.1)  # mantener vivo el hilo principal
except KeyboardInterrupt:
    print("\n[Main] Ctrl+C recibido. Terminando programa.")
