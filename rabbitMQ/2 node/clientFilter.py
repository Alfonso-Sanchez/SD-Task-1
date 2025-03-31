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

entradas = [
    "filtrar1",
    "filtrar2"
]

channels = []

def enviar_y_recibir():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel1 = connection.channel()
    channel2 = connection.channel()

    def callback(ch, method, properties, body):
            print(f"[Cliente_Filter] Frase filtrada recibida: {body.decode()}")

    # Declarar las colas
    channel1.queue_declare(queue='filtrar1')
    channel1.queue_declare(queue='filtradas1')
    channel1.basic_consume(queue='filtradas1', on_message_callback=callback, auto_ack=True)

    channel2.queue_declare(queue='filtrar2')
    channel2.queue_declare(queue='filtradas2')
    channel2.basic_consume(queue='filtradas2', on_message_callback=callback, auto_ack=True)

    channels.append(channel1)
    channels.append(channel2)

    try:
        while True:
            # Enviar una frase
            frase = random.choice(frases)
            option = random.randint(0,1)
            channel = channels[option]
            channel.basic_publish(exchange='', routing_key=entradas[option], body=frase)
            print(f"[Cliente_Filter] Frase enviada: {frase}")

            # Escuchar la respuesta filtrada
            print("[Cliente_Filter] Esperando frase filtrada...")
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
