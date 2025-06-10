# RAG-VERTEXAI-GCP
This GitHub repository showcases two complementary approaches to grounding LLMs using __Griptape__ (_an enterprise ready alternative to LangChain_) and __Google Cloud Platform tools__, demonstrating different data integration strategies for enterprise AI applications. 
### Project 1: GCP Model Garden Integration (`gcp-agent.py`)  
**Objective**: Connect to Vertex AI Model Garden via public APIs while grounding responses with real-time web data  

**Implementation**:  
- Accesses Google's Gemini 2.0 Flash model through Vertex AI  
- Uses Griptape's workflow engine to manage multi-step AI tasks  
- Grounds model outputs using Google Search results  
- Implements secure API authentication via GCP service accounts  

**Technical Components**:  
```python
# Simplified workflow example
from griptape.structures import Workflow
from griptape.tools import WebSearchTool

agent_workflow = Workflow()
agent_workflow.add_tool(WebSearchTool(google_api_key="..."))

task = agent_workflow.add_task(
    "Analyze current trends in AI governance using web sources"
)
print(task.output.value)
```

**Portfolio Tools**:  
| Category       | Technologies Used          |  
|----------------|----------------------------|  
| Cloud AI       | Vertex AI Model Garden     |  
| Data Grounding | Google Search API          |  
| Orchestration  | Griptape Workflow Engine   |  

---

### Project 2: Document-Based Grounding System (`griptape-gcp.py`)  
**Objective**: Ground LLM responses in private PDF documents using vector search  

**Core Features**:  
- Local PostgreSQL+pgvector database via Docker  
- Automated PDF processing pipeline  
- Semantic search capabilities over document content  
- Hybrid search (vector + keyword) implementation  

**System Flow**:  
1. User uploads PDFs to `./docs` directory  
2. Script chunks documents and generates embeddings  
3. Stores vectors in pgvector-enabled PostgreSQL  
4. Queries combine semantic search and LLM generation  

**Technical Setup**:  
```bash
# Start vector database
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=secret ankane/pgvector
```

```python
# PDF processing example
from griptape.loaders import PdfLoader

documents = PdfLoader().load("docs/whitepaper.pdf")
vector_store.upsert_vectors(process_documents(documents))
```

---

### Combined Architecture  
**Data Flow**:  
```
[User Query] → [Griptape Agent] → [Model Garden LLM]  
                   ↑  
[Web Results/PDF Vectors] ← [Hybrid Search]  
```

**Key Differentiators**:  
- Dual grounding strategy (public web + private docs)  
- Portable architecture with Dockerized components  
- Production-ready error handling for API failures  
- Configurable fallback between data sources  

**DevOps Components**:  
1. Infrastructure-as-Code: Docker Compose for database  
2. CI/CD-ready Python package management  
3. Environment isolation for GCP credentials  

This implementation demonstrates practical patterns for building enterprise-grade LLM systems using GCP services and open-source tools, emphasizing data grounding and production readiness.