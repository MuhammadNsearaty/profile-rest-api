from search_engine.trip_planner.trip_classes.Day import Day
from search_engine.trip_planner.trip_classes.Item import Item
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN
from sklearn_extra.cluster import KMedoids
import numpy as np
import pickle
from search_engine.trip_planner.trip_classes.Trip import Trip
from icecream import ic

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import requests
import json

from trip_planning.Plan_itinerary import plot_path, colors

API_KEY = '5b3ce3597851110001cf6248bd5e3be150bc410ebc5d8527d2521161'
url = 'https://api.openrouteservice.org/v2/matrix/driving-car'

from haversine import haversine


def get_distance(item1: Item, item2: Item):
    cord1 = item1.coordinate
    cord2 = item2.coordinate
    tuple1 = (cord1['lat'], cord1['lon'])
    tuple2 = (cord2['lat'], cord2['lon'])
    return haversine(tuple1, tuple2)


def create_data_model(p_items):
    coordinates = []

    """Stores the data for the problem."""
    data = {}

    for i in range(len(p_items)):
        coordinates.append([p_items[i].coordinate['lon'], p_items[i].coordinate['lat']])
    body = {'locations': coordinates, 'metrics': ['distance'], 'units': 'km'}
    header = {'Authorization': API_KEY}
    try:
        response = requests.post(url=url, json=body, headers=header)
        if response.status_code == requests.codes.ok:
            data['distance_matrix'] = json.loads(response.text)['distances']
    except ValueError as err:
        print('distance matrix err: ', err)

    data['num_vehicles'] = 1
    data['depot'] = 0
    return data


def get_routes(solution, routing, manager):
    """Get vehicle routes from a solution and store them in an array."""
    # Get vehicle routes and store them in a two dimensional array whose
    # i,j entry is the jth location visited by vehicle i along its route.
    routes = []
    for route_nbr in range(routing.vehicles()):
        index = routing.Start(route_nbr)
        route = [manager.IndexToNode(index)]
        while not routing.IsEnd(index):
            index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))
        routes.append(route)
    return routes


def plan_itinerary_LP(p_items):
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model(p_items)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        # print_solution(manager, routing, solution
        path = get_routes(solution, routing, manager)
        return [p_items[i] for i in path[0]]


class ClusterPlanner:
    def __init__(self, items, n_poi):
        self.n_poi = n_poi
        self.n_clusters = len(items) // n_poi
        self.food_types = ['restaurants', 'fast_food', 'food']
        self.items = [item for item in items if item.item_type not in self.food_types]
        self.restaurants = [item for item in items if item.item_type in self.food_types]
        print('items', len(self.items))
        self.data = pd.DataFrame({
            'index': [i for i in range(len(self.items))],
            'lat': [item.coordinate['lat'] for item in self.items],
            'lon': [item.coordinate['lon'] for item in self.items],
            'type': [item.item_type for item in self.items]})

    def cluster_data(self):
        # clusterer = DBSCAN(eps=0.1, min_samples=self.n_poi, metric='haversine')
        clusterer = KMedoids(n_clusters=self.n_poi, metric='haversine')
        self.data['label'] = clusterer.fit_predict(self.data[['lat', 'lon']].values)

    # insert restaurant in the day at index
    def insert_restaurant(self, poi, idx, day):
        distances = []
        if self.restaurants:
            for rest in self.restaurants:
                distances.append(get_distance(poi, rest))
            index = distances.index(min(distances))
            day.insert_item(self.restaurants[index], idx)
            self.restaurants = [self.restaurants[l] for l in range(len(self.restaurants)) if l != index]

    # plan every cluster in city then return the full plan
    def plan_days(self, i, days):

        if i == self.n_clusters:
            return days

        places = self.data[self.data['label'] == i]
        p_items = [self.items[int(p['index'])] for _, p in places.iterrows()]
        # plan if items > 3
        if len(p_items) > 3:
            itinerary = plan_itinerary_LP(p_items)[:-1]
            days.append(Day(i, itinerary))

        elif p_items:
            days.append(Day(i, p_items))

        for k in range(0, len(p_items)):
            if 'hotel' == p_items[k].item_type and k != 0:
                days[i].swap_items(0, k)

        return self.plan_days(i + 1, days)


# reorganize plan
def plan_itinerary_schedule_clusters(items: dict):
    trip = Trip(days=[])

    cities = list(items.values())
    pois = []
    for city in cities:
        pois.extend(city)
    clusterer = ClusterPlanner(pois, 5)
    clusterer.cluster_data()
    plan_days = clusterer.plan_days(0, [])
    scheduled_days = []
    # for day in plan_days:
    # scheduled_days = [Day(l,day.tolist()) for l,day in enumerate(scheduled_days)]

    n_poi = []
    for d in plan_days:
        for p in d.items:
            n_poi.append(p)

    scheduled_days.extend([Day(i, n_poi[i:i + 5]) for i in range(0, len(n_poi), 5)])
    trip.add_bulk_days(scheduled_days)

    print('output len', len(n_poi))
    ic('clusters', trip.days)
    plot_path(trip, 'map_clusters.html')
    return trip

# if __name__ == '__main__':
#     with open('../testing/samples/berlin_london_trip_data.pkl', 'rb') as input:
#         m_trip = pickle.load(input)
#
#     trip = plan_itinerary_schedule_clusters(m_trip)
#     print(trip)
