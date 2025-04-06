import unittest
from xmlrpc.client import ServerProxy
import threading
from xmlrpc.server import SimpleXMLRPCServer
import time

# Simulación del servidor 3 para pruebas
def start_server3():
    insults = [
        "tonto", "necio", "torpe", "ridículo",
        "patético", "inútil", "inepto", "desgraciado",
        "insensato", "ignorante"
    ]

    # Función para devolver un insulto
    def insultame():
        if insults:
            insult = insults.pop(0)
            insults.append(insult)  # Rotar el insulto
            return insult
        return "No hay más insultos disponibles."

    # Función para filtrar una frase
    def filtrar_frase(frase):
        for insult in insults:
            if insult in frase:
                frase = frase.replace(insult, "****")
        return frase

    # Función para obtener estadísticas
    def obtener_estadisticas():
        return {
            "requests_last_second": 5,
            "requests_last_10_seconds": 50
        }

    # Configurar el servidor
    server = SimpleXMLRPCServer(("localhost", 8003), allow_none=True, logRequests=False)
    server.register_function(insultame, "insultame")
    server.register_function(filtrar_frase, "filtrar_frase")
    server.register_function(obtener_estadisticas, "obtener_estadisticas")
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, insults

class TestServer3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configurar el servidor 3 para pruebas
        cls.server3, cls.server3_insults = start_server3()
        cls.client3 = ServerProxy("http://localhost:8003/")

    @classmethod
    def tearDownClass(cls):
        # Detener el servidor 3 después de las pruebas
        cls.server3.shutdown()

    def test_insultame(self):
        # Probar que el servidor 3 devuelve un insulto
        insult = self.client3.insultame()
        self.assertIn(insult, self.server3_insults, "El insulto no pertenece a la lista del servidor 3")

    def test_filtrar_frase(self):
        # Probar que el servidor 3 filtra una frase correctamente
        frase = "Eres un tonto y un torpe"
        frase_filtrada = self.client3.filtrar_frase(frase)
        self.assertEqual(frase_filtrada, "Eres un **** y un ****", "La frase no fue filtrada correctamente por el servidor 3")

    def test_obtener_estadisticas(self):
        # Probar que el servidor 3 devuelve estadísticas correctamente
        stats = self.client3.obtener_estadisticas()
        self.assertEqual(stats["requests_last_second"], 5, "Las estadísticas del último segundo no son correctas")
        self.assertEqual(stats["requests_last_10_seconds"], 50, "Las estadísticas de los últimos 10 segundos no son correctas")

if __name__ == "__main__":
    unittest.main()