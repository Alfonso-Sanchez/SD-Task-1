import Pyro4
import curses
import time

def fetch_stats(uri):
    try:
        proxy = Pyro4.Proxy(f"PYRONAME:{uri}")
        return proxy.getStats()
    except Exception as e:
        return {"error": str(e)}

def load_server_uris():
    try:
        with open("servers.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def display_stats(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(1000)

    while True:
        stdscr.clear()
        server_uris = load_server_uris()

        total_sec = 0
        for i, uri in enumerate(server_uris):
            stats = fetch_stats(uri)
            base_row = i * 5
            stdscr.addstr(base_row, 0, f"==== STATS {uri} ====")
            if "error" in stats:
                stdscr.addstr(base_row + 1, 0, f"Error: {stats['error']}")
            else:
                stdscr.addstr(base_row + 1, 0, f"Insultos/segundo:     {stats['insults_per_sec']}")
                stdscr.addstr(base_row + 2, 0, f"Insultos/10 segundos: {stats['insults_per_10s']}")
                stdscr.addstr(base_row + 3, 0, f"Insultos/minuto:      {stats['insults_per_min']}")
                stdscr.addstr(base_row + 4, 0, f"Tiempo de respuesta:  {stats['response_time']}")
                total_sec += stats["insults_per_sec"]

        stdscr.addstr(len(server_uris)*5 + 1, 0, f"Total insultos/segundo: {total_sec}")
        stdscr.addstr(len(server_uris)*5 + 3, 0, "Presiona 'q' para salir.")
        stdscr.refresh()

        if stdscr.getch() == ord('q'):
            break

        time.sleep(2)

def main():
    curses.wrapper(display_stats)

if __name__ == "__main__":
    main()
