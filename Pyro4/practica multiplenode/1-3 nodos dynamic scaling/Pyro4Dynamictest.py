import unittest
import Pyro4
import time
import threading
import random

# Constantes de carga
LOAD_LOW = 5      # Carga baja: 5 solicitudes por segundo
LOAD_MEDIUM = 15  # Carga media: 20 solicitudes por segundo (para escalar a 2)
LOAD_HIGH = 400   # Carga alta: 400 solicitudes por segundo (para máximo escalado)

class TestInsultFilterScaling(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proxies = {}  # Diccionario de proxies activos
        cls.max_servers = 5  # Coincide con MAX_SERVERS en dynamic_cluster.py
        cls.load_threads = []
        cls.running = True
        cls.server_uris = []  # Lista de URIs desde servers.txt
        
        # Leer URIs iniciales desde servers.txt
        timeout = 10
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                with open("servers.txt", "r") as file:
                    cls.server_uris = [line.strip() for line in file if line.strip()]
                if cls.server_uris:  # Asegurarse de que hay al menos un servidor
                    proxy = Pyro4.Proxy(f"PYRONAME:{cls.server_uris[0]}")
                    proxy.getSentences()
                    cls.proxies[cls.server_uris[0]] = proxy
                    break
            except (FileNotFoundError, Pyro4.errors.PyroError):
                time.sleep(1)
        else:
            raise Exception("No se pudo conectar al servidor inicial o servers.txt no existe")

    def setUp(self):
        # Limpiar todos los servidores antes de cada prueba
        for proxy in self.proxies.values():
            try:
                proxy.clearSentences()
            except:
                pass
        # Detener hilos de carga previos
        self.running = False
        for thread in self.load_threads:
            thread.join()
        self.load_threads = []
        self.running = True

    def tearDown(self):
        # Detener carga y limpiar hilos
        self.running = False
        for thread in self.load_threads:
            thread.join()

    def generate_load(self, proxies, intensity=1, duration=None):
        """Generar carga distribuida entre todos los servidores activos."""
        def load_thread():
            sentences = [
                "Hola mundo",
                "Eres un capullo",
                "Que gilipollas eres",
                "Todo bien fea"
            ]
            start_time = time.time()
            while self.running and (duration is None or (time.time() - start_time) < duration):
                # Elegir un proxy aleatorio para distribuir la carga
                proxy = random.choice(list(proxies.values()))
                proxy.saveInsult(random.choice(sentences))
                time.sleep(1/intensity)
        thread = threading.Thread(target=load_thread)
        thread.daemon = True
        thread.start()
        self.load_threads.append(thread)

    def get_active_servers(self):
        """Obtener servidores activos desde servers.txt, similar al cliente."""
        active = {}
        try:
            with open("servers.txt", "r") as file:
                uris = [line.strip() for line in file if line.strip()]
            for uri in uris:
                try:
                    proxy = Pyro4.Proxy(f"PYRONAME:{uri}")
                    proxy.getSentences()  # Verificar conexión
                    active[uri] = proxy
                except Pyro4.errors.PyroError:
                    continue
        except FileNotFoundError:
            raise Exception("El archivo servers.txt no existe")
        
        self.proxies = active
        self.server_uris = list(active.keys())
        return len(active)

    # Pruebas de servidor único
    def test_single_server_basic(self):
        """Probar funcionalidad básica con una sola frase"""
        proxy = list(self.proxies.values())[0]  # Usar el primer servidor activo
        result = proxy.saveInsult("Hola mundo")
        self.assertEqual(result, "Guardado")
        self.assertEqual(proxy.getSentences(), ["Hola mundo"])

    def test_single_server_insult_filter(self):
        """Probar el filtro de insultos"""
        proxy = list(self.proxies.values())[0]
        result = proxy.saveInsult("Eres un capullo y gilipollas")
        self.assertEqual(result, "Guardado")
        self.assertEqual(proxy.getSentences(), ["Eres un CENSORED y CENSORED"])

    def test_single_server_duplicate(self):
        """Probar que frases repetidas no se guardan"""
        proxy = list(self.proxies.values())[0]
        result1 = proxy.saveInsult("Hola capullo")
        self.assertEqual(result1, "Guardado")
        result2 = proxy.saveInsult("Hola capullo")
        self.assertEqual(result2, "No guardado")
        self.assertEqual(proxy.getSentences(), ["Hola CENSORED"])

    # Pruebas de escalado
    def test_scale_to_max_servers(self):
        """Probar escalado a 2 servidores con carga media"""
        # Verificar estado inicial
        timeout = 20
        start_time = time.time()
        while time.time() - start_time < timeout:
            initial_servers = self.get_active_servers()
            print(f"[DEBUG] Servidores iniciales: {initial_servers}, URIs: {self.server_uris}")
            if initial_servers >= 1:
                break
            time.sleep(1)
        self.assertGreaterEqual(initial_servers, 1, "No se detectó al menos 1 servidor inicial")
        
        # Generar carga media distribuida y mantenerla hasta el final del test
        print(f"[DEBUG] Generando carga media (intensity={LOAD_HIGH}) en {len(self.proxies)} servidores")
        self.generate_load(self.proxies, intensity=LOAD_HIGH)  # Sin duration, se mantiene activa
        
        # Monitorear escalado mientras la carga está activa
        max_servers_observed = initial_servers
        timeout = 12
        start_time = time.time()
        while time.time() - start_time < timeout:
            current_servers = self.get_active_servers()
            max_servers_observed = max(max_servers_observed, current_servers)
            print(f"[DEBUG] Servidores activos: {current_servers}, URIs: {self.server_uris}")
            if current_servers >= 5:
                break
            time.sleep(1)
        
        # Verificar que se alcanzó al menos 2 servidores
        self.assertGreaterEqual(max_servers_observed, 5, 
                            f"El máximo número de servidores observado fue {max_servers_observed}, esperado al menos 5")
        
        # Esperar un momento para que servers.txt se estabilice
        time.sleep(3)
        final_servers = self.get_active_servers()
        print(f"[DEBUG] Servidores finales después de espera: {final_servers}, URIs: {self.server_uris}")
        
        # Detener la carga al final del test
        self.running = False
        for thread in self.load_threads:
            thread.join()
        self.load_threads = []

    def test_scale_down(self):
        """Probar reducción de servidores tras eliminar carga"""
        # Primero escalar al máximo
        timeout = 20
        start_time = time.time()
        while time.time() - start_time < timeout:
            initial_servers = self.get_active_servers()
            print(f"[DEBUG] Servidores iniciales: {initial_servers}, URIs: {self.server_uris}")
            if initial_servers >= 1:
                break
            time.sleep(1)
        self.assertGreaterEqual(initial_servers, 1, "No se detectó al menos 1 servidor inicial")
        
        print(f"[DEBUG] Generando carga alta para escalar al máximo (intensity={LOAD_HIGH})")
        self.generate_load(self.proxies, intensity=LOAD_HIGH)  # Carga continua
        
        max_servers_observed = initial_servers
        timeout = 12
        start_time = time.time()
        while time.time() - start_time < timeout:
            current_servers = self.get_active_servers()
            max_servers_observed = max(max_servers_observed, current_servers)
            print(f"[DEBUG] Servidores activos durante escalado: {current_servers}, URIs: {self.server_uris}")
            if current_servers >= self.max_servers:
                break
            time.sleep(1)
        
        # Verificar que se alcanzó el máximo (5 servidores)
        self.assertEqual(max_servers_observed, self.max_servers, 
                        f"El máximo número de servidores observado fue {max_servers_observed}, esperado {self.max_servers}")
        
        # Detener carga
        print("[DEBUG] Deteniendo carga para permitir reducción")
        self.running = False
        for thread in self.load_threads:
            thread.join()
        self.load_threads = []
        
        # Esperar reducción (hasta 20 segundos o hasta que baje a 1 servidor)
        timeout = 20
        start_time = time.time()
        min_servers_observed = self.max_servers
        while time.time() - start_time < timeout:
            current_servers = self.get_active_servers()
            min_servers_observed = min(min_servers_observed, current_servers)
            print(f"[DEBUG] Servidores activos durante reducción: {current_servers}, URIs: {self.server_uris}")
            if current_servers <= 1:  # Parar si se alcanza 1 servidor
                break
            time.sleep(1)
        
        # Verificar que el número de servidores se redujo a 1
        final_servers = self.get_active_servers()
        print(f"[DEBUG] Servidores finales después de reducción: {final_servers}, URIs: {self.server_uris}")
        self.assertEqual(final_servers, 1, f"El número final de servidores fue {final_servers}, esperado 1")

if __name__ == "__main__":
    unittest.main()