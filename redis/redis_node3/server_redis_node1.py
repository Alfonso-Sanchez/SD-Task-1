import redis
import time
import threading
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def insultame():
    insult = r.spop("server_insults_node1")
    if insult:
        return insult.decode()
    return "No hay más insultos disponibles."

def filtrar_frase(frase):
    insultos = [i.decode() for i in r.smembers("server_insults_node1")]
    for insulto in insultos:
        frase = frase.replace(insulto, "****")
    return frase

# Estadísticas
total_requests = 0
requests_last_second = 0
requests_last_10_seconds = 0
lock = threading.Lock()

def actualizar_estadisticas():
    global requests_last_second, requests_last_10_seconds, total_requests
    last_10_seconds_time = time.time()

    while True:
        time.sleep(1)
        with lock:
            stats = {
                "last_second": requests_last_second,
                "last_10_seconds": requests_last_10_seconds,
                "total_requests": total_requests
            }
            r.hset("stats_node1", mapping=stats)
            # Reiniciamos el contador de este último segundo
            requests_last_second = 0

        # Cada 10 segundos, reiniciamos ese acumulador de 10s
        if time.time() - last_10_seconds_time >= 10:
            with lock:
                requests_last_10_seconds = 0
                last_10_seconds_time = time.time()

# Hilo para actualizar estadísticas
thread = threading.Thread(target=actualizar_estadisticas, daemon=True)
thread.start()

print("🟢 Nodo 1 arrancado. Esperando solicitudes (cola requests_node1)...")

while True:
    # data = ( 'requests_node1', b'{"type":"insult","response_queue":"xxxxx",...}' )
    data = r.blpop("requests_node1", timeout=0)  # Bloquea hasta que llegue algo
    if not data:
        continue
    
    raw_request = data[1]  # el payload
    request = json.loads(raw_request.decode("utf-8"))

    if request["type"] == "insult":
        respuesta = insultame()
    elif request["type"] == "filter":
        frase = request.get("phrase", "")
        respuesta = filtrar_frase(frase)
    else:
        respuesta = "Solicitud desconocida"

    # Actualizar estadísticas
    with lock:
        total_requests += 1
        requests_last_second += 1
        requests_last_10_seconds += 1

    # Enviar respuesta a la cola que indicó el cliente
    r.rpush(request["response_queue"], respuesta)