import redis
import time
import threading
import json

r = redis.Redis(host='localhost', port=6381, db=0)

def insultame():
    insult = r.spop("server_insults_node3")
    if insult:
        return insult.decode()
    return "No hay más insultos disponibles."

def filtrar_frase(frase):
    insultos = [i.decode() for i in r.smembers("server_insults_node3")]
    for insulto in insultos:
        frase = frase.replace(insulto, "****")
    return frase

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
            r.hset("stats_node3", mapping=stats)
            requests_last_second = 0

        if time.time() - last_10_seconds_time >= 10:
            with lock:
                requests_last_10_seconds = 0
                last_10_seconds_time = time.time()

thread = threading.Thread(target=actualizar_estadisticas, daemon=True)
thread.start()

print("🟢 Nodo 3 arrancado. Esperando solicitudes (cola requests_node3)...")

while True:
    data = r.blpop("requests_node3", timeout=0)
    if not data:
        continue
    
    request = json.loads(data[1].decode("utf-8"))

    if request["type"] == "insult":
        respuesta = insultame()
    elif request["type"] == "filter":
        respuesta = filtrar_frase(request.get("phrase", ""))
    else:
        respuesta = "Solicitud desconocida"

    with lock:
        total_requests += 1
        requests_last_second += 1
        requests_last_10_seconds += 1

    r.rpush(request["response_queue"], respuesta)