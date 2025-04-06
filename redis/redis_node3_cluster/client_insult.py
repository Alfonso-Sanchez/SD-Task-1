# client_insult.py
from rediscluster import RedisCluster
import json

startup_nodes = [
    {"host": "127.0.0.1", "port": 7000},
    {"host": "127.0.0.1", "port": 7001},
    {"host": "127.0.0.1", "port": 7002}
]
r = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

print("🔴 [client_insult] Solicitando insultos...")

try:
    while True:
        request_data = {
            "type": "insult",
            "response_queue": "client_insult_responses"
        }
        r.rpush("requests_queue", json.dumps(request_data))
        print("📤 Petición 'insult' enviada...")

        data = r.blpop("client_insult_responses", timeout=5)
        if data:
            insulto = data[1]
            print(f"📜 Respuesta recibida: {insulto}")
        else:
            print("⚠️ No se recibió respuesta en 5s.")

except KeyboardInterrupt:
    print("\n🔴 [client_insult] Interrumpido.")