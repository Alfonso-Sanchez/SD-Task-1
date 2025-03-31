import Pyro4
import threading
import time
import sys
import os
import subprocess
import signal
from collections import deque

# ===== CONFIGURACIÓN DE ESCALADO =====
MIN_SERVERS = 1
MAX_SERVERS = 5
SERVER_CAPACITY = 5            # mensajes por segundo por servidor (ajusta también)
SCALING_INTERVAL = 3  # segundos entre chequeos
SIMULATED_RESPONSE_TIME = 0.5
REAL_MODE = False
MAX_SCALING_SERVERS = 2
MAX_DOWNGRADING_SERVERS = 1

# ====== SERVIDOR DE INSULTOS ======
@Pyro4.expose
class InsultServer:
    def __init__(self):
        self.insults = ["capullo", "gilipollas", "fea"]
        self.sentences = []
        self.request_times = deque()
        self.lock = threading.Lock()
        self.insults_per_sec = 0
        self.insults_per_10s = 0
        self.insults_per_min = 0
        self.response_time = 0

        metrics_thread = threading.Thread(target=self.update_metrics_loop)
        metrics_thread.daemon = True
        metrics_thread.start()

    def saveInsult(self, sentence):
        start_time = time.time()
        result = "No guardado"
        words = sentence.split()
        filtered = ["CENSORED" if word.lower() in self.insults else word for word in words]
        sentence = " ".join(filtered)

        with self.lock:
            if sentence not in self.sentences:
                self.sentences.append(sentence)
                result = "Guardado"
            self.request_times.append(time.time())
        self.response_time = time.time() - start_time
        return result

    def getStats(self):
        if (REAL_MODE):
            with self.lock:
                return {
                    "insults_per_sec": self.insults_per_sec,
                    "insults_per_10s": self.insults_per_10s,
                    "insults_per_min": self.insults_per_min,
                    "response_time": self.response_time
                }
        else:
            with self.lock:
                return {
                    "insults_per_sec": self.insults_per_sec,
                    "insults_per_10s": self.insults_per_10s,
                    "insults_per_min": self.insults_per_min,
                    "response_time": SIMULATED_RESPONSE_TIME
                }

    def getSentences(self):
        return self.sentences
    
    def clearSentences(self):
        with self.lock:
            self.sentences.clear()

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

# ====== ESCALADOR Y GESTOR ======
active_servers = {}  # id: process 

def start_server(server_id): # Creación de nuevos servidores (procesos)
    env = os.environ.copy()
    env["SERVER_ID"] = str(server_id)
    proc = subprocess.Popen([sys.executable, __file__, str(server_id)], env=env)
    active_servers[server_id] = proc
    print(f"[Scaler] Servidor {server_id} iniciado.")
    update_server_list_file()

def stop_server(server_id): # Eliminación del servidor indicado por ID. 
    proc = active_servers.pop(server_id, None)
    if proc:
        proc.terminate()
        print(f"[Scaler] Servidor {server_id} detenido.")
        update_server_list_file()

def get_server_proxy(server_id):
    return Pyro4.Proxy(f"PYRONAME:example.insultserver{server_id}")  # Todos comparten el mismo nombre base, solo tienen un ID añadido

def get_total_load(metric="insults_per_sec"): # Obtiene la carga total del servidor!
    total = 0
    for sid in list(active_servers):
        try:
            proxy = get_server_proxy(sid)
            stats = proxy.getStats()
            total += stats.get(metric, 0)
        except Exception as e:
            print(f"[Scaler] Error obteniendo stats de server {sid}: {e}")
    return total
def get_average_time(): # Obtiene el tiempo promedio de respuesta de todos los servidores
    total = 0
    for sid in list(active_servers):
        try: 
            proxy = get_server_proxy(sid)
            stats = proxy.getStats()
            total += stats.get("response_time", 0)
        except Exception as e:
            print(f"[Scaler] Error obteniendo el tiempo promedio de server {sid} : {e}")
    if not active_servers:
        return 0
    else: 
        return total / len(active_servers)

def update_server_list_file(): # Actualiza la lista de servidores disponibles para que stats.py y los clientes lo actualicen. 
    with open("servers.txt", "w") as f:
        for sid in active_servers:
            f.write(f"example.insultserver{sid}\n")

def scaler_loop():
    import math
    next_id = 1
    for _ in range(MIN_SERVERS):
        start_server(next_id)
        next_id += 1

    while True:
        time.sleep(SCALING_INTERVAL)
        total_load = get_total_load("insults_per_sec")  # λ

        average = get_average_time()
        current_count = len(active_servers)
        
        # Fórmula: N = ceil((λ × T) / C)
        if (REAL_MODE):
            required_servers = math.ceil((total_load * average) / SERVER_CAPACITY)
        else: 
            required_servers = math.ceil((total_load * SIMULATED_RESPONSE_TIME) / SERVER_CAPACITY)

        # Limitar a los rangos permitidos
        required_servers = max(MIN_SERVERS, min(MAX_SERVERS, required_servers))

        if required_servers > current_count:
            required = required_servers - current_count
            if ((required) > MAX_SCALING_SERVERS):
                required = MAX_SCALING_SERVERS

            for _ in range(required):
                start_server(next_id)
                next_id += 1

        elif required_servers < current_count:
            required = current_count - required_servers
            if ((required) > MAX_DOWNGRADING_SERVERS):
                required = MAX_DOWNGRADING_SERVERS

            for _ in range(required):
                max_id = max(active_servers)
                stop_server(max_id)

# ====== LANZADOR ======
def run_server_instance(server_id):
    server = InsultServer()
    Pyro4.Daemon.serveSimple({server: f"example.insultserver{server_id}"}, ns=True)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        # Ejecutar como servidor individual
        run_server_instance(sys.argv[1])
    else:
        # Ejecutar como gestor principal
        print("[Scaler] Iniciando gestor de escalado dinámico...")
        try:
            scaler_loop()
        except KeyboardInterrupt:
            print("[Scaler] Apagando todos los servidores...")
            for sid in list(active_servers):
                stop_server(sid)
