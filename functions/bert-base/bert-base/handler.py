import json
import torch
from transformers import BertModel, BertTokenizer

model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name, output_hidden_states=True)


def handle(req):
    body = json.loads(req)
    input_text = body["input"]
    input_ids = torch.tensor(
        [tokenizer.encode(input_text, add_special_tokens=True)])
    with torch.no_grad():
        outputs = model(input_ids)
        last_hidden_state = outputs[0]
    return last_hidden_state[0].tolist()
