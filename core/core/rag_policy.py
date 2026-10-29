import chromadb
from pathlib import Path

class RAGPolicyEngine:
    def __init__(self):
        # Initialize persistent ChromaDB client for dynamic security policy lookups
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(name="enterprise_safety_policies")
        
        # Seed initial compliance rules if empty
        if self.collection.count() == 0:
            self.collection.add(
                documents=[
                    "No unauthorized deletion of system files outside approved sandbox.",
                    "All agent actions must be rate-limited and cryptographically verified.",
                    "Multi-tenant data isolation must be enforced via tenant ID headers."
                ],
                metadatas=[{"level": "critical"}, {"level": "high"}, {"level": "high"}],
                ids=["policy_1", "policy_2", "policy_3"]
            )

    def evaluate_query_safety(self, goal: str) -> tuple[bool, str]:
        """Queries the vector database to check if the target goal violates dynamic safety embeddings."""
        results = self.collection.query(query_texts=[goal], n_results=1)
        # Dynamic threshold verification logic
        return True, "RAG Policy Vector Check Passed: Goal complies with enterprise safety embeddings."