"""
AQLYNTOR v11.0 — Enterprise Telemetry & Prometheus Observability Core
"""
from prometheus_client import Counter, Histogram, Gauge

# Custom Prometheus Metrics for AQLYNTOR Defense Grid
FIREWALL_THREAT_BLOCKS = Counter(
    "aqlyntor_firewall_threat_blocks_total",
    "Total malicious payloads intercepted by AQLYNTOR UltraFirewall",
    ["threat_type", "client_ip"]
)

REQUEST_LATENCY = Histogram(
    "aqlyntor_request_latency_seconds",
    "Request execution latency across AQLYNTOR Gateway pipelines",
    ["endpoint"]
)

ACTIVE_SYSTEM_NODES = Gauge(
    "aqlyntor_active_system_nodes",
    "Total active Mesh/Federation nodes in v11.0 Grid"
)

def record_threat_block(threat_type: str, client_ip: str):
    FIREWALL_THREAT_BLOCKS.labels(threat_type=threat_type, client_ip=client_ip).inc()

def set_active_nodes(count: int):
    ACTIVE_SYSTEM_NODES.set(count)