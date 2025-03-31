import Pyro4
import random
import time

@Pyro4.expose
class Broadcaster:
    def __init__(self, server_uris):
        self.server_uris = server_uris

    def get_servers(self):
        servers = []
        for uri in self.server_uris:
            try:
                servers.append(Pyro4.Proxy(f"PYRONAME:{uri}"))
            except Exception as e:
                print(f"[Cliente] Error conectando con {uri}: {e}")
        return servers

    def start_broadcasting(self):
        insults = [
            "Mi melon melon sabe mejor!",
            "El capullo de mi ex",
            "No hay nada más gilipollas que no leer el manual",
            "Tienes una cara fea"
        ]
        while True:
            self.server_uris = load_server_uris()
            servers = self.get_servers()

            if not servers:
                print("[Cliente] No hay servidores disponibles.")
                time.sleep(2)
                continue

            server = random.choice(servers)
            insult = random.choice(insults)

            try:
                result = server.saveInsult(insult)
                print(f"[Cliente] Insulto '{insult}' enviado -> Resultado: {result}")
            except Exception as e:
                print(f"[Cliente] Error al enviar insulto: {e}")
            time.sleep(0.1)

def load_server_uris():
    try:
        with open("servers.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def main():
    uris = load_server_uris()
    broadcaster = Broadcaster(uris)

    try:
        broadcaster.start_broadcasting()
    except KeyboardInterrupt:
        print("\n[Cliente] Interrupción detectada. Obteniendo frases guardadas...")
        for uri in uris:
            try:
                server = Pyro4.Proxy(f"PYRONAME:{uri}")
                print(f"\nFrases del servidor {uri}:")
                for s in server.getSentences():
                    print(" -", s)
            except Exception as e:
                print(f"  Error con {uri}: {e}")

if __name__ == "__main__":
    main()
