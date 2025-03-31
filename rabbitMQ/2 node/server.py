import pika
import threading
import time
import curses

# Variables compartidas
cola_insultos = set()
contador_insultos = 0
contador_filtrados = 0
contador_solicitudes_insulto = 0
peticiones_en_segundo_actual = 0
pps = 0
lock = threading.Lock()

# Servicio 1: Recibir insultos del broadcaster
def recibir_insultos():
    global contador_insultos
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='insultos1')
    
    def callback(ch, method, properties, body):
        global contador_insultos
        insulto = body.decode()
        with lock:
            if insulto not in cola_insultos:
                cola_insultos.add(insulto)
                contador_insultos += 1

    channel.basic_consume(queue='insultos1', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

# Servicio 2: Filtrar frases recibidas en la cola 'filtrar'
def filtrar_frases():
    global contador_filtrados, peticiones_en_segundo_actual
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='filtrar1')
    channel.queue_declare(queue='filtradas1')
    
    def callback(ch, method, properties, body):
        global contador_filtrados, peticiones_en_segundo_actual
        frase = body.decode()
        palabras = frase.strip().split(" ")
        # Obtener los insultos filtrados de la colección
        with lock:
            insultos_list = [i.lower().strip(".,!?") for i in cola_insultos]
        palabras_filtradas = [
            "CENSORED" if palabra.lower().strip(".,!?") in insultos_list else palabra 
            for palabra in palabras
        ]
        resultado = " ".join(palabras_filtradas)
        with lock:
            contador_filtrados += 1
            peticiones_en_segundo_actual += 1
        ch.basic_publish(exchange='', routing_key='filtradas1', body=resultado)

    channel.basic_consume(queue='filtrar1', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

# Servicio 3: Responder solicitudes de insulto en 'solicitudes_insulto'
def responder_insultos():
    global contador_solicitudes_insulto, peticiones_en_segundo_actual
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='insultame1')
    channel.queue_declare(queue='insultar1')
    
    def callback(ch, method, properties, body):
        global contador_solicitudes_insulto, peticiones_en_segundo_actual
        print("he recibido algo")
        with lock:
            contador_solicitudes_insulto += 1
            peticiones_en_segundo_actual += 1
        
        # Si no hay insultos, se devuelve un mensaje por defecto
        insulto = list(cola_insultos)[-1] if cola_insultos else "Sin insultos."
        ch.basic_publish(exchange='', routing_key='insultar1', body=insulto)

    channel.basic_consume(queue='insultame1', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

# Servicio 4: Mostrar estadísticas usando curses
def mostrar_stats(stdscr):
    global peticiones_en_segundo_actual, contador_insultos, contador_filtrados, contador_solicitudes_insulto, pps
    curses.curs_set(0)
    stdscr.nodelay(True)
    while True:
        with lock:
            pps = peticiones_en_segundo_actual
            peticiones_en_segundo_actual = 0
            # Se copia la lista de insultos para la presentación
            insultos_list = list(cola_insultos)
            stats_insultos = contador_insultos
            stats_filtrados = contador_filtrados
            stats_solicitudes = contador_solicitudes_insulto
        stdscr.clear()
        stdscr.addstr(1, 1, "== Servidor 1 RabbitMQ - Estadísticas ==")
        stdscr.addstr(3, 2, f"Insultos únicos recibidos: {stats_insultos}")
        stdscr.addstr(4, 2, f"Frases filtradas: {stats_filtrados}")
        stdscr.addstr(5, 2, f"Solicitudes insulto servidas: {stats_solicitudes}")
        stdscr.addstr(6, 2, f"Peticiones por segundo (total): {pps}")
        stdscr.addstr(8, 2, f"Ejemplo insultos: {', '.join(insultos_list[:5])}")
        stdscr.refresh()
        time.sleep(1)

#Servicio 5: Enviar stats al centro de stadisticas
def publicar_stats(nombre_servidor):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='stats')

    while True:
        with lock:
            mensaje = {
                "servidor": nombre_servidor,
                "insultos": contador_insultos,
                "filtrados": contador_filtrados,
                "solicitudes": contador_solicitudes_insulto,
                "solicitudes/segundo": pps
            }
        channel.basic_publish(exchange='', routing_key='stats', body=str(mensaje))
        time.sleep(1)

if __name__ == '__main__':
    threading.Thread(target=recibir_insultos, daemon=True).start()
    threading.Thread(target=filtrar_frases, daemon=True).start()
    threading.Thread(target=responder_insultos, daemon=True).start()
    threading.Thread(target=publicar_stats, args=("Servidor1",), daemon=True).start()
    curses.wrapper(mostrar_stats)