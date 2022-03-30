from xmlrpc.client import ServerProxy, Error
import config



if __name__ == "__main__":
    s = ServerProxy(f"http://{config.HOST}:{config.PORT}")
    s.compute_shortest_wikipedia_path()
    print()
