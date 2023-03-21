import json
import torch
from transformers import pipeline, logging, AutoTokenizer, AutoModel

logging.set_verbosity_error()

model_name = "huggingface-course/bert-finetuned-ner"
model_state_dict = torch.load('bert_model.pth')

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name, state_dict=model_state_dict)


def handle(req):
    body = json.loads(req)
    text = body["text"]
    model_name = body["model_name"]

    mask_filler = pipeline("token-classification",
                           model=model_name, aggregation_strategy="simple")
    ans = mask_filler(text)

    return json.dumps(ans)
