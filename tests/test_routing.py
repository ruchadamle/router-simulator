import unittest
from backend.simulator.topology import Topology

class TestRouting(unittest.TestCase):
    def test_dijkstra(self):
        topo = Topology()
        for n in ['A', 'B', 'C']:
            topo.add_router(n)
        topo.link('A', 'B', 2)
        topo.link('B', 'C', 3)
        topo.link('A', 'C', 10)
        topo.compute_all_routing_tables()

        next_hop, cost = topo.routers['A'].routing_table['C']
        self.assertEqual(next_hop, 'B')
        self.assertEqual(cost, 5)

if __name__ == '__main__':
    unittest.main()
