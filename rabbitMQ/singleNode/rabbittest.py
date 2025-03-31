import unittest
import pika
import time
import uuid

class TestRabbitMQClientReal(unittest.TestCase):
    def setUp(self):
        # Establecer conexión real con RabbitMQ
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        # Colas de entrada del servidor (definidas en server.py)
        self.queue_solicitudes_insulto = 'solicitudes_insulto'
        self.queue_filtrar = 'filtrar'
        self.queue_filtradas = 'filtradas'

        # Declarar las colas del servidor por si no existen aún
        self.channel.queue_declare(queue=self.queue_solicitudes_insulto)
        self.channel.queue_declare(queue=self.queue_filtrar)
        self.channel.queue_declare(queue=self.queue_filtradas)

        # Cola temporal para respuestas de insultos (como cliente)
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.reply_queue_insultos = result.method.queue

        # Lista de insultos de prueba (reemplaza con tus insultos reales)
        self.test_insults = {"Tonto","Gilipollas","Maricon"}

        # Pre-poblar la cola 'insultos' para simular el broadcaster
        self.channel.queue_declare(queue='insultos')  # Cola de entrada del servidor
        for insult in self.test_insults:
            self.channel.basic_publish(exchange='', routing_key='insultos', body=insult.encode())
        
        # Dar tiempo al servidor para procesar los insultos
        time.sleep(1)

    def test_solicitar_insulto(self):
        """Probar solicitar un insulto al servidor y verificar la respuesta"""
        # Generar un ID único para la solicitud
        correlation_id = str(uuid.uuid4())

        # Enviar solicitud a 'solicitudes_insulto' con cola de respuesta
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_solicitudes_insulto,
            properties=pika.BasicProperties(
                reply_to=self.reply_queue_insultos,
                correlation_id=correlation_id
            ),
            body=b"Dame un insulto"
        )

        # Consumir la respuesta desde la cola temporal
        response = None
        for method, properties, body in self.channel.consume(self.reply_queue_insultos, auto_ack=True, inactivity_timeout=2):
            if properties.correlation_id == correlation_id:
                response = body.decode()
                break

        # Verificar la respuesta
        self.assertIsNotNone(response, "No se recibió respuesta del servidor")
        self.assertIn(response, self.test_insults, "El insulto recibido no está en la lista esperada")

    def test_filtrar_frase_con_insulto(self):
        """Probar enviar una frase con insulto y verificar que se censura"""
        # Enviar una frase con insulto a 'filtrar'
        test_phrase = "Eres un gilipollas en serio"
        self.channel.basic_publish(exchange='', routing_key=self.queue_filtrar, body=test_phrase.encode())

        # Consumir el resultado desde 'filtradas'
        response = None
        for method, properties, body in self.channel.consume(self.queue_filtradas, auto_ack=True, inactivity_timeout=2):
            response = body.decode()
            break

        # Verificar el resultado
        self.assertIsNotNone(response, "No se recibió respuesta filtrada")
        self.assertEqual(response, "Eres un CENSORED en serio", "El insulto no fue censurado correctamente")

    def test_filtrar_frase_sin_insulto(self):
        """Probar enviar una frase sin insulto y verificar que no se censura"""
        # Enviar una frase sin insulto a 'filtrar'
        test_phrase = "Eres muy amable"
        self.channel.basic_publish(exchange='', routing_key=self.queue_filtrar, body=test_phrase.encode())

        # Consumir el resultado desde 'filtradas'
        response = None
        for method, properties, body in self.channel.consume(self.queue_filtradas, auto_ack=True, inactivity_timeout=2):
            response = body.decode()
            break

        # Verificar el resultado
        self.assertIsNotNone(response, "No se recibió respuesta filtrada")
        self.assertEqual(response, "Eres muy amable", "La frase fue modificada cuando no debía")

    def tearDown(self):
        # Limpiar: purgar colas y cerrar conexión
        self.channel.queue_purge('insultos')
        self.channel.queue_purge(self.queue_solicitudes_insulto)
        self.channel.queue_purge(self.queue_filtrar)
        self.channel.queue_purge(self.queue_filtradas)
        self.connection.close()

if __name__ == '__main__':
    unittest.main()