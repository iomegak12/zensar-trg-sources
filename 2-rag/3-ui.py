import os
import streamlit as st
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain.chains.summarize import load_summarize_chain

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
        index_name = os.getenv("PINECONE_INDEX_NAME")

    if embeddings is None:
        embeddings = create_embeddings()

    vector_store = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings
    )

    results = vector_store.similarity_search_with_score(query, k=no_of_results)

    return results


def get_summary_from_llm(resume_document):
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_deployment = os.getenv("AZURE_DEPLOYMENT_NAME")
    azure_api_version = os.getenv("AZURE_API_VERSION")

    if not azure_endpoint or not azure_api_key or not azure_deployment or not azure_api_version:
        raise ValueError("Azure OpenAI environment variables are not set.")

    llm = AzureChatOpenAI(
        azure_endpoint=azure_endpoint,
        api_key=azure_api_key,
        azure_deployment=azure_deployment,
        api_version=azure_api_version,
        temperature=0.0,
        model="gpt-4o",
    )

    chain = load_summarize_chain(llm, chain_type="map_reduce")

    summary = chain.invoke([resume_document])

    return summary


def main():
    try:
        embeddings = create_embeddings()

        if not embeddings:
            raise ValueError("Failed to create embeddings.")

        index_name = os.getenv("PINECONE_INDEX_NAME")

        if not index_name:
            raise ValueError(
                "PINECONE_INDEX_NAME environment variable is not set.")

        st.set_page_config(page_title="RAG CSAE Study", layout="wide")
        st.sidebar.title("RAG CSAE Study - Search")

        st.title("RAG CASE Study - UI")
        st.write(
            "This application allows you to search for similar documents and summarize them using LLMs.")

        query = st.sidebar.text_area("Job Description:", "")
        no_of_results = st.sidebar.number_input(
            "Number of results to return:", min_value=1, max_value=10, value=3)

        if st.sidebar.button("Search"):
            if query:
                try:
                    results = search_similar_documents(
                        query, no_of_results, index_name, embeddings)

                    if results:
                        st.sidebar.success(
                            f"Found {len(results)} similar documents.")

                        for i, (doc, score) in enumerate(results):
                            st.sidebar.write(
                                f"**Result {i + 1}:** {doc.metadata['source']} (Score: {score:.4f})")

                            st.subheader(f"Document {i + 1} Content")
                            st.write("**** FILE *** " + doc.metadata['source'])

                            with st.expander("Show Summary", expanded=False):
                                summary = get_summary_from_llm(doc)
                                st.write(summary["output_text"])
                    else:
                        st.sidebar.warning("No similar documents found.")
                except Exception as e:
                    st.sidebar.error(f"Error during search: {e}")
            else:
                st.sidebar.error("Please enter a valid query.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return


if __name__ == "__main__":
    main()
