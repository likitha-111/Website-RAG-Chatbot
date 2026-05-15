from rag.embeddings import embedding_model
from rag.vector_store import collection


def retrieve_documents(query, k=4):

    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    context = []

    for doc, meta in zip(docs, metas):
        context.append({
            "content": doc,
            "source": meta["source"],
            "title": meta["title"]
        })

    return context