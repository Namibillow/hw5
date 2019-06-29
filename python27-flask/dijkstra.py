# def print_dfs(graph, start_station, goal_station):
#     station_to_num = {station: ind for ind, station in enumerate(graph.verticies.values())}

#     start = graph.verticies[start_station]
#     goal = graph.verticies[goal_station]

#     numV = graph.numVerticies
#     is_visited = [False] * numV

#     path = []

#     dfs(graph, start, goal, path, station_to_num, is_visited)


# def dfs(graph, s, d, path, station_to_num, is_visited):
#     path.append(s)
#     is_visited[station_to_num[s]] = True

#     if s == d:
#         # print(path)
#         for p in path:
#             print(p.station.encode('utf-8'))
#         print()
#         print()
#     else:
#         for neighbor in s.neighbors:
#             if not is_visited[station_to_num[neighbor[0]]]:
#                 dfs(graph, neighbor[0], d, path, station_to_num, is_visited)

#     path.pop()
#     is_visited[station_to_num[s]] = False


def dijkstra(start, goal, graph, schedules, outtages, input_time):
    station_to_num = {station: ind for ind, station in enumerate(graph.verticies.values())}

    total_time = [float('inf')] * graph.numVerticies
    previous = [None] * graph.numVerticies

    total_time[station_to_num[start]] = 0

    verticies = graph.verticies.values().copy()

    while verticies:
        current_vertex = min(verticies, key=lambda v: total_time[station_to_num[v]])

        if total_time[current_vertex] == float('inf'):
            break

        verticies.remove(current_vertex)

        for neigh_info in current_vertex.neighbors:
            # neigh, line, direction
            curr_cost = get_time(schedules, input_time, *neigh_info)
            cost = total_time[station_to_num[current_vertex]] + curr_cost

            if cost < total_time[station_to_num[neighbor]]:
                total_time[station_to_num[neighbor]] = cost
                previous[station_to_num[neighbor]] = current_vertex

        verticies.remove(current_vertex)


def get_time(schedules, input_time, neigh, line, direction):
    current_hour, current_min = input_time
    # Same hour  than subtract min
    # next hour than convert hours to min and return min
    # if its the last train then return somtehing
    if current_hour in schedules[neigh.station][line][direction].keys():
        possible_min = [i for i in schedules[neigh.station][line][direction][current_hour] if i > current_time]
        if possible_min:
            next_min = min(possible_min)
        else:

        return next_min, current_hour
    elif current_hour + 1 in schedules[neigh.station][line][direction].keys():
        possible_min = [i for i in schedules[neigh.station][line][direction][current_hour] if i > current_time]
