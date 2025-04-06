# client_filter.py
from rediscluster import RedisCluster
import json

startup_nodes = [
    {"host": "127.0.0.1", "port": 7000},
    {"host": "127.0.0.1", "port": 7001},
    {"host": "127.0.0.1", "port": 7002}
]
r = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

frases = [
    "Alfonso eres idiota",
    "Neus eres una zorra",
    "Clara eres una boba"
]

print("🔴 [client_filter] Solicitando filtrados...")

try:
    i = 0
    while True:
        frase = frases[i % len(frases)]
        request_data = {
            "type": "filter",
            "phrase": frase,
            "response_queue": "client_filter_responses"
        }
        r.rpush("requests_queue", json.dumps(request_data))
        print(f"📤 Petición 'filter' con frase: {frase}")

        data = r.blpop("client_filter_responses", timeout=5)
        if data:
            filtrado = data[1]
            print(f"📥 Respuesta recibida: {filtrado}")
        else:
            print("⚠️ No se recibió respuesta en 5s.")

        i += 1

except KeyboardInterrupt:
    print("\n🔴 [client_filter] Interrumpido.")