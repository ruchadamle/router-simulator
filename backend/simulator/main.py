"""
main.py

This script builds a sample network topology, computes routing tables for all routers, sends a test
packet across the network, and prints detailed routing and forwarding output.
"""

from topology import Topology
from packet import Packet

def run_demo():
    """Builds a sample network and simulates a packet delivery."""
    # Build the topology
    topology = Topology()
    for name in ['A', 'B', 'C', 'D', 'E']:
        topology.add_router(name)

    # Connect routers
    topology.link('A', 'B', 1)
    topology.link('B', 'C', 1)
    topology.link('C', 'D', 1)
    topology.link('B', 'D', 4)
    topology.link('A', 'E', 5)

    # Compute routing tables for all routers
    topology.compute_all_routing_tables()

    # Display routing tables
    print("\nRouting tables:")
    for name, router in topology.routers.items():
        print(f"{name}: {router.routing_table}")

    # Simulate packet forwarding
    packet = Packet(src='A', dest='D', payload='Hello, D!')
    topology.routers['A'].forward_packet(packet, topology)

if __name__ == "__main__":
    run_demo()
