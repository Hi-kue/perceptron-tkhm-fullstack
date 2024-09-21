from config.log_config import logger as log
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

# baselib
import os
from pathlib import Path

env_path = Path("../.env")
load_dotenv(dotenv_path=env_path)

pinec = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

pinec_build = {
    "name": "alfai-vdb",
    "dimension": 1536,
    "metrics": ["cosine", "euclidean"],
    "spec": ServerlessSpec(cloud="aws", region="us-east-1")
}


def pinec_build_index() -> None:
    if pinec_build["name"] in pinec.list_indexes().names():
        log.info(f"Index found, deleting previous index named: {pinec_build['name']}")
        pinec.delete_index(pinec_build["name"])

        pinec.create_index(
            name=pinec_build["name"],
            dimension=pinec_build["dimension"],
            metric=pinec_build["metrics"][0],
            spec=pinec_build["spec"]
        )

    else:
        log.info("No previous index found, creating new index.")

        pinec.create_index(
            name=pinec_build["name"],
            dimension=pinec_build["dimension"],
            metric=pinec_build["metrics"][0],
            spec=pinec_build["spec"]
        )


def pinec_search_index(query: str) -> dict:
    return pinec.query(index_name=pinec_build["name"], query_vector=query, top_k=3)


def pinec_upsert_index(data: dict) -> None:
    pinec_index = pinec.Index(name=pinec_build["name"])
    pinec_index.upsert(
        vectors=data["vectors"],
        namespace=data["namespace"],
    )

# NOTE: future implementations will require a RAG application for better search and filtering
