import unittest
import redis
import time
import threading

# Configuración de Redis
r = redis.Redis(host='localhost', port=6379, db=0)

def servidor_mock():
    """
    Simula el comportamiento del servidor Redis.
    Lee la solicitud de insulto y responde con un insulto.
    """
    while True:
        if r.exists("request_insult"):
            r.delete("request_insult")  # Eliminar la solicitud
            insult = r.spop("server_insults")  # Obtener un insulto
            if insult:
                r.set("response_insult", insult.decode())  # Responder con el insulto
            break
        time.sleep(0.1)

class TestClientServerInteraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configurar Redis antes de las pruebas
        r.flushdb()  # Limpiar la base de datos de Redis
        r.sadd("server_insults", "idiota")  # Añadir un insulto de prueba

    def test_cliente_solicita_insulto(self):
        # Iniciar el servidor mock en un hilo separado
        servidor_thread = threading.Thread(target=servidor_mock)
        servidor_thread.start()

        # Simular una solicitud de insulto desde el cliente
        r.set("request_insult", "1")

        # Esperar la respuesta del servidor
        insult = None
        for _ in range(20):  # Intentar durante 2 segundos (20 intentos x 0.1s)
            if r.exists("response_insult"):
                insult = r.get("response_insult").decode()
                r.delete("response_insult")  # Limpiar la respuesta
                break
            time.sleep(0.1)

        # Verificar que el insulto recibido es válido
        self.assertIsNotNone(insult, "El servidor no respondió con un insulto")
        self.assertEqual(insult, "idiota", "El insulto recibido no es el esperado")

if __name__ == "__main__":
    unittest.main()