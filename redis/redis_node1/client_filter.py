import redis
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
            print(f"Enviando frase: {frase}")

            # Enviar la frase al servidor
            r.set("request_filter", frase)

            # Esperar la respuesta del servidor
            while not r.exists("response_filter"):
                pass  # Esperar activamente

            # Obtener la frase filtrada
            frase_filtrada = r.get("response_filter").decode()
            r.delete("response_filter")  # Eliminar la respuesta después de procesarla

            # Mostrar la frase filtrada
            print(f"Frase filtrada: {frase_filtrada}")

except KeyboardInterrupt:
    print("\n🔴 Cliente desconectado.")