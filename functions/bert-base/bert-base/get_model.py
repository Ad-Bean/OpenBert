import torch
from transformers import BertModel, AutoTokenizer

model_name = 'bert-base-uncased'
model = BertModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

torch.save(model.state_dict(), 'bert_model.pth')
tokenizer.save_pretrained('bert_tokenizer')
