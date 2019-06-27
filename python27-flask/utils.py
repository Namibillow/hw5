# -*- coding: utf-8 -*-
from collections import defaultdict

import itertools


def create_pairs(stations):
    tot = []

    def pairwise(s):
        # "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = itertools.tee(s)
        next(b, None)
        return itertools.izip(a, b)

    for s in stations:
        temp = []
        for name in s['Stations']:
            temp.append((s['Name'], name))
            # (src, next line)
        tot += list(pairwise(temp))
    return tot


def build_graph(connected, outtages=None):
    graph = Graph()

    for pairs in connected:
        from_station, to_station = pairs
        graph.addEdge(from_station, to_station)

    if outtages:
        for blocked in outtages:
            graph.removeEdge(blocked['From'], blocked['To'])
    return graph


def build_weighted_graph(connected, outtages=None, time):
    graph = Graph()

    for shcedule in time['Schedules']
        station = shcedule['Station']
        line = shcedule['LineId']['Line']['Name']
        curr_pos = None
        for ind, neigh in enumerate(shcedule['LineId']['Line']['Stations']):
            if neigh == station:
                curr_pos = ind
                break
        direction = shcedule['LineId']['Line']['Direction']
        line_stations = shcedule['LineId']['Line']['Stations']
        neighbor = None
        if direction == 1:
            neighbor = line_stations[ind + 1] if ind < len(line_stations) - 1 else None
        else:
            neighbor = line_station[ind - 1] if ind > 0 else None

        if neighbor:
            connection = [(line, station), (line, neighbor), direction, weight]

            schedule['Rows']


def process_timeJson(time, graph):
    #
    for schedule in time['Schedules']:
        vertex = graph.verticies[schedule['Station']]

        time_schedule = [str(h['Hour']) + str(m) for h in schedule['Rows'] for m in h['Mins']]
        print(schedule['Station'])
        vertex.addTimeSchedule(schedule['Station']['Direction'], time_schedule)


class Vertex:
    def __init__(self, line, station):
        self.station = station  # .encode('utf-8')
        self.neighbors = []
        self.up_neighbors = []
        self.down_neighbors = []
        self.lines = [line]
        self.cost = float('inf')
        self.dist = 0
        self.time_up = []
        self.time_down = []

    def addNeighbor(self, neigh):
        self.neighbors.append(neigh)

    def addLine(self, line):
        self.lines.append(line)

    def __str__(self):
        return str(self.station.encode('utf-8')) + ' is connected to ' + str([n.station for n in self.neighbors])

    def getConnections(self):
        return self.neighbors

    def getStationInfo(self):
        return self.station, self.lines

    def addTimeSchedule(self, sign, time):
        pass
        # if sign == 1:
        #     self.time_up.append()
        # else:
        #     self.time_down.append()


class Graph:
    def __init__(self):
        self.verticies = {}
        self.numVerticies = 0

    def addVertex(self, line, station):
        """
        """
        if station in self.verticies:
            self.verticies[station].addLine(line)
        else:
            self.numVerticies += 1
            self.verticies[station] = Vertex(line, station)

    def addWeightedEdge(self, from_info, to_info, weight, line):

    def addEdge(self, from_info, to_info):
        """
        input:
            from_info - tuple(line, station)
            to_info - tuple(line, station)
        """
        self.addVertex(*from_info)
        self.addVertex(*to_info)

        self.verticies[from_info[1]].addNeighbor(self.verticies[to_info[1]])
        self.verticies[to_info[1]].addNeighbor(self.verticies[from_info[1]])

    def removeEdge(self, from_station, to_station):
        to_vertex = self.verticies[to_station]
        from_vertex = self.verticies[from_station]

        try:
            index = self.verticies[from_station].neighbors.index(to_vertex)
        except:
            print(from_station, " is not connected to ", to_station)
            return
        print("removing")
        self.verticies[from_station].neighbors.pop(index)
