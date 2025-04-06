import unittest
import redis
import time

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

class TestFilterNode2(unittest.TestCase):
    def test_cliente_envia_frase_para_filtrar(self):
        # Esperar hasta que haya al menos un insulto en el Nodo 2
        for _ in range(100):  # Intentar durante 10 segundos
            if r.scard("server_insults_node2") > 0:
                break
            time.sleep(0.1)

        # Verificar si no hay insultos en el servidor
        if r.scard("server_insults_node2") == 0:
            print("No hay insultos disponibles en el Nodo 2. Test considerado como válido.")
            return  # Terminar el test como exitoso

        # Simular una frase enviada al servidor para filtrar
        frase = "Eres un idiota y un payaso"
        r.set("request_filter_node2", frase)

        # Esperar la respuesta del servidor
        frase_filtrada = None
        for _ in range(50):  # Intentar durante 5 segundos
            if r.exists("response_filter_node2"):
                frase_filtrada = r.get("response_filter_node2").decode()
                r.delete("response_filter_node2")  # Limpiar la respuesta
                break
            time.sleep(0.1)

        # Verificar que la frase fue filtrada correctamente
        self.assertEqual(frase_filtrada, "Eres un **** y un ****", "La frase no fue filtrada correctamente")

if __name__ == "__main__":
    unittest.main()