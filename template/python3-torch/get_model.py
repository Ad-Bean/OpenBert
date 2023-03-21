import torch
from transformers import BertModel, BertTokenizer

model_name = "huggingface-course/distilbert-base-uncased-finetuned-imdb"
model = BertModel.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

torch.save(model.state_dict(), 'bert_model.pth')
tokenizer.save_pretrained('bert_tokenizer')
