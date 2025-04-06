import Pyro4
import curses
import time
import matplotlib
matplotlib.use("TkAgg")  # <-- Fuerza uso de backend interactivo
import matplotlib.pyplot as plt

SAVE_PLOT = True

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
        print("⚠️ Archivo 'servers.txt' no encontrado.")
        return []

def generate_live_plot(duration_sec=60, interval=5):
    print("📊 Iniciando gráfica en vivo...")

    plt.ion()  # Activar modo interactivo
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    tiempos = []
    mensajes = []
    servidores = []

    try:
        for t in range(duration_sec // interval):
            print(f"\n⏱️ Iteración {t + 1}")
            server_uris = load_server_uris()
            total_mensajes = 0
            servidores_activos = 0

            for uri in server_uris:
                stats = fetch_stats(uri)
                print(f"📡 Stats {uri}: {stats}")
                if "error" not in stats:
                    total_mensajes += stats.get("insults_per_sec", 0)
                    servidores_activos += 1

            tiempos.append(t * interval)
            mensajes.append(total_mensajes)
            servidores.append(servidores_activos)

            ax1.clear()
            ax2.clear()

            # Barras para mensajes
            ax1.bar(tiempos, mensajes, width=interval * 0.6, color='#2f6587', label='Mensajes / segundo')
            ax1.set_ylabel("Mensajes / segundo")
            ax1.set_xlabel("Tiempo")
            ax1.set_xticks(tiempos)
            ax1.set_xticklabels([f"{x}s" for x in tiempos])
            ax1.legend(loc='lower center')

            # Línea para servidores
            ax2.plot(tiempos, servidores, color='#f26c23', marker='o', label='Servidores')
            ax2.set_ylabel("Servidores")
            ax2.legend(loc='upper right')

            plt.title("SCALING")
            plt.tight_layout()
            plt.pause(0.1)

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n🛑 Interrupción detectada. Guardando gráfica antes de salir...")

    finally:
        plt.ioff()
        if SAVE_PLOT:
            plt.savefig("scaling_plot.png")
            print("✅ Gráfica guardada como 'scaling_plot.png'")
        plt.show()

def display_stats(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(1000)

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        server_uris = load_server_uris()

        required_height = len(server_uris) * 5 + 4  # Líneas necesarias para mostrar todo

        if height < required_height:
            stdscr.addstr(0, 0, f"La ventana del terminal es demasiado pequeña ({height} líneas).")
            stdscr.addstr(1, 0, f"Se necesitan al menos {required_height} líneas para mostrar todo.")
            stdscr.addstr(3, 0, "Aumenta el tamaño de la ventana o presiona 'q' para salir.")
        else:
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
    print("==== STATS MODE ====")
    print("1) Activar gráfica")
    print("2) Activar modo consola (curses)")
    opcion = input("Selecciona una opción (1/2): ").strip()

    if opcion == '1':
        try:
            tiempo = int(input("⏱️ Tiempo de graficado en segundos (máximo 600): ").strip())
            if tiempo <= 0 or tiempo > 600:
                print("⚠️ Tiempo fuera de rango. Usando 60s por defecto.")
                tiempo = 60
        except ValueError:
            print("⚠️ Entrada inválida. Usando 60s por defecto.")
            tiempo = 60
        
        try:
            interval = int(input("⏱️ Intervalo de actualización en segundos (mínimo: 2 | máximo: 10): ").strip())
            if interval <= 2 or interval > 10:
                print("⚠️ Intervalo fuera de rango. Usando 5s por defecto.")
                interval = 5
        except ValueError:
            print("⚠️ Entrada inválida. Usando 5s por defecto.")
            interval = 5

        print(f"🕒 Graficando durante {tiempo} segundos con intervalos de {interval} segundos.")
        generate_live_plot(duration_sec=tiempo, interval=interval)
    elif opcion == '2':
        curses.wrapper(display_stats)
    else:
        print("❌ Opción inválida. Saliendo.")

if __name__ == "__main__":
    main()
