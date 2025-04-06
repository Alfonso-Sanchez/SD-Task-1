# monitor.py
from rediscluster import RedisCluster
import curses

startup_nodes = [
    {"host": "127.0.0.1", "port": 7000},
    {"host": "127.0.0.1", "port": 7001},
    {"host": "127.0.0.1", "port": 7002}
]

def main(stdscr):
    r = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.clear()

    while True:
        try:
            stats = r.hgetall("stats_cluster")
            last_second = stats.get("last_second", "0")
            last_10s = stats.get("last_10_seconds", "0")
            total = stats.get("total_requests", "0")

            stdscr.clear()
            stdscr.addstr(0, 0, "📊 Estadísticas del Cluster:")
            stdscr.addstr(1, 0, f"   Último segundo: {last_second}")
            stdscr.addstr(2, 0, f"   Últimos 10 seg: {last_10s}")
            stdscr.addstr(3, 0, f"   Total Requests: {total}")
            stdscr.addstr(5, 0, "Pulsa 'q' para salir.")
            stdscr.refresh()

            key = stdscr.getch()
            if key == ord('q'):
                break

        except curses.error:
            stdscr.clear()
            stdscr.addstr(0, 0, "⚠️ El terminal es demasiado pequeño.")
            stdscr.refresh()

curses.wrapper(main)