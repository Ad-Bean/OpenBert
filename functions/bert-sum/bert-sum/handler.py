import json
import torch
from transformers import logging, AutoTokenizer, AutoModelForSeq2SeqLM

logging.set_verbosity_error()

model_name = "Callidior/bert2bert-base-arxiv-titlegen"
model_state_dict = torch.load('bert_model.pth')


model = AutoModelForSeq2SeqLM.from_pretrained(
    "Callidior/bert2bert-base-arxiv-titlegen", state_dict=model_state_dict)
tokenizer = AutoTokenizer.from_pretrained(
    "Callidior/bert2bert-base-arxiv-titlegen")


def handle(req):
    body = json.loads(req)
    text = body["text"]

    inputs = tokenizer(text, max_length=1024, truncation=True,
                       padding="longest", return_tensors="pt")

    summary_ids = model.generate(
        inputs["input_ids"], num_beams=4, max_length=100, early_stopping=True)

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    res = "输入文本：{}\n\n".format(text)
    res += "文本概括：{}\n".format(summary)
    return res
