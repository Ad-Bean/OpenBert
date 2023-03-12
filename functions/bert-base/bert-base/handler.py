import json
import torch
from transformers import BertModel, BertTokenizer

model_state_dict = torch.load('bert_model.pth')
model = BertModel.from_pretrained('bert-base-uncased', state_dict=model_state_dict)
tokenizer = BertTokenizer.from_pretrained('bert_tokenizer')

def handle(req):
    body = json.loads(req)
    input_text = body["input"]
    input_ids = torch.tensor(
        [tokenizer.encode(input_text, add_special_tokens=True)])
    with torch.no_grad():
        outputs = model(input_ids)
        last_hidden_state = outputs[0]
    return last_hidden_state[0].tolist()
