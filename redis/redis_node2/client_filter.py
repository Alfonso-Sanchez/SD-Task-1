import redis
import random
import time

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Frases que se enviarán en bucle
frases = [
    "Alfonso eres idiota",
    "Neus eres una zorra",
    "Clara eres una boba"
]

print("🔴 Cliente de filtrado conectado al servidor. Enviando frases automáticamente...")

try:
    while True:
        for frase in frases:
            # Seleccionar aleatoriamente el nodo al que conectarse
            nodo = random.choice(["node1", "node2"])
            print(f"Enviando frase al {nodo}: {frase}")

            # Enviar la frase al servidor seleccionado
            r.set(f"request_filter_{nodo}", frase)

            # Esperar la respuesta del servidor con un tiempo de espera
            timeout = 5  # Tiempo máximo de espera en segundos
            start_time = time.time()

            while not r.exists(f"response_filter_{nodo}"):
                if time.time() - start_time > timeout:
                    print(f"⚠️ Tiempo de espera agotado para el nodo {nodo}.")
                    break  # Salir del bucle si se agota el tiempo de espera

            # Obtener la respuesta si existe
            if r.exists(f"response_filter_{nodo}"):
                frase_filtrada = r.get(f"response_filter_{nodo}").decode()
                r.delete(f"response_filter_{nodo}")  # Eliminar la respuesta después de procesarla
                print(f"Frase filtrada del {nodo}: {frase_filtrada}")

except KeyboardInterrupt:
    print("\n🔴 Cliente desconectado.")