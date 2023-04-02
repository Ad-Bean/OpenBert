import json
import torch
from transformers import pipeline, logging, AutoTokenizer, AutoModel

logging.set_verbosity_error()

model_name = "huggingface-course/bert-finetuned-ner"
model_state_dict = torch.load('bert_model.pth')

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name, state_dict=model_state_dict)


def getType(word):
    if word == "PER":
        return "人名"
    elif word == "ORG":
        return "组织"
    elif word == "LOC":
        return "地点"
    else:
        return word


def handle(req):
    body = json.loads(req)
    text = body["text"]
    model_name = body["model_name"]

    mask_filler = pipeline("token-classification",
                           model=model_name, aggregation_strategy="simple")
    ans = mask_filler(text)

    res = "输入句子：{}\n\n".format(text)
    for n in ans:
        res += "类型：{}\n".format(getType(n["entity_group"]))
        res += "单词：{}\n".format(n["word"])
        res += "得分：{}\n\n".format(n["score"])

    return res
