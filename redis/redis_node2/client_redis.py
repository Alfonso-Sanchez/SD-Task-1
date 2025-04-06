import redis
import random
import time

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

print("🔴 Cliente Redis conectado al servidor. Solicitando insultos...")

try:
    while True:
        # Seleccionar aleatoriamente el nodo al que conectarse
        nodo = random.choice(["node1", "node2"])
        print(f"Solicitando insulto al {nodo}...")

        # Enviar una solicitud al servidor seleccionado
        r.set(f"request_insult_{nodo}", "1")

        # Esperar la respuesta del servidor con un tiempo de espera
        timeout = 5  # Tiempo máximo de espera en segundos
        start_time = time.time()

        while not r.exists(f"response_insult_{nodo}"):
            if time.time() - start_time > timeout:
                print(f"⚠️ Tiempo de espera agotado para el nodo {nodo}.")
                break  # Salir del bucle si se agota el tiempo de espera

        # Obtener la respuesta si existe
        if r.exists(f"response_insult_{nodo}"):
            insult = r.get(f"response_insult_{nodo}")
            if insult:
                print(f"📜 Insulto recibido del {nodo}: {insult.decode()}")
                r.delete(f"response_insult_{nodo}")  # Eliminar la respuesta para evitar duplicados

except KeyboardInterrupt:
    print("\n🔴 Cliente desconectado.")