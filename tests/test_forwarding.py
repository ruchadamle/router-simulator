import unittest
from backend.topology import Topology
from backend.packet import Packet

class TestForwarding(unittest.TestCase):
    def test_packet_delivery(self):
        topo = Topology()
        for n in ['R1', 'R2', 'R3']:
            topo.add_router(n)
        topo.link('R1', 'R2', 1)
        topo.link('R2', 'R3', 1)
        topo.compute_all_routing_tables()

        p = Packet('R1', 'R3', 'data')
        res = topo.routers['R1'].forward_packet(p, topo)
        self.assertIsNotNone(res)
        self.assertEqual(res.dest, 'R3')

if __name__ == '__main__':
    unittest.main()
