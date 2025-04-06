import redis

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

print("🔴 Cliente Redis conectado al servidor. Solicitando insultos...")

try:
    # Solicitar insultos en un bucle infinito
    while True:
        # Enviar una solicitud al servidor
        r.set("request_insult", "1")

        # Esperar la respuesta del servidor
        while not r.exists("response_insult"):
            pass  # Esperar activamente sin retrasos innecesarios

        insult = r.get("response_insult")
        if insult:
            print(f"📜 Insulto recibido: {insult.decode()}")
            r.delete("response_insult")  # Eliminar la respuesta para evitar duplicados

except KeyboardInterrupt:
    print("\n🔴 Cliente desconectado.")