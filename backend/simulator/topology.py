"""
topology.py

Defines the Topology class that manages the simulated network by:
- Creating routers
- Connecting them via links
- Building a graph representation for Dijkstra's algorithm
- Triggering routing table computation across all routers
"""
from .router import Router

class Topology:
    """
    Represents the network of interconnected routers.

    Attributes:
        routers (dict): All routers in the network, keyed by router name.
    """

    def __init__(self):
        self.routers = {}

    def add_router(self, router_name):
        """
        Adds a new router to the topology.

        :param router_name (str): Unqiue name of the router

        :return: The newly created Router object
        """
        new_router = Router(router_name)
        self.routers[router_name] = new_router
        return new_router

    def link(self, router_a_name, router_b_name, cost=1):
        """
        Connects two routers with a bidirectional link.

        :param router_a_name (str): Name of first router
        :param router_b_name (str): Name of second router
        :param cost (int): Link cost (default cost = 1)
        """
        router_a = self.routers[router_a_name]
        router_b = self.routers[router_b_name]
        router_a.add_link(router_b, cost)
        router_b.add_link(router_a, cost)

    def build_graph(self):
        """
        Returns the network graph as a dict for routing algorithms.

        :return: { router_name: {neighbor_name: cost, ...}, ... }
        """
        graph = {}
        for router_name, router_obj in self.routers.items():
            graph[router_name] = dict(router_obj.neighbors)
        return graph

    def compute_all_routing_tables(self):
        """
        Computes routing tables for all routers in the network.
        """
        network_graph = self.build_graph()
        for router_obj in self.routers.values():
            router_obj.compute_routing_table(network_graph)
