import redis
import time
import curses

# Conexión a Redis (asegúrate de que redis-server esté corriendo)
r = redis.Redis(host='localhost', port=6379, db=0)
1
# Función para devolver un insulto
def insultame():
    # Obtener un insulto de la lista `server_insults`
    insult = r.spop("server_insults")
    if insult:
        insult = insult.decode()  # Decodificar el insulto de bytes a string
        r.sadd("server_insults", insult)  # Rotar el insulto (volver a añadirlo)
        return insult
    return "No hay más insultos disponibles."

# Función para filtrar una frase
def filtrar_frase(frase):
    # Obtener todos los insultos almacenados en Redis
    insultos = r.smembers("server_insults")
    insultos = [insulto.decode() for insulto in insultos]  # Decodificar los insultos

    # Censurar los insultos en la frase
    for insulto in insultos:
        if insulto in frase:
            frase = frase.replace(insulto, "****")
    return frase

def main(stdscr):
    # Configuración inicial de curses
    curses.curs_set(0)  # Ocultar el cursor
    stdscr.nodelay(1)   # No bloquear en getch()
    stdscr.clear()

    # Variables para estadísticas
    total_requests = 0
    requests_last_second = 0
    requests_last_10_seconds = 0
    start_time = time.time()
    last_second_time = start_time
    last_10_seconds_time = start_time

    print("🟢 Servidor Redis arrancado. Esperando solicitudes de insultos y frases para filtrar...")

    # Bucle infinito para manejar solicitudes
    while True:
        current_time = time.time()

        # Verificar si hay una solicitud de insulto
        if r.exists("request_insult"):
            # Eliminar la solicitud para evitar procesarla varias veces
            r.delete("request_insult")

            # Generar un insulto y enviarlo al cliente
            insult = insultame()
            r.set("response_insult", insult)
            r.expire("response_insult", 10)  # Establecer un tiempo de expiración

            # Actualizar estadísticas
            total_requests += 1
            requests_last_second += 1
            requests_last_10_seconds += 1

        # Verificar si hay una solicitud de filtrado de frase
        if r.exists("request_filter"):
            # Obtener la frase enviada por el cliente
            frase = r.get("request_filter").decode()
            r.delete("request_filter")  # Eliminar la solicitud

            # Filtrar la frase
            frase_filtrada = filtrar_frase(frase)

            # Enviar la frase filtrada al cliente
            r.set("response_filter", frase_filtrada)
            r.expire("response_filter", 10)  # Establecer un tiempo de expiración

        # Actualizar estadísticas cada segundo
        if current_time - last_second_time >= 1:
            stdscr.addstr(0, 0, f"📢 Solicitudes en el último segundo: {requests_last_second}")
            requests_last_second = 0
            last_second_time = current_time

        # Actualizar estadísticas cada 10 segundos
        if current_time - last_10_seconds_time >= 10:
            stdscr.addstr(1, 0, f"📊 Solicitudes en los últimos 10 segundos: {requests_last_10_seconds}")
            requests_last_10_seconds = 0
            last_10_seconds_time = current_time

        # Mostrar el total acumulado desde el inicio
        stdscr.addstr(2, 0, f"🔢 Total de solicitudes desde el inicio: {total_requests}")

        # Refrescar la pantalla de curses
        stdscr.refresh()

        # Salir si se presiona 'q'
        try:
            key = stdscr.getch()
            if key == ord('q'):
                break
        except Exception:
            pass

# Ejecutar curses
curses.wrapper(main)