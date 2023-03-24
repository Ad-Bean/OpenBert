import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "Callidior/bert2bert-base-arxiv-titlegen"
model = AutoTokenizer.from_pretrained(model_name)

tokenizer = AutoTokenizer.from_pretrained(
    "Callidior/bert2bert-base-arxiv-titlegen")
model = AutoModelForSeq2SeqLM.from_pretrained(
    "Callidior/bert2bert-base-arxiv-titlegen")

torch.save(model.state_dict(), 'bert_model.pth')
tokenizer.save_pretrained('bert_tokenizer')
