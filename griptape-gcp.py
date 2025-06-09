from configparser import ConfigParser 
from griptape.chunkers import PdfChunker
from griptape.loaders import PdfLoader
from griptape.drivers.vector.pgvector import PgVectorVectorStoreDriver
from griptape.drivers.prompt.google import GooglePromptDriver
from griptape.drivers.embedding.google import GoogleEmbeddingDriver
from griptape.tools import VectorStoreTool
from griptape.structures import Agent
from griptape.utils import Chat
import time
import concurrent.futures


# Get secrects as variables 
config = ConfigParser()
config.read("./secrets.ini")
GOOGLE_API_KEY = config.get("gcp","api_key")
DB_USER = config.get("docker", "db_user")
DB_PASSWORD = config.get("docker","db_pass")
DB_HOST = "localhost"
DB_PORT = "5432"
DB_Name = "developer"

def process_item(item):
    # process items. item is a tuple with the pdf file path and the namespace
    print(f"Processing tuple: {item}")
    print(f"Loading PDF: {item[0]}")
    pdf_artifact = PdfLoader().load(item[0])
    print(f"Chunking PDF: {item[0]}")
    chunks = PdfChunker(max_tokens=500).chunk(pdf_artifact)
    print(f"Upserting chunks from: {item[0]} in namespace: {item[1]}")
    vector_store_driver.upsert_text_artifacts({item[1]: chunks})

# define function to process a list in threads
def process_list_in_threads(items):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_item, item) for item in items]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # Retrieve the result to catch any exceptions
            except Exception as e:
                print(f"An error occurred: {e}")

# Create the connetion string
db_connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_Name}"

# Create the PgVectorVectorStoreDriver
vector_store_driver = PgVectorVectorStoreDriver(
    connection_string=db_connection_string,
    embedding_driver=GoogleEmbeddingDriver(
        model="models/text-embedding-004",
        api_key=GOOGLE_API_KEY
    ),
    table_name="vectors",
)

# Install required Postgres extensions and create database schema
vector_store_driver.setup()

documents_to_upsert = [  # list your PDF documents here. Each tuple should contain a PDF file path and a namespace.
    ("./doc/LLM_AI_Security_and_Governance_Checklist-v1.1.pdf", "LLM AI Security"),
    ("./doc/Implementation_Guide_for_the_AI_Cyber_Security_Code_of_Practice (1).pdf", "AI Cyber Security code of practice"),
]

if True:
    print("Upserting documents in threads, one thread per document")
    t1 = time.perf_counter()  # Start the timer
    process_list_in_threads(documents_to_upsert)
    t2 = time.perf_counter()  # Stop the timer
    print(t2 - t1, "Completed with {} seconds elapsed")  # Print the time elapsed

# Create the tool
flextool = VectorStoreTool(
    vector_store_driver=vector_store_driver,
    description="This DB has information about the LLM AI Security PDF",
    query_params={"namespace": "LLM AI Security"},
    name="flextool"
)
aitool = VectorStoreTool(
    vector_store_driver=vector_store_driver,
    description="This DB has information about AI Cyber Security code of practice PDF",
    query_params={"namespace": "AI Cyber Security code of practice"},
    name="aitool" 
)

# Create the agent
agent = Agent(
    tools=[flextool, aitool],
    prompt_driver=GooglePromptDriver(
        model="gemini-2.0-flash",
        api_key=GOOGLE_API_KEY,
        stream=True
    ),
   
)

# Run the agent
Chat(agent).start()


