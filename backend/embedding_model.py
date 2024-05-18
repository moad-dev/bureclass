from sentence_transformers import SentenceTransformer
import torch
import os


if os.getenv('DUMMY_EMBEDDINGS') == 'true':    
    def embeddings_model(text) -> torch.Tensor:
        return torch.zeros(1024) 
else:
    device = "cuda" if torch.cuda.is_available() else "gpu"
    model = SentenceTransformer('data/saved_models/multilingual-e5-large-amethyst-advanced', device=device)
    def embeddings_model(text) -> torch.Tensor:
        return model.encode(text)

