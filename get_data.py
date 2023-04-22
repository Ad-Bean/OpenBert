# import uuid
# import requests
# import torch
# from minio import Minio
# from transformers import BertModel, BertTokenizer, AutoModelForMaskedLM, AutoTokenizer

# model_name = 'distilbert-base-uncased'
# model = AutoModelForMaskedLM.from_pretrained(model_name)
# tokenizer = AutoTokenizer.from_pretrained(model_name)


# directory = r'./models/distilbert-base-uncased'
# model.save_pretrained(directory)
# tokenizer.save_pretrained(directory)


# import torch
# from transformers import AutoModel, AutoTokenizer
from datasets import load_dataset

# model_name = "distilbert-base-uncased"
# model = AutoModel.from_pretrained(model_name)
# tokenizer = AutoTokenizer.from_pretrained(model_name)


datasets = "imdb"
imdb_dataset = load_dataset("models/imdb")

# # torch.save(model.state_dict(), 'bert_model.pth')
# # tokenizer.save_pretrained('bert_tokenizer')

# imdb_dataset.save_to_disk("models/imdb")
