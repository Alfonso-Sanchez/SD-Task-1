from xmlrpc.server import SimpleXMLRPCServer
import threading
import time

# Lista de insultos para el servidor 2
insults = [
    "grosero", "arrogante", "engreído", "despreciable",
    "ignorante", "inepto", "ineficaz", "mentecato",
    "pelmazo", "simplón", "bufón", "charlatán"
]

# Variables para estadísticas
total_requests = 0
requests_last_second = 0
requests_last_10_seconds = 0
lock = threading.Lock()

# Función para devolver un insulto
def insultame():
    global total_requests, requests_last_second, requests_last_10_seconds
    with lock:
        total_requests += 1
        requests_last_second += 1
        requests_last_10_seconds += 1
    if insults:
        insult = insults.pop(0)
        insults.append(insult)  # Rotar el insulto
        return insult
    return "No hay más insultos disponibles."

# Función para filtrar una frase
def filtrar_frase(frase):
    global total_requests, requests_last_second, requests_last_10_seconds
    with lock:
        total_requests += 1
        requests_last_second += 1
        requests_last_10_seconds += 1
    for insult in insults:
        if insult in frase:
            frase = frase.replace(insult, "****")
    return frase

# Función para obtener estadísticas
def obtener_estadisticas():
    with lock:
        return {
            "requests_last_second": requests_last_second,
            "requests_last_10_seconds": requests_last_10_seconds
        }

# Hilo para reiniciar el contador de solicitudes por segundo
def reset_requests_last_second():
    global requests_last_second
    while True:
        time.sleep(1)
        with lock:
            requests_last_second = 0

# Hilo para reiniciar el contador de solicitudes de los últimos 10 segundos
def reset_requests_last_10_seconds():
    global requests_last_10_seconds
    while True:
        time.sleep(10)
        with lock:
            requests_last_10_seconds = 0

# Iniciar los hilos
thread1 = threading.Thread(target=reset_requests_last_second, daemon=True)
thread2 = threading.Thread(target=reset_requests_last_10_seconds, daemon=True)
thread1.start()
thread2.start()

# Iniciar el servidor XML-RPC
server = SimpleXMLRPCServer(("localhost", 8002), allow_none=True, logRequests=False)
server.register_function(insultame, "insultame")
server.register_function(filtrar_frase, "filtrar_frase")
server.register_function(obtener_estadisticas, "obtener_estadisticas")

print("🟢 Servidor XMLRPC Nodo 2 corriendo en puerto 8002...")
server.serve_forever()