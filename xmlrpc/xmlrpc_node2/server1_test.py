import unittest
from xmlrpc.client import ServerProxy
import threading
from xmlrpc.server import SimpleXMLRPCServer

# Simulación del servidor 2 para pruebas
def start_server2():
    insults = [
        "grosero", "arrogante", "engreído", "despreciable",
        "ignorante", "inepto", "ineficaz", "mentecato",
        "pelmazo", "simplón", "bufón", "charlatán"
    ]

    def insultame():
        if insults:
            insult = insults.pop(0)
            insults.append(insult)
            return insult
        return "No hay más insultos disponibles."

    def filtrar_frase(frase):
        for insult in insults:
            if insult in frase:
                frase = frase.replace(insult, "****")
        return frase

    server = SimpleXMLRPCServer(("localhost", 8002), allow_none=True, logRequests=False)
    server.register_function(insultame, "insultame")
    server.register_function(filtrar_frase, "filtrar_frase")
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, insults

class TestServer2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configurar el servidor 2 para pruebas
        cls.server2, cls.server2_insults = start_server2()
        cls.client2 = ServerProxy("http://localhost:8002/")

    @classmethod
    def tearDownClass(cls):
        # Detener el servidor 2 después de las pruebas
        cls.server2.shutdown()

    def test_insultame(self):
        # Probar que el servidor 2 devuelve un insulto
        insult = self.client2.insultame()
        self.assertIn(insult, self.server2_insults, "El insulto no pertenece a la lista del servidor 2")

    def test_filtrar_frase(self):
        # Probar que el servidor 2 filtra una frase correctamente
        frase = "Eres un grosero y un bufón"
        frase_filtrada = self.client2.filtrar_frase(frase)
        self.assertEqual(frase_filtrada, "Eres un **** y un ****", "La frase no fue filtrada correctamente por el servidor 2")

if __name__ == "__main__":
    unittest.main()