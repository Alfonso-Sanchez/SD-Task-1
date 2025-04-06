import redis
import time

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Eliminar las claves de insultos al inicio para evitar datos residuales
r.delete("server_insults_node1")
r.delete("server_insults_node2")

# Lista de insultos que el broadcaster enviará
broadcaster_insults = [
    "idiota", "zorra", "cap de cul", "tonto",
    "imbécil", "burro", "payaso", "boba",
    "estúpido", "cretino", "patán", "necio",
    "torpe", "cabezón", "vago", "pesado",
    "inútil", "desgraciado", "miserable",
    "ridículo", "grosero", "insolente",
    "arrogante", "engreído", "despreciable",
    "ignorante", "inepto", "ineficaz",
    "mentecato", "pelmazo", "simplón",
    "cretino", "bufón", "charlatán",
    "desquiciado", "hipócrita", "malcriado",
    "mezquino", "pedante", "presumido",
    "sabelotodo", "soso", "torpe", "traidor",
    "vulgar", "zafio", "zoquete", "cobarde",
    "desalmado", "egoísta", "farsante"
]

print("🔵 Broadcaster iniciado. Enviando insultos a ambos servidores cada 5 segundos...")

try:
    while True:
        # Seleccionar un insulto de la lista del broadcaster
        insult = broadcaster_insults.pop(0)
        broadcaster_insults.append(insult)  # Rotar el insulto

        # Enviar el insulto al Nodo 1
        if not r.sismember("server_insults_node1", insult):
            r.sadd("server_insults_node1", insult)
            print(f"✅ Insulto añadido al Nodo 1: {insult}")

        # Enviar el insulto al Nodo 2
        if not r.sismember("server_insults_node2", insult):
            r.sadd("server_insults_node2", insult)
            print(f"✅ Insulto añadido al Nodo 2: {insult}")

        # Esperar 5 segundos antes de enviar el siguiente insulto
        time.sleep(5)

except KeyboardInterrupt:
    print("\n🔵 Broadcaster detenido.")