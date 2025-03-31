import pika
import threading
import random
import time

frases = [
    "Edu es Tonto.",
    "Eres un Gilipollas.",
    "Soy Maricon.",
    "Hola, buen día."
]

def recibir_filtradas():
    def callback(ch, method, properties, body):
        print(f"[Cliente_Filter] Frase filtrada recibida: {body.decode()}")

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='filtradas')
    channel.basic_consume(queue='filtradas', on_message_callback=callback, auto_ack=True)
    print("[Cliente_Filter] Escuchando frases filtradas...")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n[Cliente_Filter] Interrumpido (recibir)")
        channel.stop_consuming()
        connection.close()

def enviar_frases():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='filtrar')

    try:
        while True:
            frase = random.choice(frases)
            channel.basic_publish(exchange='', routing_key='filtrar', body=frase)
            print(f"[Cliente_Filter] Frase enviada: {frase}")
    except KeyboardInterrupt:
        print("\n[Cliente_Filter] Interrumpido (enviar)")
        connection.close()

# Iniciar en paralelo con daemon=True
hilo1 = threading.Thread(target=recibir_filtradas, daemon=True)
hilo2 = threading.Thread(target=enviar_frases, daemon=True)

hilo1.start()
hilo2.start()

try:
    while True:
        time.sleep(0.1)  # mantener vivo el hilo principal
except KeyboardInterrupt:
    print("\n[Main] Ctrl+C recibido. Terminando programa.")
