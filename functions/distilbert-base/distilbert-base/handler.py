import json
from transformers import logging, AutoModel, AutoTokenizer, pipeline

logging.set_verbosity_error()

model_name = 'distilbert-base-uncased'
model = AutoModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)


def handle(req):
    try:
        body = json.loads(req)
        type = body["type"]
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e.msg)
        return "failed to process the task"

    if type == "mask":
        text = body["text"]
        unmasker = pipeline("fill-mask", model=model_name)
        ans = unmasker(text, top_k=1)
        res = {
            "text": text,
            "score": ans[0]["score"],
            "token_str": ans[0]["token_str"],
            "sequence": ans[0]["sequence"]
        }
        return json.dumps(res)
    elif type == "pretrain":
        return req

    return req
