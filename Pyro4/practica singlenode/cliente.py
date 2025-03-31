import Pyro4
import random
import time

@Pyro4.expose
class Broadcaster:
    def __init__(self, server):
        self.server = server

    def start_broadcasting(self):
        insults = ["Mi melon melon sabe mejor!", "El capullo de mi ex", "No hay nada mas gilipollas que no leer el manual", "Tienes una cara fea"]
        while True:
            try:
                insult = random.choice(insults)
                result = self.server.saveInsult(insult)
                print(f"Insulto {insult} enviado con resultado: {result}")  # Añadir un print para verificar el envío
            except Exception as e:
                print(f"Error al enviar insulto: {e}")  # Mensaje de depuración

def main():
    # Conectarse al servidor de insultos
    try:
        server = Pyro4.Proxy("PYRONAME:example.insultserver")
        print("Conectado al servidor de insultos")  # Mensaje de depuración
    except Exception as e:
        print(f"Error al conectar con el servidor: {e}")  # Mensaje de depuración
        return
    
    # Crear el broadcaster y comenzar a recibir insultos
    broadcaster = Broadcaster(server)
    
    try:
        broadcaster.start_broadcasting()
    except KeyboardInterrupt:
        print("Interrupción del teclado detectada. Mostrando todas las frases guardadas:")
        try:
            sentences = server.getSentences()
            for sentence in sentences:
                print(sentence)
        except Exception as e:
            print(f"Error al obtener las frases guardadas: {e}")

if __name__ == "__main__":
    main()