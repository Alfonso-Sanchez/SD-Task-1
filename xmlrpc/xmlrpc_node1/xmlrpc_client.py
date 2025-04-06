from xmlrpc.client import ServerProxy
import time

# Dirección del servidor
SERVER_ADDRESS = "http://localhost:8000/"

# Conectar al servidor principal
proxy = ServerProxy(SERVER_ADDRESS)

print("🔴 Cliente XMLRPC conectado al servidor. Solicitando insultos...")

try:
    # Solicitar insultos en un bucle infinito
    while True:
        # Solicitar un insulto al servidor
        insult = proxy.insultame()
        print(f"📜 Insulto recibido: {insult}")
        
except KeyboardInterrupt:
    print("\n🔴 Cliente desconectado.")