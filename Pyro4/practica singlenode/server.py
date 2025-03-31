import Pyro4
import time
import threading
from collections import deque
import curses

@Pyro4.expose
class InsultServer:
    def __init__(self):
        self.insults = ["capullo", "gilipollas", "fea"]
        self.sentences = []
        self.request_times = deque()

        self.insults_per_sec = 0
        self.insults_per_10s = 0
        self.insults_per_min = 0

        self.lock = threading.Lock()

        metrics_thread = threading.Thread(target=self.update_metrics_loop)
        metrics_thread.daemon = True
        metrics_thread.start()

    def saveInsult(self, sentence):
        result = "No guardado"
        sentence = sentence.strip()

        words = sentence.split()
        censored_words = ["CENSORED" if word.lower() in self.insults else word for word in words]
        filterSentence = " ".join(censored_words)

        if filterSentence not in self.sentences:
            self.sentences.append(filterSentence)
            result = "Guardado"

        with self.lock:
            self.request_times.append(time.time())

        return result

    def clearSentences(self):
        self.sentences.clear()

    def getInsults(self):
        return self.insults

    def getSentences(self):
        return self.sentences

    def update_metrics_loop(self):
        while True:
            now = time.time()
            with self.lock:
                while self.request_times and self.request_times[0] < now - 60:
                    self.request_times.popleft()

                self.insults_per_sec = sum(1 for t in self.request_times if t >= now - 1)
                self.insults_per_10s = sum(1 for t in self.request_times if t >= now - 10)
                self.insults_per_min = len(self.request_times)
            time.sleep(1)

def display_stats(stdscr, server):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(1000)

    while True:
        with server.lock:
            sec = server.insults_per_sec
            ten = server.insults_per_10s
            minute = server.insults_per_min

        stdscr.clear()
        stdscr.addstr(0, 0, f"Insultos enviados/segundo:     {sec}")
        stdscr.addstr(1, 0, f"Insultos enviados/10 segundos: {ten}")
        stdscr.addstr(2, 0, f"Insultos enviados/1 minuto:    {minute}")
        stdscr.addstr(4, 0, "Presiona 'q' para salir.")
        stdscr.refresh()

        if stdscr.getch() == ord('q'):
            break

def main():
    server = InsultServer()

    def start_pyro4_server():
        Pyro4.Daemon.serveSimple(
            {
                server: "example.insultserver"
            },
            ns=True
        )

    pyro_thread = threading.Thread(target=start_pyro4_server)
    pyro_thread.daemon = True
    pyro_thread.start()

    curses.wrapper(display_stats, server)

if __name__ == "__main__":
    main()
