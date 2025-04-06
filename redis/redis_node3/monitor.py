import redis
import curses

nodes = [
    redis.Redis(host='localhost', port=6379, db=0),
    redis.Redis(host='localhost', port=6380, db=0),
    redis.Redis(host='localhost', port=6381, db=0)
]

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.clear()

    while True:
        try:
            stats = []
            for i, node in enumerate(nodes):
                try:
                    data = node.hgetall(f"stats_node{i+1}")
                    stats.append({
                        k.decode(): int(v)
                        for k, v in data.items()
                    })
                except redis.ConnectionError:
                    stats.append({"last_second": 0, "last_10_seconds": 0, "total_requests": 0})

            # Sumar stats globales
            stats_general = {
                "last_second": sum(s.get("last_second", 0) for s in stats),
                "last_10_seconds": sum(s.get("last_10_seconds", 0) for s in stats),
                "total_requests": sum(s.get("total_requests", 0) for s in stats)
            }

            stdscr.clear()
            for i, node_stats in enumerate(stats):
                stdscr.addstr(i * 4, 0, f"📊 Nodo {i+1}:")
                stdscr.addstr(i * 4 + 1, 0, f"   Último segundo: {node_stats.get('last_second', 0)}")
                stdscr.addstr(i * 4 + 2, 0, f"   Últimos 10 seg: {node_stats.get('last_10_seconds', 0)}")
                stdscr.addstr(i * 4 + 3, 0, f"   Total: {node_stats.get('total_requests', 0)}")

            offset = len(nodes) * 4
            stdscr.addstr(offset, 0, "📊 Estadísticas generales:")
            stdscr.addstr(offset + 1, 0, f"   Último segundo: {stats_general['last_second']}")
            stdscr.addstr(offset + 2, 0, f"   Últimos 10 seg: {stats_general['last_10_seconds']}")
            stdscr.addstr(offset + 3, 0, f"   Total: {stats_general['total_requests']}")

            stdscr.refresh()

            key = stdscr.getch()
            if key == ord('q'):
                break

        except curses.error:
            stdscr.clear()
            stdscr.addstr(0, 0, "⚠️ El terminal es demasiado pequeño.")
            stdscr.refresh()

curses.wrapper(main)