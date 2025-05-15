import re
import os
import vertexai
from vertexai import rag

from config import (
    DEFAULT_EMBEDDING_MODEL,
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_CHUNK_SIZE,
    DEFAULT_EMBEDDING_REQUESTS_PER_MIN,
)
from tools.utils import get_corpus_resource_name

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

vertexai.init(project=PROJECT_ID, location=LOCATION)
corpus_name = os.getenv("GOOGLE_CORPUS_NAME")
paths = [
    "gs://solar-datasheets/DT-M-0010 E Datasheet_Vertex_DE20_EN_2024_A.pdf",
    "gs://solar-datasheets/DT-M-0011 E Datasheet_Vertex_DEG20C.20_EN_2024_A.pdf",
    "gs://solar-datasheets/DT-M-0012 F Datasheet_Vertex_DE21_EN_2024_B.pdf",
    "gs://solar-datasheets/DT-M-0013 C Datasheet_Vertex_DEG21C.20_EN_2024_A_0.pdf"
]

try:
    display_name = re.sub(r"[^a-zA-Z0-9_-]", "_", corpus_name)

    embedding_model_config = rag.RagEmbeddingModelConfig(
        vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
            publisher_model=DEFAULT_EMBEDDING_MODEL
        )
    )

    rag_corpus = rag.create_corpus(
        display_name=display_name,
        backend_config=rag.RagVectorDbConfig(
            rag_embedding_model_config=embedding_model_config
        ),
    )
    corpus_resource_name = get_corpus_resource_name(corpus_name)

    transformation_config = rag.TransformationConfig(
        chunking_config=rag.ChunkingConfig(
            chunk_size=DEFAULT_CHUNK_SIZE,
            chunk_overlap=DEFAULT_CHUNK_OVERLAP,
        ),
    )

    transformation_config = rag.TransformationConfig(
            chunking_config=rag.ChunkingConfig(
                chunk_size=DEFAULT_CHUNK_SIZE,
                chunk_overlap=DEFAULT_CHUNK_OVERLAP,
            ),
        )

    import_result = rag.import_files(
        corpus_resource_name,
        paths,
        transformation_config=transformation_config,
        max_embedding_requests_per_min=DEFAULT_EMBEDDING_REQUESTS_PER_MIN,
    )
except Exception as e:
    print(f"Error when checking for corpus display name: {str(e)}")
    pass