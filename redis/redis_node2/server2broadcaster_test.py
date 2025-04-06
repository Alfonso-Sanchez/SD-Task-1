import unittest
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

class TestBroadcasterNode2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        r.delete("server_insults_node2")  # Limpiar la lista de insultos del Nodo 2

    def test_broadcaster_envia_insultos(self):
        insulto = "payaso"
        r.sadd("server_insults_node2", insulto)
        self.assertTrue(r.sismember("server_insults_node2", insulto), "El insulto no fue añadido correctamente al Nodo 2")

if __name__ == "__main__":
    unittest.main()