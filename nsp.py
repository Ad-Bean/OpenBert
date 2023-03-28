# import torch
# from transformers import BertTokenizer, BertForNextSentencePrediction

# model = BertForNextSentencePrediction.from_pretrained('bert-base-uncased')
# tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# def predict_nsp(text_a, text_b):
#     # Tokenize
#     inputs = tokenizer(text_a, text_b, return_tensors='pt')

#     # Make a forward pass through the model
#     outputs = model(**inputs)

#     # Extract the probability that text_b follows text_a
#     probability = torch.softmax(outputs.logits, dim=1)[0][0].item()

#     return probability


# # text_a = "I went to the store to buy some apples."
# # text_b = "Then, I went home and made a pie."
# # text1 = ("After Abraham Lincoln won the November 1860 presidential election on an "
# #         "anti-slavery platform, an initial seven slave states declared their "
# #         "secession from the country to form the Confederacy.")
# # text2 = ("War broke out in April 1861 when secessionist forces attacked Fort "
# #          "Sumter in South Carolina, just over a month after Lincoln's "
# #          "inauguration.")

# text_a = "The cat sat on the mat."
# text_b = "It was a rainny day outside."
# # text_a = "I went to the market yesterday and bought some apples."
# # text_b = "I thought those apples were very tasty."
# probability = predict_nsp(text_a, text_b)

# print(f"The probability that text_b follows text_a is {probability:.2f}.")

class Model:
    def __init__(self, name, description):
        self.name = name
        self.description = description


models = [
    Model("bert-base",
          '''
说明：BERT 是一个经过自监督的大型英语数据库预训练 Transformers 模型。其预先训练了两个目标：语言遮蔽模型，下一句预测模型

使用方法：输入不同的 task 执行或分发不同的任务，如 
    nsp 进行预测两句是否互相跟随
    mask 进行语言遮蔽预测
    mask-imdb 进行在 imdb 数据集上微调和遮蔽预测
    ner 进行命名实体识别
    qa 进行对输入上下文做问答
    sa 进行对输入句子情感分析
    sum 进行对输入句子做摘要
    key 进行对输入句子做关键词提取
    
输入样例: 
{
  'type':'mask',
  'text':'The [MASK] is a large animal that lives in the ocean.'
}
''')
]


print(models[0].description)
