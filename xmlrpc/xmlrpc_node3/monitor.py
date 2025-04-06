from xmlrpc.client import ServerProxy
import curses
import time

# Direcciones de los servidores
SERVERS = [
    "http://localhost:8001/",
    "http://localhost:8002/",
    "http://localhost:8003/"
]

def obtener_estadisticas(proxy):
    try:
        return proxy.obtener_estadisticas()
    except Exception as e:
        return {"requests_last_second": 0, "requests_last_10_seconds": 0}

def main(stdscr):
    # Configuración inicial de curses
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.clear()

    # Variables para estadísticas globales
    total_requests_global = 0

    while True:
        try:
            # Obtener estadísticas de cada servidor
            stats_node1 = obtener_estadisticas(ServerProxy(SERVERS[0]))
            stats_node2 = obtener_estadisticas(ServerProxy(SERVERS[1]))
            stats_node3 = obtener_estadisticas(ServerProxy(SERVERS[2]))

            # Calcular estadísticas globales
            requests_last_second_global = stats_node1["requests_last_second"] + stats_node2["requests_last_second"] + stats_node3["requests_last_second"]
            requests_last_10_seconds_global = stats_node1["requests_last_10_seconds"] + stats_node2["requests_last_10_seconds"] + stats_node3["requests_last_10_seconds"]
            total_requests_global += requests_last_second_global

            # Mostrar estadísticas del Nodo 1
            stdscr.addstr(0, 0, "📊 Estadísticas del Nodo 1:")
            stdscr.addstr(1, 0, f"📢 Solicitudes en el último segundo: {stats_node1['requests_last_second']}")
            stdscr.addstr(2, 0, f"📊 Solicitudes en los últimos 10 segundos: {stats_node1['requests_last_10_seconds']}")

            # Mostrar estadísticas del Nodo 2
            stdscr.addstr(4, 0, "📊 Estadísticas del Nodo 2:")
            stdscr.addstr(5, 0, f"📢 Solicitudes en el último segundo: {stats_node2['requests_last_second']}")
            stdscr.addstr(6, 0, f"📊 Solicitudes en los últimos 10 segundos: {stats_node2['requests_last_10_seconds']}")

            # Mostrar estadísticas del Nodo 3
            stdscr.addstr(8, 0, "📊 Estadísticas del Nodo 3:")
            stdscr.addstr(9, 0, f"📢 Solicitudes en el último segundo: {stats_node3['requests_last_second']}")
            stdscr.addstr(10, 0, f"📊 Solicitudes en los últimos 10 segundos: {stats_node3['requests_last_10_seconds']}")

            # Mostrar estadísticas globales
            stdscr.addstr(12, 0, "📊 Estadísticas globales (suma de los tres nodos):")
            stdscr.addstr(13, 0, f"📢 Solicitudes en el último segundo: {requests_last_second_global}")
            stdscr.addstr(14, 0, f"📊 Solicitudes en los últimos 10 segundos: {requests_last_10_seconds_global}")
            stdscr.addstr(15, 0, f"🔢 Total de solicitudes desde el inicio: {total_requests_global}")

            # Refrescar la pantalla de curses
            stdscr.refresh()

            # Salir si se presiona 'q'
            key = stdscr.getch()
            if key == ord('q'):
                break

            # Esperar un segundo antes de actualizar
            time.sleep(1)

        except Exception as e:
            stdscr.addstr(17, 0, f"⚠️ Error: {e}")
            stdscr.refresh()
            time.sleep(1)

# Ejecutar curses
curses.wrapper(main)