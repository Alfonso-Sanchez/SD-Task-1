import pika
import ast
import threading
import time
import curses

stats_data = {
    "Servidor1": {},
    "Servidor2": {}
}

def callback(ch, method, properties, body):
    try:
        mensaje = ast.literal_eval(body.decode())
        servidor = mensaje.get("servidor", "desconocido")
        stats_data[servidor] = mensaje
    except Exception as e:
        pass  # Puedes loguear el error si querés

def consumir_stats():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='stats')
    channel.basic_consume(queue='stats', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

def mostrar_stats(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        try:
            stdscr.addstr(1, 2, "== MONITOR CENTRALIZADO DE SERVIDORES ==")
        except curses.error:
            pass  # por si la pantalla es demasiado pequeña

        row = 3
        for servidor in sorted(stats_data.keys()):
            datos = stats_data[servidor]
            try:
                stdscr.addstr(row, 4, f"[{servidor}]")
                row += 1
                stdscr.addstr(row, 6, f"Insultos únicos recibidos: {datos.get('insultos', 0)}")
                row += 1
                stdscr.addstr(row, 6, f"Frases filtradas: {datos.get('filtrados', 0)}")
                row += 1
                stdscr.addstr(row, 6, f"Solicitudes insulto servidas: {datos.get('solicitudes', 0)}")
                row += 1
                stdscr.addstr(row, 6, f"Peticiones por segundo: {datos.get('solicitudes/segundo', 0)}")
                row += 2
            except curses.error:
                pass  # evita crasheos si no hay espacio
        total_solicitudes_segundo = sum(
            datos.get('solicitudes/segundo', 0) for datos in stats_data.values()
        )
        try:
            stdscr.addstr(row, 4, f"Total peticiones por segundo: {total_solicitudes_segundo}")
        except curses.error:
            pass  # por si la pantalla es demasiado pequeña
        stdscr.refresh()
        time.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=consumir_stats, daemon=True).start()
    curses.wrapper(mostrar_stats)
