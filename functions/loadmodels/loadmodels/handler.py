import json
import os
from minio import Minio
import torch
from transformers import logging, BertTokenizer, BertForNextSentencePrediction

logging.set_verbosity_error()

model_name = 'bert-base-uncased'
token_name = 'bert_tokenizer'
file_path = "/tmp/"


def handle(req):
    try:
        body = json.loads(req)
        text_a = body["text_a"]
        text_b = body["text_b"]
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e.msg)
        return "failed to process the task"

    mc = Minio(os.environ['minio_hostname'],
               access_key=os.environ['minio_access_key'],
               secret_key=os.environ['minio_secret_key'],
               secure=False)

    objects = mc.list_objects(model_name, recursive=True)
    for obj in objects:
        file_name = obj.object_name.split('/')[-1]
        mc.fget_object(model_name, file_name, file_path + file_name)

    # get model state_dict
    # mc.fget_object(model_name, object_name, file_path+object_name)
    # model_state_dict = torch.load(file_path)
    modelNSP = BertForNextSentencePrediction.from_pretrained(file_path)
    tokenizer = BertTokenizer.from_pretrained(file_path)

    inputs = tokenizer(text_a, text_b, return_tensors='pt')
    outputs = modelNSP(**inputs)
    probability = torch.nn.functional.softmax(
        outputs.logits, dim=1)[0][0].item()
    res = {
        "text_a": text_a,
        "text_b": text_b,
        "probability": probability,
    }

    # try:
    #     os.remove(file_path+object_name)
    #     print(f"{file_path+object_name} 文件删除成功！")
    # except FileNotFoundError as e:
    #     print(f"{file_path+object_name} 文件不存在，无法删除！")
    # except Exception as e:
    #     print(f"{file_path+object_name} 文件删除失败，错误信息为：{e}")

    return json.dumps(res)
