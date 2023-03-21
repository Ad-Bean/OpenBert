import json
import torch
from transformers import pipeline, logging, AutoTokenizer, AutoModel

logging.set_verbosity_error()

model_name = "huggingface-course/distilbert-base-uncased-finetuned-imdb"
model_state_dict = torch.load('bert_model.pth')

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name, state_dict=model_state_dict)


def handle(req):
    body = json.loads(req)
    text = body["text"]
    model_name = body["model_name"]

    mask_filler = pipeline("fill-mask", model=model_name)
    ans = mask_filler(text, top_k=1)

    res = {
        "text": text,
        "score": ans[0]["score"],
        "token_str": ans[0]["token_str"],
        "sequence": ans[0]["sequence"]
    }

    return json.dumps(res)
