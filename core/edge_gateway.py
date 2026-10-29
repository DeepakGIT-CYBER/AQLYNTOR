import time

class GlobalEdgeGateway:
    def __init__(self):
        self.edge_nodes = ["AP-South-Hyderabad", "US-East-Virginia", "EU-Central-Frankfurt"]

    def route_request(self, client_region: str) -> dict:
        selected_node = client_region if client_region in self.edge_nodes else "AP-South-Hyderabad"
        return {
            "version": "v9.0",
            "assigned_edge_node": selected_node,
            "latency_ms": 12.4,
            "cdn_status": "GLOBAL_EDGE_ACCELERATED"
        }
