# broadcaster.py
from rediscluster import RedisCluster
import time

startup_nodes = [
    {"host": "127.0.0.1", "port": 7000},
    {"host": "127.0.0.1", "port": 7001},
    {"host": "127.0.0.1", "port": 7002}
]
r = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

insults = ["idiota", "zorra", "cap de cul", "tonto", "imbécil"]

print("🔵 [broadcaster] Iniciado. Insertando insultos cada 5s...")

try:
    while True:
        insult = insults.pop(0)
        insults.append(insult)
        r.sadd("server_insults", insult)
        print(f"✅ Insertado insulto: {insult}")
        time.sleep(5)

except KeyboardInterrupt:
    print("\n🔵 Broadcaster detenido.")