from xmlrpc.client import ServerProxy
import config


def menu():
    print("Available options:")
    print("1) Find the shortest path between 2 Wikipedia articles")
    print("0) Exit")

    try:
        return int(input("Your choice: "))
    except ValueError:
        return -1


def get_shortest_path(rpc):
    start_page = input("Start page: ")
    end_page = input("End page: ")

    shortest_path, delta_time = rpc.compute_shortest_wikipedia_path(start_page, end_page)
    shortest_path_length = len(shortest_path)
    
    if (shortest_path_length != 0):
        print(f"Path found with {shortest_path_length - 1} degree(s) of separation in {delta_time} seconds:")
        print(shortest_path)
    else:
        print("Could not find a path between the pages or the server failed to process your request.")


def main():
    try:
        choice = -1
        rpc = ServerProxy(f"http://{config.HOST}:{config.PORT}")

        while True:
            choice = menu()

            match choice:
                case 0:
                    break
                case 1:
                    get_shortest_path(rpc)
                case _:
                    print("Invalid option. Try again.")
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
    
    print("Exiting...")
        

if __name__ == "__main__":
    main()
