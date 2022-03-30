from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
import concurrent.futures
import config


class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


def compute_shortest_wikipedia_path():
    print()


def create_and_run_server():
    try:
        print("Starting the server. Press CTRL + C to exit.")
        with SimpleThreadedXMLRPCServer((config.HOST, config.PORT)) as server:
            server.register_introspection_functions()
            server.register_function(compute_shortest_wikipedia_path)
            server.serve_forever()
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    create_and_run_server()
