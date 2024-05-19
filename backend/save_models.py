from sentence_transformers import SentenceTransformer

model_checkpoint = "MOADdev/multilingual-e5-large-amethyst"
save_path = "data/saved_models/multilingual-e5-large-amethyst"

model = SentenceTransformer(model_checkpoint)
model.save(save_path)
