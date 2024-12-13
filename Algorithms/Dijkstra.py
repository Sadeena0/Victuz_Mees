from heapq import heappush, heappop

def dijkstra(graph, queue, distances, visited, previous, end):
    if not queue:
        return None

    current_distance, current_node = heappop(queue) # Get closest node (top of minheap)

    if current_node == end:
        path = []
        while current_node is not None:
            path.append(current_node) # Add current node to path
            current_node = previous[current_node] # Set current node to previous node
        return path[::-1] # Returned reversed path (So it's Start to End)

    if current_node in visited: # If current node has already been visited, continue to next node
        return dijkstra(graph, queue, distances, visited, previous, end)

    visited.add(current_node)

    for neighbor, weight in graph[current_node]:
        new_distance = current_distance + weight # Distance is current distance + distance from old to current node
        if new_distance < distances[neighbor]:
            distances[neighbor] = new_distance
            previous[neighbor] = current_node
            heappush(queue, (new_distance, neighbor)) # Add new node to heap

    return dijkstra(graph, queue, distances, visited, previous, end)

def shortest_route(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    queue = [(0, start)]

    return dijkstra(graph, queue, distances, set(), previous, end)