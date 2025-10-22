"""
packet.py:
Defines basic data structures used for the router simulator.
- Packet: an IP-like packet
- Frame: an Ethernet-like frame that encapsulates a packet

These are simplified models.
"""

class Packet:
    """
    A simplified IP packet that carries a source, destination, and payload.

    Attributes:
        src (str): Source router name
        dest (str): Destination router name
        payload (str): The content of the packet
        ttl (int): Time-to-live (to prevent infinite loops in case of routing loops)
    """
    def __init__(self, src, dest, payload, ttl=64):
        self.src = src
        self.dest = dest
        self.payload = payload
        self.ttl = ttl

    def __repr__(self):
        """String representation for debugging."""
        return f"Packet(src={self.src}, dest={self.dest}, ttl={self.ttl}, payload={self.payload})"

class Frame:
    """
    A simplified ethernet frame that encapsulating a packet.

    Attributes:
        src_mac (str): Source MAC address
        dest_mac (str): Destination MAC address
        ethertype (int): Protocol identifier
        payload (Packet): Encapsulated Packet object
    """
    def __init__(self, src_mac, dest_mac, ethertype, payload):
        self.src_mac = src_mac
        self.dest_mac = dest_mac
        self.ethertype = ethertype
        self.payload = payload

    def __repr__(self):
        """String representation for debugging."""
        return f"Frame({self.src_mac}->{self.dest_mac}, type={hex(self.ethertype)}, payload={self.payload})"
