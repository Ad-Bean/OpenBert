import torch
from transformers import AutoModel, AutoTokenizer

model_name = "huggingface-course/distilbert-base-uncased-finetuned-imdb"
model = AutoModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

torch.save(model.state_dict(), 'bert_model.pth')
tokenizer.save_pretrained('bert_tokenizer')
