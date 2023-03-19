import json


def handle(req):
    body = json.loads(req)
    text = body["text"]
    score = body["score"]
    token_str = body["token_str"]
    sequence = body["sequence"]

    ans = "输入句子：{}\n预测单词：{}\n得分：{}\n预测结果：{}".format(
        text, token_str, score, sequence)
    return ans
