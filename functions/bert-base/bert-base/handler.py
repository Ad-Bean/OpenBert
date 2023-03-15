import json
import torch
from transformers import logging, BertModel, BertTokenizer, BertForNextSentencePrediction

logging.set_verbosity_error()

model_name = 'bert-base-uncased'
model_state_dict = torch.load('bert_model.pth')
model = BertModel.from_pretrained(model_name, state_dict=model_state_dict)
tokenizer = BertTokenizer.from_pretrained(model_name)
modelNSP = BertForNextSentencePrediction.from_pretrained(
    model_name, state_dict=model_state_dict)


def handle(req):
    body = json.loads(req)
    type = body["type"]
    if type == "nsp":
        text_a = body["text_a"]
        text_b = body["text_b"]
        inputs = tokenizer(text_a, text_b, return_tensors='pt')
        outputs = modelNSP(**inputs)
        probability = torch.softmax(outputs.logits, dim=1)[0][0].item()

        res = {
            "text_a": text_a,
            "text_b": text_b,
            "probability": probability
        }
        return json.dumps(res)
    elif type == "mask":
        input_text = body["input"]
        input_ids = torch.tensor(
            [tokenizer.encode(input_text, add_special_tokens=True)])
        with torch.no_grad():
            outputs = model(input_ids)
            last_hidden_state = outputs[0]
        return last_hidden_state[0].tolist()
