from transformers import BertModel, BertTokenizer
import torch
import json

# 加载预训练 BERT 模型和分词器
model = BertModel.from_pretrained('bert-base-uncased')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# 定义函数入口

# cat input.json | faas invoke openbert
# echo {"body": "Hello, world!"}  | faas invoke openbert


def handle(req):
    # 获取输入的字符串
    input_text = req["body"]

    # 将输入的字符串分词并添加特殊标记
    input_tokens = tokenizer.encode(input_text, add_special_tokens=True)

    # 将分词后的列表转换为 PyTorch 张量
    input_tensor = torch.tensor([input_tokens])

    # 获取每个词的 BERT 编码
    with torch.no_grad():
        encoded_layers, _ = model(input_tensor)

    # 将编码后的张量转换为列表
    sentence_embedding = list(encoded_layers[0][0].numpy())

    # 构建返回的 JSON 对象
    result = {"embedding": sentence_embedding}

    # 返回 JSON 对象
    return json.dumps(result)
