import unittest
import Pyro4

class TestInsultFilter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Conectar a los servidores Pyro4 que ya están corriendo
        cls.proxies = {
            "server1": Pyro4.Proxy("PYRONAME:example.insultserver1"),
            "server2": Pyro4.Proxy("PYRONAME:example.insultserver2")
        }
        # Asumimos que ambos servidores ya están activos

    def setUp(self):
        # Limpiar la lista de sentencias antes de cada prueba para cada servidor
        for server_name, proxy in self.proxies.items():
            proxy.clearSentences()  # Necesitamos este método en los servidores

    # Pruebas para Server1
    def test_server1_no_insults(self):
        proxy = self.proxies["server1"]
        proxy.clearSentences()
        result = proxy.saveInsult("Hola mundo")
        self.assertEqual(result, "Guardado")
        sentences = proxy.getSentences()
        self.assertEqual(sentences, ["Hola mundo"])

    def test_server1_with_insults(self):
        proxy = self.proxies["server1"]
        proxy.clearSentences()
        result = proxy.saveInsult("Eres un capullo y gilipollas")
        self.assertEqual(result, "Guardado")
        sentences = proxy.getSentences()
        self.assertEqual(sentences, ["Eres un CENSORED y CENSORED"])

    def test_server1_duplicate_sentence(self):
        proxy = self.proxies["server1"]
        proxy.clearSentences()
        proxy.saveInsult("Hola capullo")
        result = proxy.saveInsult("Hola capullo")
        self.assertEqual(result, "No guardado")
        sentences = proxy.getSentences()
        self.assertEqual(len(sentences), 1)
        self.assertEqual(sentences, ["Hola CENSORED"])

    def test_server1_get_sentences(self):
        proxy = self.proxies["server1"]
        proxy.clearSentences()
        proxy.saveInsult("Texto fea")
        proxy.saveInsult("Otro gilipollas")
        sentences = proxy.getSentences()
        self.assertEqual(len(sentences), 2)
        self.assertIn("Texto CENSORED", sentences)
        self.assertIn("Otro CENSORED", sentences)

    # Pruebas para Server2
    def test_server2_no_insults(self):
        proxy = self.proxies["server2"]
        proxy.clearSentences()
        result = proxy.saveInsult("Hola mundo")
        self.assertEqual(result, "Guardado")
        sentences = proxy.getSentences()
        self.assertEqual(sentences, ["Hola mundo"])

    def test_server2_with_insults(self):
        proxy = self.proxies["server2"]
        proxy.clearSentences()
        result = proxy.saveInsult("Eres un capullo y gilipollas")
        self.assertEqual(result, "Guardado")
        sentences = proxy.getSentences()
        self.assertEqual(sentences, ["Eres un CENSORED y CENSORED"])

    def test_server2_duplicate_sentence(self):
        proxy = self.proxies["server2"]
        proxy.clearSentences()
        proxy.saveInsult("Hola capullo")
        result = proxy.saveInsult("Hola capullo")
        self.assertEqual(result, "No guardado")
        sentences = proxy.getSentences()
        self.assertEqual(len(sentences), 1)
        self.assertEqual(sentences, ["Hola CENSORED"])

    def test_server2_get_sentences(self):
        proxy = self.proxies["server2"]
        proxy.clearSentences()
        proxy.saveInsult("Texto fea")
        proxy.saveInsult("Otro gilipollas")
        sentences = proxy.getSentences()
        self.assertEqual(len(sentences), 2)
        self.assertIn("Texto CENSORED", sentences)
        self.assertIn("Otro CENSORED", sentences)

if __name__ == "__main__":
    unittest.main()