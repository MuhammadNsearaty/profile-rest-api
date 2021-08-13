import pickle

from Planner import Planner
from icecream import ic
from matplotlib import pyplot as plt

# import networkx as nx

axis = [[32.745255, -74.034775], [34.155834, -119.202789], [42.933334, -100.566666], [42.095554, -79.238609],
        [38.846668, -71.948059], [36.392502, -81.534447], [32.745255, -74.034775]]

with open('../../../testing/samples/dubai_trip_data.pkl', 'rb') as input:
    m_trip = pickle.load(input)

items = list(m_trip)


def plot_path(path):
    x_axes = [item.coordinate['lat'] for item in path]
    y_axes = [item.coordinate['lon'] for item in path]
    plt.plot(x_axes, y_axes, 'o--')

    plt.plot(x_axes[0], y_axes[0], 'go--', linewidth=2, markersize=12, color="r")
    plt.plot(x_axes[-2], y_axes[-2], 'go--', linewidth=2, linestyle="dashed", markersize=12, color='r')
    for i, x in enumerate(x_axes):
        plt.annotate(str(i) + path[i].item_type[:2], (x_axes[i], y_axes[i]))


if __name__ == '__main__':
    planner = Planner(items)
    optimal_route, optimal_cost, path = planner.plan_two_opt(iterations=1)
    ic(optimal_cost)

    full_plan = planner.plan_itinerary()
    ic(full_plan)
