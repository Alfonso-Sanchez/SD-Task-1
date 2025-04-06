import redis
import time

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

def insultame():
    insult = r.spop("server_insults_node2")
    if insult:
        insult = insult.decode()
        r.sadd("server_insults_node2", insult)  # Rotar el insulto
        return insult
    return "No hay más insultos disponibles."

def filtrar_frase(frase):
    insultos = r.smembers("server_insults_node2")
    insultos = [insulto.decode() for insulto in insultos]
    for insulto in insultos:
        if insulto in frase:
            frase = frase.replace(insulto, "****")
    return frase

# Variables para estadísticas
total_requests = 0
requests_last_second = 0
requests_last_10_seconds = 0
start_time = time.time()
last_second_time = start_time
last_10_seconds_time = start_time

print("🟢 Servidor Redis Nodo 2 arrancado. Esperando solicitudes...")

while True:
    current_time = time.time()

    # Procesar solicitudes de insultos
    if r.exists("request_insult_node2"):
        r.delete("request_insult_node2")
        insult = insultame()
        r.set("response_insult_node2", insult)
        r.expire("response_insult_node2", 10)

        # Actualizar estadísticas
        total_requests += 1
        requests_last_second += 1
        requests_last_10_seconds += 1

    # Procesar solicitudes de filtrado de frases
    if r.exists("request_filter_node2"):
        frase = r.get("request_filter_node2").decode()
        r.delete("request_filter_node2")
        frase_filtrada = filtrar_frase(frase)
        r.set("response_filter_node2", frase_filtrada)
        r.expire("response_filter_node2", 10)

        # Actualizar estadísticas
        total_requests += 1
        requests_last_second += 1
        requests_last_10_seconds += 1

    # Actualizar estadísticas cada segundo
    if current_time - last_second_time >= 1:
        stats = {
            "last_second": requests_last_second,
            "last_10_seconds": requests_last_10_seconds,
            "total_requests": total_requests
        }
        r.hset("stats_node2", mapping=stats)  # Usar hset en lugar de hmset
        requests_last_second = 0
        last_second_time = current_time

    # Actualizar estadísticas cada 10 segundos
    if current_time - last_10_seconds_time >= 10:
        requests_last_10_seconds = 0
        last_10_seconds_time = current_time