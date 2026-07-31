from sentence_transformers import SentenceTransformer

# Load once when the application starts
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str) -> list[float]:
    return model.encode(
        text,
        convert_to_numpy=True,
    ).tolist()