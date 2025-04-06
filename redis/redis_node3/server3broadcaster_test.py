import unittest
import redis

# Configuración de Redis
r = redis.Redis(host='localhost', port=6381, db=0)

class TestBroadcaster(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configurar Redis antes de las pruebas
        r.delete("server_insults")  # Limpiar la lista de insultos

    def test_broadcaster_envia_insultos(self):
        # Simular el envío de un insulto por el broadcaster
        insulto = "nuevo_insulto"
        r.sadd("server_insults", insulto)

        # Verificar que el insulto fue añadido al servidor
        self.assertTrue(r.sismember("server_insults", insulto), "El insulto no fue añadido al servidor por el broadcaster")

if __name__ == "__main__":
    unittest.main()