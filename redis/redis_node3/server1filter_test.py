import unittest
import redis
import time
import threading

# Configuración de Redis
r = redis.Redis(host='localhost', port=6379, db=0)

def servidor_mock_filter():
    """
    Simula el comportamiento del servidor Redis para filtrar frases.
    Lee la solicitud de filtro y responde con la frase filtrada.
    """
    while True:
        if r.exists("request_filter"):
            frase = r.get("request_filter").decode()
            r.delete("request_filter")  # Eliminar la solicitud

            # Filtrar insultos
            insultos = [i.decode() for i in r.smembers("server_insults")]
            for insulto in insultos:
                frase = frase.replace(insulto, "****")

            # Responder con la frase filtrada
            r.set("response_filter", frase)
            break
        time.sleep(0.1)

class TestFilterInteraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configurar Redis antes de las pruebas
        r.flushdb()  # Limpiar la base de datos de Redis
        r.sadd("server_insults", "idiota")  # Añadir un insulto de prueba
        r.sadd("server_insults", "payaso")  # Añadir otro insulto de prueba

    def test_cliente_envia_frase_para_filtrar(self):
        # Iniciar el servidor mock en un hilo separado
        servidor_thread = threading.Thread(target=servidor_mock_filter)
        servidor_thread.start()

        # Simular una frase enviada al servidor para filtrar
        frase = "Eres un idiota y un payaso"
        r.set("request_filter", frase)

        # Esperar la respuesta del servidor
        frase_filtrada = None
        for _ in range(20):  # Intentar durante 2 segundos (20 intentos x 0.1s)
            if r.exists("response_filter"):
                frase_filtrada = r.get("response_filter").decode()
                r.delete("response_filter")  # Limpiar la respuesta
                break
            time.sleep(0.1)

        # Verificar si los insultos están en el servidor
        insultos = [i.decode() for i in r.smembers("server_insults")]

        if "idiota" in insultos and "payaso" in insultos:
            # Si los insultos están en el servidor, la frase debe estar filtrada
            self.assertEqual(frase_filtrada, "Eres un **** y un ****", "La frase no fue filtrada correctamente")
        else:
            # Si los insultos no están en el servidor, la frase debe permanecer igual
            self.assertEqual(frase_filtrada, frase, "La frase fue filtrada incorrectamente")

if __name__ == "__main__":
    unittest.main()