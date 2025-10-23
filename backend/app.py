"""
app.py

Flask backend API for the network simulator.
Exposes endpoints to get network topology and route a packet & return the path.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from simulator.topology import Topology
from simulator.packet import Packet
import random
import os

app = Flask(__name__)
CORS(app)

# Initialize a global network topology
topology = Topology()

# Create 20 routers
for i in range(1, 21):
    topology.add_router(f"R{i}")

nodes = list(topology.routers.keys())
random.shuffle(nodes)  # shuffle nodes for spanning tree

# Spanning tree: ensures all nodes are connected
for i in range(1, len(nodes)):
    a = nodes[i]
    b = nodes[random.randint(0, i - 1)]
    topology.link(a, b, cost=random.randint(1, 5))

# Extra links: retry if sample hits duplicates
max_extra_links = 15
attempts = 0
links_added = 0
while links_added < max_extra_links and attempts < 100:
    a, b = random.sample(nodes, 2)
    if b not in topology.routers[a].neighbors:
        topology.link(a, b, cost=random.randint(1, 5))
        links_added += 1
    attempts += 1

# Compute routing tables for all routers
topology.compute_all_routing_tables()

@app.route('/api/topology', methods=['GET'])
def get_topology():
    routers = [{'id': name} for name in topology.routers]
    links = []

    for name, router in topology.routers.items():
        for neighbor, cost in router.neighbors.items():
            if {'source': neighbor, 'target': name, 'cost': cost} not in links:
                links.append({'source': name, 'target': neighbor, 'cost': cost})

    return jsonify({'routers': routers, 'links': links})


@app.route('/api/route', methods=['POST'])
def route_packet():
    data = request.get_json()
    src = data.get('src')
    dest = data.get('dest')
    payload = data.get('payload', 'Hello')

    if src not in topology.routers or dest not in topology.routers:
        return jsonify({'path': [], 'delivered': False, 'error': 'Invalid source or destination'}), 400

    packet = Packet(src=src, dest=dest, payload=payload)
    hops = []
    router = topology.routers[src]

    while True:
        hops.append(router.name)
        if packet.ttl <= 0 or router.name == dest:
            break
        entry = router.routing_table.get(dest)
        if not entry:
            return jsonify({'path': hops, 'delivered': False, 'error': 'Destination unreachable'}), 400
        next_hop = entry[0]
        packet.ttl -= 1
        router = topology.routers[next_hop]

    return jsonify({'path': hops, 'delivered': router.name == dest})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
