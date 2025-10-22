"""
router.py

Defines the Router class, which:
- Maintains neighbor connections
- Computes shortest path routing tables with Dijkstra's algorithm
- Forwards packets based on those tables
"""

import heapq

class Router:
    """
    Represents a single router in the simulated network.

    Attributes:
        name (str): Router identifier
        neighbors (dict): Directly connected routers and their link costs
        routing_table (dict): Computed table mapping destinations to (next_hop, total_cost)
                              next_hop - the neighbor to forward packets to first
                              total_cost - how far that path costs
    """
    def __init__(self, name):
        self.name = name
        self.neighbors = {}
        self.routing_table = {}

    def add_link(self, neighbor, cost=1):
        """
        Creates a link to another Router.

        :param neighbor (Router): Neighbor Router object
        :param cost (int): Cost/weight of the link
        """
        self.neighbors[neighbor.name] = cost

    def compute_routing_table(self, network_graph):
        """
        Computes the shortest path to all other routers using Dijkstra's algorithm.

        :param network_graph (dict): A dictionary representing the network topology:
                                     { router_name: {neighbor_name: link_cost, ...}, ... }
        """

        # Initialize distance to all routers as "infinity" and no previous hop
        distance_to_router = {router_name: float('inf') for router_name in network_graph}
        previous_hop = {router_name: None for router_name in network_graph}

        # Distance to self is zero
        distance_to_router[self.name] = 0

        # Priority queue for Dijkstra
        priority_queue = [(0, self.name)]

        while priority_queue:
            current_distance, current_router = heapq.heappop(priority_queue)

            # Skip if we already found a shorter path
            if current_distance > distance_to_router[current_router]:
                continue

            # Check all neighbors of the current router
            for neighbor_name, link_cost in network_graph[current_router].items():
                new_distance = current_distance + link_cost
                if new_distance < distance_to_router[neighbor_name]:
                    distance_to_router[neighbor_name] = new_distance
                    previous_hop[neighbor_name] = current_router
                    heapq.heappush(priority_queue, (new_distance, neighbor_name))

        # Build the routing table
        # For each destination, record next hop and total cost
        self.routing_table = {}
        for destination in network_graph:
            if destination == self.name or distance_to_router[destination] == float('inf'):
                # Skip self and unreachable routers
                continue

            # Trace back from destination to determine next hop
            current = destination
            while previous_hop[current] and previous_hop[current] != self.name:
                current = previous_hop[current]

            next_hop = current
            total_cost = distance_to_router[destination]
            self.routing_table[destination] = (next_hop, total_cost)

    def forward_packet(self, packet, topology):
        """
        Simulates packet forwarding based on the routing table.

        :param packet (Packet): The packet to forward
        :param topology (Topology): Reference to the network topology

        :return: The delivered packet if it reached its destination, else None
        """
        # Drop packet if TTL expired
        if packet.ttl <= 0:
            print(f"{self.name}: dropping {packet} (TTL expired)")
            return None

        # If the router is the destination, the packet is delivered
        if packet.dest == self.name:
            print(f"{self.name}: delivered {packet}")
            return packet

        # Lookup next hop in the routing table
        entry = self.routing_table.get(packet.dest)
        if not entry:
            print(f"{self.name}: no route for {packet.dest}, dropping {packet}")
            return None

        next_hop = entry[0]
        packet.ttl -= 1
        print(f"{self.name}: forwarding {packet} to {next_hop}")

        # Forward recursively to next router
        next_router = topology.routers[next_hop]
        return next_router.forward_packet(packet, topology)
