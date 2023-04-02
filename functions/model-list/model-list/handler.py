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
'''),
    Model("bert-key",
          '''
说明：关键词提取是文本分析中的一种技术，可以从文档中提取重要的关键词。该模型基于 distilbert 和 inspec 数据集微调。
    
输入样例: 
{
    "type":"key",
    "text": "In this work, we explore how to learn task specific language models aimed towards learning rich representation of keyphrases from text documents. We experiment with different masking strategies for pre-training transformer language models (LMs) in discriminative as well as generative settings. In the discriminative setting, we introduce a new pre-training objective - Keyphrase Boundary Infilling with Replacement (KBIR), showing large gains in performance (up to 9.26 points in F1) over SOTA, when LM pre-trained using KBIR is fine-tuned for the task of keyphrase extraction. In the generative setting, we introduce a new pre-training setup for BART - KeyBART, that reproduces the keyphrases related to the input text in the CatSeq format, instead of the denoised original input. This also led to gains in performance (up to 4.33 points inF1@M) over SOTA for keyphrase generation. Additionally, we also fine-tune the pre-trained language models on named entity recognition(NER), question answering (QA), relation extraction (RE), abstractive summarization and achieve comparable performance with that of the SOTA, showing that learning rich representation of keyphrases is indeed beneficial for many other fundamental NLP tasks."
}
'''),
    Model("bert-mlm",
          '''
说明：BERT 是一个经过自监督的大型英语数据库预训练 Transformers 模型。其预先训练了两个目标：语言遮蔽模型

输入样例: 
{
  "type": "mask",
  "text": "The capital of China is [MASK]"
}
'''),
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
'''),
]


def handle(req):
    for model in models:
        print('函数：{}\n说明：{}\n'.format(model.name, model.description))
    return req
