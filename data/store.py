from langchain_neo4j import Neo4jVector
from neo4j import GraphDatabase
from modules.models.model import embed_model
from dotenv import load_dotenv
import os

load_dotenv()
url = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")


def create_vector_store() -> Neo4jVector:
    """載入 Neo4jVector"""
    
    # 建立並載入index
    try:
        store = Neo4jVector.from_existing_index(
            embed_model,
            url=url,
            username=username,
            password=password,
            index_name="vector",
        )
    except Exception:
        store = Neo4jVector.from_documents(
            [],
            embed_model,
            url=url,
            username=username,
            password=password,
            index_name="vector",
        )
    return store


def delete_chunks_by_path(pdf_path) -> None:
    """清除對應Pdf_path 的 chunk 儲存"""

    driver = GraphDatabase.driver(url, auth=(username, password))
    with driver.session() as session:
        session.run(
            """
            MATCH (c:Chunk)
            WHERE c.source = $pdf_path
            DETACH DELETE c
        """,
            pdf_path=pdf_path,
        )


def clear_all_chunks() -> None:
    """清除所有 chunk 及 vector index"""
    driver = GraphDatabase.driver(url, auth=(username, password))
    with driver.session() as session:
        session.run("MATCH (c:Chunk) DETACH DELETE c")
        session.run("DROP INDEX `vector` IF EXISTS")
