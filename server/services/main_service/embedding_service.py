import os
import threading
from typing import List, Optional

import numpy as np
from sentence_transformers import SentenceTransformer

_model = None
_model_lock = threading.Lock()


def _default_model_path() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'my_model'))


def load_model(model_path: Optional[str] = None, device: str = 'cpu') -> SentenceTransformer:
    """Lazily load and return the SentenceTransformer model.

    By default loads the local model under `server/my_model`.
    """
    global _model
    if model_path is None:
        model_path = _default_model_path()
    if _model is None:
        with _model_lock:
            if _model is None:
                _model = SentenceTransformer(model_path, device=device)
    return _model


def embed_texts(texts: List[str], normalize: bool = True, model_path: Optional[str] = None) -> np.ndarray:
    """Encode a list of texts to embeddings (numpy array).

    Returns an array of shape (len(texts), dim).
    """
    model = load_model(model_path)
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    if normalize:
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        embeddings = embeddings / norms
    return embeddings


def embed_text(text: str, normalize: bool = True, model_path: Optional[str] = None) -> np.ndarray:
    """Encode a single text and return its embedding vector."""
    return embed_texts([text], normalize=normalize, model_path=model_path)[0]
