import json
import torch
from transformers import pipeline, logging, AutoTokenizer, AutoModel

logging.set_verbosity_error()

model_name = "huggingface-course/bert-finetuned-squad"
model_state_dict = torch.load('bert_model.pth')

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name, state_dict=model_state_dict)


def handle(req):
    body = json.loads(req)
    context = body["context"]
    question = body["question"]
    model_name = body["model_name"]

    question_answerer = pipeline("question-answering", model=model_name)
    ans = question_answerer(question=question, context=context)

    res = "问题：{}\n\n".format(question)
    res += "答案：{}\n".format(ans["answer"])
    res += "得分：{}\n".format(ans["score"])
    return res
