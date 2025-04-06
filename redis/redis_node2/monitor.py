import redis
import time
import curses

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

def main(stdscr):
    # Configuración inicial de curses
    curses.curs_set(0)  # Ocultar el cursor
    stdscr.nodelay(1)   # No bloquear en getch()
    stdscr.clear()

    print("🟢 Monitor de estadísticas iniciado. Mostrando estadísticas de ambos nodos y estadísticas generales...")

    while True:
        # Leer estadísticas del Nodo 1
        stats_node1 = r.hgetall("stats_node1")
        stats_node1 = {k.decode(): int(v) for k, v in stats_node1.items()}

        # Leer estadísticas del Nodo 2
        stats_node2 = r.hgetall("stats_node2")
        stats_node2 = {k.decode(): int(v) for k, v in stats_node2.items()}

        # Calcular estadísticas generales (suma de ambos nodos)
        stats_general = {
            "last_second": stats_node1.get("last_second", 0) + stats_node2.get("last_second", 0),
            "last_10_seconds": stats_node1.get("last_10_seconds", 0) + stats_node2.get("last_10_seconds", 0),
            "total_requests": stats_node1.get("total_requests", 0) + stats_node2.get("total_requests", 0)
        }

        # Mostrar estadísticas del Nodo 1
        stdscr.addstr(0, 0, "📊 Estadísticas del Nodo 1:")
        stdscr.addstr(1, 0, f"📢 Solicitudes en el último segundo: {stats_node1.get('last_second', 0)}")
        stdscr.addstr(2, 0, f"📊 Solicitudes en los últimos 10 segundos: {stats_node1.get('last_10_seconds', 0)}")
        stdscr.addstr(3, 0, f"🔢 Total de solicitudes desde el inicio: {stats_node1.get('total_requests', 0)}")

        # Mostrar estadísticas del Nodo 2
        stdscr.addstr(5, 0, "📊 Estadísticas del Nodo 2:")
        stdscr.addstr(6, 0, f"📢 Solicitudes en el último segundo: {stats_node2.get('last_second', 0)}")
        stdscr.addstr(7, 0, f"📊 Solicitudes en los últimos 10 segundos: {stats_node2.get('last_10_seconds', 0)}")
        stdscr.addstr(8, 0, f"🔢 Total de solicitudes desde el inicio: {stats_node2.get('total_requests', 0)}")

        # Mostrar estadísticas generales
        stdscr.addstr(10, 0, "📊 Estadísticas generales (suma de ambos nodos):")
        stdscr.addstr(11, 0, f"📢 Solicitudes en el último segundo: {stats_general['last_second']}")
        stdscr.addstr(12, 0, f"📊 Solicitudes en los últimos 10 segundos: {stats_general['last_10_seconds']}")
        stdscr.addstr(13, 0, f"🔢 Total de solicitudes desde el inicio: {stats_general['total_requests']}")

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