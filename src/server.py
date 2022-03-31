# Sources:
# https://stackoverflow.com/questions/53621682/multi-threaded-xml-rpc-python3-7-1

from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
import time
import breadth_first_search
import config
import test


class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


def compute_shortest_wikipedia_path(start_page, end_page):
    start_time = time.time()
    shortest_path = test.find_shortest_path(start_page, end_page)
    end_time = time.time()
    delta_time = round(end_time - start_time, 2)
    return (shortest_path, delta_time)


def create_and_run_server():
    try:
        print("Starting the server. Press CTRL + C to exit.")
        with SimpleThreadedXMLRPCServer((config.HOST, config.PORT)) as server:
            server.register_introspection_functions()
            server.register_function(compute_shortest_wikipedia_path)
            server.serve_forever()
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print(f"Server crashed: {e}")


if __name__ == "__main__":
    create_and_run_server()
