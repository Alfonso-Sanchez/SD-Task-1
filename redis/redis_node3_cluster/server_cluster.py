import time
import threading
import json
from rediscluster import RedisCluster

startup_nodes = [
    {"host": "127.0.0.1", "port": 7000},
    {"host": "127.0.0.1", "port": 7001},
    {"host": "127.0.0.1", "port": 7002}
]

r = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

def insultame():
    insult = r.srandmember("server_insults")
    return insult if insult else "No hay más insultos disponibles."

def filtrar_frase(frase):
    insultos = r.smembers("server_insults")
    for insulto in insultos:
        frase = frase.replace(insulto, "****")
    return frase

total_requests = 0
requests_last_second = 0
requests_last_10_seconds = 0
lock = threading.Lock()

def actualizar_estadisticas():
    global total_requests, requests_last_second, requests_last_10_seconds
    last_10s_time = time.time()
    while True:
        time.sleep(1)
        with lock:
            r.hset("stats_cluster", mapping={
                "last_second": requests_last_second,
                "last_10_seconds": requests_last_10_seconds,
                "total_requests": total_requests
            })
            requests_last_second = 0
        if time.time() - last_10s_time >= 10:
            with lock:
                requests_last_10_seconds = 0
                last_10s_time = time.time()

threading.Thread(target=actualizar_estadisticas, daemon=True).start()

print("🟢 [server_cluster] Iniciado. Esperando solicitudes...")
while True:
    data = r.blpop("requests_queue")
    request = json.loads(data[1])

    if request["type"] == "insult":
        respuesta = insultame()
    elif request["type"] == "filter":
        respuesta = filtrar_frase(request.get("phrase", ""))
    else:
        respuesta = "Tipo de solicitud desconocido"

    with lock:
        total_requests += 1
        requests_last_second += 1
        requests_last_10_seconds += 1

    r.rpush(request["response_queue"], respuesta)
