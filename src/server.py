# Sources:
# https://stackoverflow.com/questions/53621682/multi-threaded-xml-rpc-python3-7-1

from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
import time
import breadth_first_search
import wikipedia
import config


class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


def compute_shortest_wikipedia_path(start_page, end_page):
    # find the pages by the provided search term
    start_page = wikipedia.search(start_page)
    end_page = wikipedia.search(end_page)

    if (start_page and end_page):
        start_time = time.time()
        shortest_path = breadth_first_search.find_shortest_path(start_page, end_page)
        end_time = time.time()
        delta_time = round(end_time - start_time, 2)
        return (shortest_path, delta_time, None)

    return ([], 0, "invalid start page and/or end page")


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
