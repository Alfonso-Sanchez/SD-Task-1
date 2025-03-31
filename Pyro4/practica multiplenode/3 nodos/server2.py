import Pyro4
import time
import threading
from collections import deque

@Pyro4.expose
class InsultServer:
    def __init__(self):
        self.insults = ["capullo", "gilipollas", "fea"]
        self.sentences = []
        self.request_times = deque()  # timestamps de cada petición

        self.insults_per_sec = 0
        self.insults_per_10s = 0
        self.insults_per_min = 0

        self.lock = threading.Lock()

        # Iniciar hilo de métricas
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
        with self.lock:
            self.sentences.clear()

    def getInsults(self):
        return self.insults

    def getSentences(self):
        return self.sentences

    def getStats(self):
        with self.lock:
            return {
                "insults_per_sec": self.insults_per_sec,
                "insults_per_10s": self.insults_per_10s,
                "insults_per_min": self.insults_per_min
            }

    def update_metrics_loop(self):
        while True:
            now = time.time()
            with self.lock:
                # Eliminar peticiones que ocurrieron hace más de 60s
                while self.request_times and self.request_times[0] < now - 60:
                    self.request_times.popleft()

                self.insults_per_sec = sum(1 for t in self.request_times if t >= now - 1)
                self.insults_per_10s = sum(1 for t in self.request_times if t >= now - 10)
                self.insults_per_min = len(self.request_times)

            time.sleep(1)

def main():
    server = InsultServer()

    def start_pyro4_server():
        Pyro4.Daemon.serveSimple(
            {
                server: "example.insultserver2"
            },
            ns=True
        )

    pyro4_thread = threading.Thread(target=start_pyro4_server)
    pyro4_thread.daemon = True
    pyro4_thread.start()

    pyro4_thread.join()

if __name__ == "__main__":
    main()
