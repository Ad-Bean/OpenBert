# import datasets
# from transformers import AutoTokenizer, AutoModelForQuestionAnswering, TrainingArguments, Trainer
# import torch

# # 加载数据集
# train_dataset = datasets.load_dataset('squad', split='train')
# eval_dataset = datasets.load_dataset('squad', split='validation')

# # 加载模型和分词器
# model_name = 'bert-base-uncased'
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForQuestionAnswering.from_pretrained(model_name)

# # 训练参数
# training_args = TrainingArguments(
#     output_dir='./results',
#     evaluation_strategy='steps',
#     eval_steps=500,
#     save_total_limit=3,
#     learning_rate=2e-5,
#     per_device_train_batch_size=16,
#     per_device_eval_batch_size=32,
#     num_train_epochs=3,
#     weight_decay=0.01,
#     push_to_hub=False,
# )

# # 定义训练函数
# def train_function(examples):
#     # 对数据进行编码
#     encoding = tokenizer(examples['question'], examples['context'], truncation=True, padding=True)
#     # 将答案标签添加到编码中
#     encoding['start_positions'] = examples['start_position']
#     encoding['end_positions'] = examples['end_position']
#     return encoding

# # 对数据集进行编码
# train_dataset = train_dataset.map(train_function, batched=True)
# eval_dataset = eval_dataset.map(train_function, batched=True)

# # 训练模型
# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=train_dataset,
#     eval_dataset=eval_dataset,
#     data_collator=lambda data: {'input_ids': data['input_ids'], 'attention_mask': data['attention_mask'],
#                                'start_positions': data['start_positions'], 'end_positions': data['end_positions']},
#     tokenizer=tokenizer,
# )

# trainer.train()

# # 加载模型和分词器
# model_name = 'bert-base-uncased'
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForQuestionAnswering.from_pretrained('./results/checkpoint-xxxxxx')

# # 提示用户输入问题和上下文
# question = input('请输入问题：')
# context = input('请输入上下文：')

# # 对问题和上下文进行编码
# inputs = tokenizer(question, context, return_tensors='pt')

# # 用模型回答问题
# outputs = model(**inputs)
# start_scores = outputs.start_logits
# end_scores = outputs.end_logits
# start_index = torch.argmax(start_scores)
# end_index = torch.argmax(end_scores) + 1
# answer_tokens = inputs['input_ids'][0][start_index:end_index]
# answer = tokenizer.decode(answer_tokens)

# # 打印答案
# print('答案：', answer)

# test = 0.5029111504554749 * 100

# print(f"{test:.2f} %")

import json


arr = [{'entity_group': 'PER', 'score': 0.9988506, 'word': 'Sylvain', 'start': 11, 'end': 18}, {'entity_group': 'ORG', 'score': 0.9647625,
                                                                                                'word': 'Hugging Face', 'start': 33, 'end': 45}, {'entity_group': 'LOC', 'score': 0.9986118, 'word': 'Brooklyn', 'start': 49, 'end': 57}]


def getType(word):
    if word == "PER":
        return "人名"
    elif word == "ORG":
        return "组织"
    elif word == "LOC":
        return "地点"
    else:
        return word


res = ""

for n in arr:
    # temp = {
    #     "entity_group": getType(n["entity_group"]),
    #     "score": n["score"],
    #     "word": n["word"]
    # }
    # res.append(temp)
    res += "类型：{}\n".format(getType(n["entity_group"]))
    res += "单词：{}\n".format(n["word"])
    res += "得分：{}\n\n".format(n["score"])

print(res)
