"""ADK Services definition module for AlgebraMaster agent."""

from google.adk.memory import VertexAiMemoryBankService

# Hardcoded project, location, and Memory Bank ID (Agent Engine ID)
PROJECT_ID = "qwiklabs-gcp-02-7e80680db9e2"
LOCATION = "us-east1"
MEMORY_BANK_ID = "3135074887673053184"


def memory_bank_service_builder():
    """Factory function for initializing VertexAiMemoryBankService."""
    return VertexAiMemoryBankService(
        project=PROJECT_ID,
        location=LOCATION,
        agent_engine_id=MEMORY_BANK_ID,
    )
