import unittest
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import threading

# Función simulada del servidor para devolver un insulto
def insultame():
    return "Eres un idiota"

class TestXMLRPCClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configurar el servidor XML-RPC en un hilo separado
        cls.server = SimpleXMLRPCServer(("localhost", 8000), logRequests=False, allow_none=True)
        cls.server.register_function(insultame, "insultame")
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()

        # Configurar el cliente XML-RPC
        cls.client = ServerProxy("http://localhost:8000/")

    @classmethod
    def tearDownClass(cls):
        # Detener el servidor XML-RPC
        cls.server.shutdown()
        cls.server.server_close()

    def test_insultame(self):
        # Probar que el cliente recibe un insulto del servidor
        insult = self.client.insultame()
        self.assertEqual(insult, "Eres un idiota", "El cliente no recibió el insulto esperado")

if __name__ == "__main__":
    unittest.main()