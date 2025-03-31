import Pyro4
import curses
import time

def fetch_stats(server_uri):
    try:
        proxy = Pyro4.Proxy(server_uri)
        return proxy.getStats()
    except Exception as e:
        return {"error": str(e)}

def display_stats(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(1000)

    uri1 = "PYRONAME:example.insultserver1"
    uri2 = "PYRONAME:example.insultserver2"

    while True:
        stdscr.clear()

        stats1 = fetch_stats(uri1)
        stats2 = fetch_stats(uri2)

        stdscr.addstr(0, 0, "==== STATS SERVER 1 ====")
        if "error" in stats1:
            stdscr.addstr(1, 0, f"Error: {stats1['error']}")
        else:
            stdscr.addstr(1, 0, f"Insultos/segundo:     {stats1['insults_per_sec']}")
            stdscr.addstr(2, 0, f"Insultos/10 segundos: {stats1['insults_per_10s']}")
            stdscr.addstr(3, 0, f"Insultos/minuto:      {stats1['insults_per_min']}")

        stdscr.addstr(5, 0, "==== STATS SERVER 2 ====")
        if "error" in stats2:
            stdscr.addstr(6, 0, f"Error: {stats2['error']}")
        else:
            stdscr.addstr(6, 0, f"Insultos/segundo:     {stats2['insults_per_sec']}")
            stdscr.addstr(7, 0, f"Insultos/10 segundos: {stats2['insults_per_10s']}")
            stdscr.addstr(8, 0, f"Insultos/minuto:      {stats2['insults_per_min']}")

        stdscr.addstr(10, 0, "Presiona 'q' para salir.")
        stdscr.refresh()

        if stdscr.getch() == ord('q'):
            break

        time.sleep(2)

def main():
    curses.wrapper(display_stats)

if __name__ == "__main__":
    main()
