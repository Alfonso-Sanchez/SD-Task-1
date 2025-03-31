import Pyro4
import random
import time

@Pyro4.expose
class Broadcaster:
    def __init__(self, servers):
        self.servers = servers

    def start_broadcasting(self):
        insults = ["Mi melon melon sabe mejor!", "El capullo de mi ex", "No hay nada más gilipollas que no leer el manual", "Tienes una cara fea"]
        while True:
            try:
                # Seleccionar un servidor aleatoriamente
                server = random.choice(self.servers)
                insult = random.choice(insults)
                result = server.saveInsult(insult)
                print(f"Insulto '{insult}' enviado al servidor con resultado: {result}")
            except Exception as e:
                print(f"Error al enviar insulto: {e}")

def main():
    # Conectarse a los servidores de insultos
    try:
        server1 = Pyro4.Proxy("PYRONAME:example.insultserver1")
        server2 = Pyro4.Proxy("PYRONAME:example.insultserver2")
        server3 = Pyro4.Proxy("PYRONAME:example.insultserver3")
        print("Conectado a los servidores de insultos")  # Mensaje de depuración
    except Exception as e:
        print(f"Error al conectar con los servidores: {e}")  # Mensaje de depuración
        return
    
    # Crear el broadcaster y comenzar a enviar insultos
    broadcaster = Broadcaster([server1, server2, server3])
    
    try:
        broadcaster.start_broadcasting()
    except KeyboardInterrupt:
        print("Interrupción del teclado detectada. Mostrando todas las frases guardadas:")
        try:
            for server in [server1, server2, server3]:
                sentences = server.getSentences()
                print(f"Frases guardadas en el servidor {server._pyroUri}:")
                for sentence in sentences:
                    print(sentence)
        except Exception as e:
            print(f"Error al obtener las frases guardadas: {e}")

if __name__ == "__main__":
    main()