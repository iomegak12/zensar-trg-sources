import os

from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv(override=True)

azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_deployment = os.getenv("AZURE_DEPLOYMENT_NAME")
azure_api_version = os.getenv("AZURE_API_VERSION")
azure_embedding_deployment = os.getenv(
    "AZURE_EMBEDDING_DEPLOYMENT_NAME", "text-embedding-3-large")

if not azure_endpoint or not azure_api_key or not azure_deployment or not azure_api_version:
    raise ValueError("Azure OpenAI environment variables are not set.")

pinecone_api_key = os.getenv("PINECONE_API_KEY")

if not pinecone_api_key:
    raise ValueError("PINECONE_API_KEY environment variable is not set.")

pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

if not pinecone_index_name:
    raise ValueError("PINECONE_INDEX_NAME environment variable is not set.")


def create_embeddings():
    embeddings = AzureOpenAIEmbeddings(azure_endpoint=azure_endpoint,
                                       model="text-embedding-3-large",
                                       api_key=azure_api_key,
                                       deployment=azure_embedding_deployment,
                                       dimensions=3072,
                                       )

    return embeddings


def search_similar_documents(query, no_of_results=3, index_name=None, embeddings=None):
    if query is None or query.strip() == "":
        raise ValueError("Query must be a non-empty string.")

    if index_name is None:
        index_name = pinecone_index_name

    if embeddings is None:
        embeddings = create_embeddings()

    vector_store = PineconeVectorStore(
        index_name=pinecone_index_name,
        embedding=embeddings
    )

    results = vector_store.similarity_search_with_score(query, k=no_of_results)

    return results


if __name__ == "__main__":
    query = """
        Experienced Candidate with Embedded Systems and Firmware Development Skills
        Requirements:
        Bachelor's degree in Computer Science
        At least 5 years of experience in embedded systems and firmware development
        Understanding of Computer Architecture, User Interfacing Technologies and Programming Languages
    """

    embeddings = create_embeddings()
    no_of_results = 3

    results = search_similar_documents(
        query, no_of_results, pinecone_index_name, embeddings)

    print(f"Query: {query}")
    print(f"Number of results: {len(results)}")

    for i, (doc, score) in enumerate(results):
        print(f"Result {i + 1}:")
        print(f"Score: {score}")
        # Print first 200 characters
        print(f"Document content: {doc.page_content[:200]}...")
        print(f"Source: {doc.metadata.get('source', 'Unknown')}")
        print("=" * 40)
