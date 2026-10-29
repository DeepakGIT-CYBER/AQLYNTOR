import time

class KubernetesMeshSimulator:
    def __init__(self):
        self.clusters = {"AWS-Primary": "HEALTHY", "GCP-Secondary": "HEALTHY"}

    def simulate_node_failure(self, target_cluster: str) -> dict:
        if target_cluster in self.clusters:
            self.clusters[target_cluster] = "CRASHED_AUTO_HEALING"
            time.sleep(0.1)
            self.clusters[target_cluster] = "RESTORED_HEALTHY"
        return {
            "version": "v4.0",
            "mesh_status": "AUTO_HEALED",
            "cluster_states": self.clusters
        }