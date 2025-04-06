from xmlrpc.server import SimpleXMLRPCServer
import curses
import time

# Lista de insultos (puedes modificar o añadir más)
insults = [
    "idiota", "zorra", "cap de cul", "tonto",
    "imbécil", "burro", "payaso", "bobo",
    "estúpido", "cretino"
]

# Función para devolver un insulto
def insultame():
    if insults:
        insult = insults.pop(0)
        insults.append(insult)  # Rotar el insulto
        return insult
    return "No hay más insultos disponibles."

def curses_main(stdscr):
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

    # Mostrar encabezado inicial
    stdscr.addstr(0, 0, "📊 Estadísticas del servidor XMLRPC")
    stdscr.addstr(1, 0, "-" * 40)

    print("🟢 Servidor XMLRPC corriendo en puerto 8000...")

    # Iniciar el servidor XMLRPC
    server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True, logRequests=False)
    server.register_function(insultame, "insultame")

    # Bucle infinito para manejar solicitudes
    while True:
        current_time = time.time()

        # Manejar solicitudes del cliente
        server.handle_request()

        # Actualizar estadísticas
        total_requests += 1
        requests_last_second += 1
        requests_last_10_seconds += 1

        # Actualizar estadísticas cada segundo
        if current_time - last_second_time >= 1:
            stdscr.addstr(2, 0, f"📢 Solicitudes en el último segundo: {requests_last_second}")
            requests_last_second = 0
            last_second_time = current_time

        # Actualizar estadísticas cada 10 segundos
        if current_time - last_10_seconds_time >= 10:
            stdscr.addstr(3, 0, f"📊 Solicitudes en los últimos 10 segundos: {requests_last_10_seconds}")
            requests_last_10_seconds = 0
            last_10_seconds_time = current_time

        # Mostrar el total acumulado desde el inicio
        stdscr.addstr(4, 0, f"🔢 Total de solicitudes desde el inicio: {total_requests}")

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
curses.wrapper(curses_main)