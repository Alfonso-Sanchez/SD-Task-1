import redis
import time

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Eliminar la clave `server_insults` al inicio para evitar datos residuales
r.delete("server_insults")

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

print("🔵 Broadcaster iniciado. Enviando insultos al servidor cada 5 segundos...")

try:
    while True:
        # Seleccionar un insulto de la lista del broadcaster
        insult = broadcaster_insults.pop(0)
        broadcaster_insults.append(insult)  # Rotar el insulto

        # Verificar si el insulto ya está en la lista del servidor
        if not r.sismember("server_insults", insult):
            # Añadir el insulto a la lista del servidor
            r.sadd("server_insults", insult)
            print(f"✅ Insulto añadido al servidor: {insult}")
        else:
            print(f"⚠️ Insulto ya existente en el servidor: {insult}")

        # Esperar 5 segundos antes de enviar el siguiente insulto
        time.sleep(5)

except KeyboardInterrupt:
    print("\n🔵 Broadcaster detenido.")