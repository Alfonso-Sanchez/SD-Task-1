import unittest
import pika
import time

class TestServer1(unittest.TestCase):
    def setUp(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        # Colas de Servidor 1
        self.queue_solicitudes_insulto = 'insultame1'
        self.queue_respuesta_insulto = 'insultar1'
        self.queue_filtrar = 'filtrar1'
        self.queue_filtradas = 'filtradas1'
        self.queue_insultos = 'insultos1'

        # Declarar colas
        self.channel.queue_declare(queue=self.queue_solicitudes_insulto)
        self.channel.queue_declare(queue=self.queue_respuesta_insulto)
        self.channel.queue_declare(queue=self.queue_filtrar)
        self.channel.queue_declare(queue=self.queue_filtradas)
        self.channel.queue_declare(queue=self.queue_insultos)

        # Lista de insultos
        self.test_insults = {"Tonto", "Gilipollas", "Maricon"}

        # Pre-poblar 'insultos1'
        for insult in self.test_insults:
            self.channel.basic_publish(exchange='', routing_key=self.queue_insultos, body=insult.encode())
        time.sleep(1)

    def test_solicitar_insulto(self):
        # Enviar solicitud a 'insultame1'
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_solicitudes_insulto,
            body=b"Dame un insulto"
        )

        # Consumir respuesta desde 'insultar1'
        response = None
        for method, properties, body in self.channel.consume(self.queue_respuesta_insulto, auto_ack=True, inactivity_timeout=2):
            if method is None:
                break
            response = body.decode()
            break

        self.assertIsNotNone(response, "No se recibió respuesta del Servidor 1")
        self.assertIn(response, self.test_insults, "El insulto recibido no está en la lista esperada (Servidor 1)")

    def test_filtrar_frase_con_insulto(self):
        test_phrase = "Eres un gilipollas en serio"
        self.channel.basic_publish(exchange='', routing_key=self.queue_filtrar, body=test_phrase.encode())

        response = None
        for method, properties, body in self.channel.consume(self.queue_filtradas, auto_ack=True, inactivity_timeout=2):
            if method is None:
                break
            response = body.decode()
            break

        self.assertIsNotNone(response, "No se recibió respuesta filtrada del Servidor 1")
        self.assertEqual(response, "Eres un CENSORED en serio", "El insulto no fue censurado correctamente (Servidor 1)")

    def test_filtrar_frase_sin_insulto(self):
        test_phrase = "Eres muy amable"
        self.channel.basic_publish(exchange='', routing_key=self.queue_filtrar, body=test_phrase.encode())

        response = None
        for method, properties, body in self.channel.consume(self.queue_filtradas, auto_ack=True, inactivity_timeout=2):
            if method is None:
                break
            response = body.decode()
            break

        self.assertIsNotNone(response, "No se recibió respuesta filtrada del Servidor 1")
        self.assertEqual(response, "Eres muy amable", "La frase fue modificada cuando no debía (Servidor 1)")

    def tearDown(self):
        self.channel.queue_purge(self.queue_insultos)
        self.channel.queue_purge(self.queue_solicitudes_insulto)
        self.channel.queue_purge(self.queue_respuesta_insulto)
        self.channel.queue_purge(self.queue_filtrar)
        self.channel.queue_purge(self.queue_filtradas)
        self.connection.close()

class TestServer2(unittest.TestCase):
    def setUp(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        # Colas de Servidor 2
        self.queue_solicitudes_insulto = 'insultame2'
        self.queue_respuesta_insulto = 'insultar2'  # Corregido respecto a server2.py original
        self.queue_filtrar = 'filtrar2'
        self.queue_filtradas = 'filtradas2'
        self.queue_insultos = 'insultos2'

        # Declarar colas
        self.channel.queue_declare(queue=self.queue_solicitudes_insulto)
        self.channel.queue_declare(queue=self.queue_respuesta_insulto)
        self.channel.queue_declare(queue=self.queue_filtrar)
        self.channel.queue_declare(queue=self.queue_filtradas)
        self.channel.queue_declare(queue=self.queue_insultos)

        # Lista de insultos
        self.test_insults = {"Tonto", "Gilipollas", "Maricon"}

        # Pre-poblar 'insultos2'
        for insult in self.test_insults:
            self.channel.basic_publish(exchange='', routing_key=self.queue_insultos, body=insult.encode())
        time.sleep(1)

    def test_solicitar_insulto(self):
        # Enviar solicitud a 'insultame2'
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_solicitudes_insulto,
            body=b"Dame un insulto"
        )

        # Consumir respuesta desde 'insultar2'
        response = None
        for method, properties, body in self.channel.consume(self.queue_respuesta_insulto, auto_ack=True, inactivity_timeout=2):
            if method is None:
                break
            response = body.decode()
            break

        self.assertIsNotNone(response, "No se recibió respuesta del Servidor 2")
        self.assertIn(response, self.test_insults, "El insulto recibido no está en la lista esperada (Servidor 2)")

    def test_filtrar_frase_con_insulto(self):
        test_phrase = "Eres un gilipollas en serio"
        self.channel.basic_publish(exchange='', routing_key=self.queue_filtrar, body=test_phrase.encode())

        response = None
        for method, properties, body in self.channel.consume(self.queue_filtradas, auto_ack=True, inactivity_timeout=2):
            if method is None:
                break
            response = body.decode()
            break

        self.assertIsNotNone(response, "No se recibió respuesta filtrada del Servidor 2")
        self.assertEqual(response, "Eres un CENSORED en serio", "El insulto no fue censurado correctamente (Servidor 2)")

    def test_filtrar_frase_sin_insulto(self):
        test_phrase = "Eres muy amable"
        self.channel.basic_publish(exchange='', routing_key=self.queue_filtrar, body=test_phrase.encode())

        response = None
        for method, properties, body in self.channel.consume(self.queue_filtradas, auto_ack=True, inactivity_timeout=2):
            if method is None:
                break
            response = body.decode()
            break

        self.assertIsNotNone(response, "No se recibió respuesta filtrada del Servidor 2")
        self.assertEqual(response, "Eres muy amable", "La frase fue modificada cuando no debía (Servidor 2)")

    def tearDown(self):
        self.channel.queue_purge(self.queue_insultos)
        self.channel.queue_purge(self.queue_solicitudes_insulto)
        self.channel.queue_purge(self.queue_respuesta_insulto)
        self.channel.queue_purge(self.queue_filtrar)
        self.channel.queue_purge(self.queue_filtradas)
        self.connection.close()

    

class TestServer3(unittest.TestCase):
    def setUp(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        # Colas de Servidor 3
        self.queue_solicitudes_insulto = 'insultame3'
        self.queue_respuesta_insulto = 'insultar3'
        self.queue_filtrar = 'filtrar3'
        self.queue_filtradas = 'filtradas3'
        self.queue_insultos = 'insultos3'

        # Declarar colas
        self.channel.queue_declare(queue=self.queue_solicitudes_insulto)
        self.channel.queue_declare(queue=self.queue_respuesta_insulto)
        self.channel.queue_declare(queue=self.queue_filtrar)
        self.channel.queue_declare(queue=self.queue_filtradas)
        self.channel.queue_declare(queue=self.queue_insultos)

        # Lista de insultos
        self.test_insults = {"Tonto", "Gilipollas", "Maricon"}

        # Pre-poblar 'insultos3'
        for insult in self.test_insults:
            self.channel.basic_publish(exchange='', routing_key=self.queue_insultos, body=insult.encode())
        time.sleep(1)

    def test_solicitar_insulto(self):
        # Enviar solicitud a 'insultame3'
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_solicitudes_insulto,
            body=b"Dame un insulto"
        )

        # Consumir respuesta desde 'insultar3'
        response = None
        for method, properties, body in self.channel.consume(self.queue_respuesta_insulto, auto_ack=True, inactivity_timeout=2):
            if method is None:
                break
            response = body.decode()
            break

        self.assertIsNotNone(response, "No se recibió respuesta del Servidor 3")
        self.assertIn(response, self.test_insults, "El insulto recibido no está en la lista esperada (Servidor 3)")

    def test_filtrar_frase_con_insulto(self):
        test_phrase = "Eres un gilipollas en serio"
        self.channel.basic_publish(exchange='', routing_key=self.queue_filtrar, body=test_phrase.encode())

        response = None
        for method, properties, body in self.channel.consume(self.queue_filtradas, auto_ack=True, inactivity_timeout=2):
            if method is None:
                break
            response = body.decode()
            break

        self.assertIsNotNone(response, "No se recibió respuesta filtrada del Servidor 3")
        self.assertEqual(response, "Eres un CENSORED en serio", "El insulto no fue censurado correctamente (Servidor 3)")

    def test_filtrar_frase_sin_insulto(self):
        test_phrase = "Eres muy amable"
        self.channel.basic_publish(exchange='', routing_key=self.queue_filtrar, body=test_phrase.encode())

        response = None
        for method, properties, body in self.channel.consume(self.queue_filtradas, auto_ack=True, inactivity_timeout=2):
            if method is None:
                break
            response = body.decode()
            break

        self.assertIsNotNone(response, "No se recibió respuesta filtrada del Servidor 3")
        self.assertEqual(response, "Eres muy amable", "La frase fue modificada cuando no debía (Servidor 3)")

    def tearDown(self):
        self.channel.queue_purge(self.queue_insultos)
        self.channel.queue_purge(self.queue_solicitudes_insulto)
        self.channel.queue_purge(self.queue_respuesta_insulto)
        self.channel.queue_purge(self.queue_filtrar)
        self.channel.queue_purge(self.queue_filtradas)
        self.connection.close()

if __name__ == '__main__':
    unittest.main()