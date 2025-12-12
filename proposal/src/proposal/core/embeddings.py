from langchain_community.embeddings import HuggingFaceBgeEmbeddings


bge_embedding = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-large-en-v1.5",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)