# Sources:
#
# Multithreading:
# https://docs.python.org/3/library/concurrent.futures.html
# https://medium.com/daily-programming-tips/how-to-parallelize-for-loops-in-python-and-work-with-shared-dictionaries-76a5560254cd
# https://www.digitalocean.com/community/tutorials/how-to-use-threadpoolexecutor-in-python-3
#
# Breadth-first search:
# https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/
# https://www.educative.io/edpresso/how-to-implement-a-breadth-first-search-in-python
# https://github.com/stong1108/WikiRacer/blob/master/wikiracer.py

import concurrent.futures
import multiprocessing
import wikipedia

# returns a non-empty array if a shortest path has been found
def get_page_links_concurrently(visited, current_page, end_page, current_path, queue):
    # thread amount defaults to the number of processors on the machine, multiplied by 5
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        # find the links of the page if the page has not already been visited
        for page in visited[current_page]:
            if page not in visited:
                futures.append(
                    executor.submit(wikipedia.get_page_links, page)
                )

        # process the results
        for future in concurrent.futures.as_completed(futures):
            page_links, page = future.result()

            try:
                # shortest path found - return it
                if end_page in page_links:
                    return current_path + [page, end_page]

                # add the page to the queue and mark it as visited
                queue.append((page, current_path + [page]))
                visited[page] = page_links
            except:
                print(f"Failed to complete the future for '{page}'.")

    return []


def find_shortest_path(start_page, end_page):
    # start and end are the same: 0 degrees of separation
    if (start_page == end_page):
        return [start_page]

    # the variables created using Manager() are thread-safe and have a mutex lock
    manager = multiprocessing.Manager()

    # dictionary to hold already visited pages so that they are not traversed again
    # it also holds the neighbours of the breadth-first search node
    visited = manager.dict()

    queue = manager.list()

    # mark the start page as visited
    visited[start_page], _ = wikipedia.get_page_links(start_page)

    # check if the start page contains a link to the end page:
    # 1 degree of seperation
    if end_page in visited[start_page]:
        return [start_page, end_page]

    # enqueue the start page
    queue.append((start_page, [start_page]))

    while queue:
        page, path = queue.pop(0)
        print(f"Traversing page '{page}', the degree is {len(path) - 1}")

        shortest_path = get_page_links_concurrently(visited, page, end_page, path, queue)

        # non-empty => shortest path found
        if len(shortest_path) != 0:
            return shortest_path

    # could not find the shortest path
    return []
