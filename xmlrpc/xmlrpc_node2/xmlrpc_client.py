from xmlrpc.client import ServerProxy
import time

# Direcciones de los servidores
SERVERS = [
    "http://localhost:8001/",
    "http://localhost:8002/"
]

print("🔴 Cliente XMLRPC conectado. Solicitando insultos, filtrando frases y obteniendo estadísticas...")

try:
    i = 0  # Contador para alternar entre los servidores
    while True:
        # Seleccionar el servidor basado en i % 2
        server_address = SERVERS[i % 2]
        proxy = ServerProxy(server_address)
        print(f"Conectando al servidor: {server_address}")

        # Solicitar un insulto
        insult = proxy.insultame()
        print(f"📜 Insulto recibido: {insult}")

        # Enviar una frase para filtrar
        frase = f"Eres un {insult}"
        frase_filtrada = proxy.filtrar_frase(frase)
        print(f"🔍 Frase filtrada: {frase_filtrada}")

        # Obtener estadísticas del servidor
        stats = proxy.obtener_estadisticas()
        print(f"📊 Estadísticas del servidor: {stats}")

        # Incrementar el contador
        i += 1

except KeyboardInterrupt:
    print("\n🔴 Cliente desconectado.")