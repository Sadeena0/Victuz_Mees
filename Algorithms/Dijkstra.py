from heapq import heappush, heappop

def dijkstra(graph, queue, distances, visited, previous, end):
    if not queue:
        return None

    current_distance, current_node = heappop(queue)  # Get closest node (top of minheap)

    if current_node == end:
        path = []
        while current_node is not None:
            path.append(current_node)  # Add current node to path
            current_node = previous[current_node]  # Set current node to previous node
        return path[::-1], current_distance  # Returned reversed path (So it's Start to End), and the distance to here

    if current_node in visited:  # If current node has already been visited, continue to next node
        return dijkstra(graph, queue, distances, visited, previous, end)

    visited.add(current_node)

    # *rest used to iterate over potential values other than neighbor and weight
    # this is used as some nodes might have an accessibility flag
    for neighbor, weight, *rest in graph[current_node]:
        new_distance = current_distance + weight  # Distance is current distance + distance from old to current node
        if new_distance < distances[neighbor]:
            distances[neighbor] = new_distance
            previous[neighbor] = current_node
            heappush(queue, (new_distance, neighbor))  # Add new node to heap

    return dijkstra(graph, queue, distances, visited, previous, end)


def shortest_route(graph, start, end, wheelchair=False, emergency=False):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    queue = [(0, start)]

    for node in graph:
        for connection in graph[node]:
            if wheelchair:
                if emergency:
                    if len(connection) == 3 and connection[2] == 'Lift':
                        graph[node].remove(connection)
                else:
                    if len(connection) == 3 and connection[2] == 'Stairs':
                        graph[node].remove(connection)
            else:
                if len(connection) == 3 and connection[2] == 'Lift':
                    graph[node].remove(connection)

    result = dijkstra(graph, queue, distances, set(), previous, end)
    if result is None:
        return None, float('inf')
    else:
        path, distance = result
        return path, distance

