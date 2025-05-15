import re
import os
from vertexai import rag

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

def get_corpus_resource_name(corpus_name: str) -> str:
    """
    Convert a corpus name to its full resource name if needed.
    Handles various input formats and ensures the returned name follows Vertex AI's requirements.

    Args:
        corpus_name (str): The corpus name or display name

    Returns:
        str: The full resource name of the corpus
    """

    if re.match(r"^projects/[^/]+/locations/[^/]+/ragCorpora/[^/]+$", corpus_name):
        return corpus_name

    try:
        corpora = rag.list_corpora()
        for corpus in corpora:
            if hasattr(corpus, "display_name") and corpus.display_name == corpus_name:
                return corpus.name
    except Exception as e:
        print(f"Error when checking for corpus display name: {str(e)}")
        pass

    if "/" in corpus_name:
        corpus_id = corpus_name.split("/")[-1]
    else:
        corpus_id = corpus_name

    corpus_id = re.sub(r"[^a-zA-Z0-9_-]", "_", corpus_id)

    return f"projects/{PROJECT_ID}/locations/{LOCATION}/ragCorpora/{corpus_id}"