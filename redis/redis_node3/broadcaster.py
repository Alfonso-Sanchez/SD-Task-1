import redis
import time

# Conexión a los tres nodos Redis
nodes = [
    redis.Redis(host='localhost', port=6379, db=0),
    redis.Redis(host='localhost', port=6380, db=0),
    redis.Redis(host='localhost', port=6381, db=0)
]

# Lista de insultos
insults = ["idiota", "zorra", "cap de cul", "tonto", "imbécil"]

print("🔵 Broadcaster iniciado. Insertando insultos cada 5s en cada nodo...")

try:
    while True:
        # Rota el primer insulto al final de la lista
        insult = insults.pop(0)
        insults.append(insult)

        # Inserta en cada nodo si tiene <10 insultos (o como prefieras)
        for i, node in enumerate(nodes):
            if node.scard(f"server_insults_node{i+1}") < 10:
                node.sadd(f"server_insults_node{i+1}", insult)
                print(f"✅ Nodo {i+1}: Insulto añadido -> {insult}")

        time.sleep(5)

except KeyboardInterrupt:
    print("\n🔵 Broadcaster detenido.")