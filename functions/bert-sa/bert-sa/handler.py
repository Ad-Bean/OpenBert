import json
import torch
from transformers import pipeline, logging, AutoTokenizer, AutoModel

logging.set_verbosity_error()

model_name = "nickwong64/bert-base-uncased-poems-sentiment"
model_state_dict = torch.load('bert_model.pth')

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name, state_dict=model_state_dict)


def handle(req):
    body = json.loads(req)
    text = body["text"]
    model_name = body["model_name"]

    nlp = pipeline(task='text-classification', model=model_name)
    ans = nlp(text)
    res = "输入句子：{}\n\n".format(text)
    res += "文本分类：{}\n".format(ans[0]["label"])
    res += "得分：{}\n".format(ans[0]["score"])
    return res
