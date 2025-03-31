import unittest
import Pyro4

class TestInsultFilter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Conectar al servidor Pyro4 que ya está corriendo
        cls.proxy = Pyro4.Proxy("PYRONAME:example.insultserver")
        # No iniciamos el servidor aquí, asumimos que ya está activo

    def setUp(self):
        # Limpiar la lista de sentencias antes de cada prueba
        # Usamos el proxy para obtener el estado inicial y limpiarlo
        sentences = self.proxy.getSentences()
        if sentences:  # Si hay sentencias, las limpiamos manualmente
            for _ in range(len(sentences)):
                self.proxy.getSentences()  # Esto no limpia directamente, necesitamos un método en el servidor
            # Nota: Idealmente, el servidor debería tener un método como clearSentences()
            # Por ahora, asumimos que puedes limpiar manualmente o ajustar el servidor
            # Si no hay método para limpiar, reinicia el servidor antes de las pruebas

    def test_filter_no_insults(self):
        # Probar un texto sin insultos
        self.proxy.clearSentences()
        result = self.proxy.saveInsult("Hola mundo")
        self.assertEqual(result, "Guardado")
        sentences = self.proxy.getSentences()
        self.assertEqual(sentences, ["Hola mundo"])

    def test_filter_with_insults(self):
        # Probar un texto con insultos
        self.proxy.clearSentences()
        result = self.proxy.saveInsult("Eres un capullo y gilipollas")
        self.assertEqual(result, "Guardado")
        sentences = self.proxy.getSentences()
        self.assertEqual(sentences, ["Eres un CENSORED y CENSORED"])

    def test_duplicate_sentence(self):
        # Probar un texto duplicado
        self.proxy.clearSentences()
        self.proxy.saveInsult("Hola capullo")
        result = self.proxy.saveInsult("Hola capullo")
        self.assertEqual(result, "No guardado")
        sentences = self.proxy.getSentences()
        self.assertEqual(len(sentences), 1)
        self.assertEqual(sentences, ["Hola CENSORED"])

    def test_get_sentences(self):
        # Probar recuperación de múltiples textos
        self.proxy.clearSentences()
        self.proxy.saveInsult("Texto fea")
        self.proxy.saveInsult("Otro gilipollas")
        sentences = self.proxy.getSentences()
        self.assertEqual(len(sentences), 2)
        self.assertIn("Texto CENSORED", sentences)
        self.assertIn("Otro CENSORED", sentences)

if __name__ == "__main__":
    unittest.main()