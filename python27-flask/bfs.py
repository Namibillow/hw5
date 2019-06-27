def bfs(graph, start, goal, station_to_num):
    numV = graph.numVerticies
    is_visited = [False] * numV
    dist = [0] * numV
    prev = [None] * numV

    queue = [start]
    is_visited[station_to_num[start.station]] = True

    while queue:
        vertex = queue.pop(0)
        for neighbor in graph.verticies[vertex.station].neighbors:
            if not is_visited[station_to_num[neighbor.station]]:
                id = station_to_num[neighbor.station]
                vertex_id = station_to_num[vertex.station]
                is_visited[id] = True
                dist[id] = dist[vertex_id] + 1
                prev[id] = vertex.station
                queue.append(neighbor)
                if neighbor == goal:
                    return prev, dist
    return None, None


def print_bfs(graph, start_station, goal_station):
    station_to_num = {station: ind for ind, station in enumerate(graph.verticies.keys())}

    start = graph.verticies[start_station]
    goal = graph.verticies[goal_station]

    path, dist = bfs(graph, start, goal, station_to_num)
    if path:
        temp = station_to_num[goal_station]
        shortest_path = [goal_station]
        while path[temp]:
            shortest_path.append(path[temp])
            temp = station_to_num[path[temp]]

        print(dist[station_to_num[goal_station]], " shortest path steps.")

        print("Shortest path is : ")
        for p in shortest_path[::-1]:
            print(p.encode('utf-8'))
        return shortest_path[::-1], dist[station_to_num[goal_station]]

    else:
        print("Sorry there is no path!")
        return None, None
