import json


def handle(req):
    body = json.loads(req)
    text_a = body["text_a"]
    text_b = body["text_b"]
    prob = float(body["probability"]) * 100
    ans = "第一句：{}\n第二句：{}\n第二句是第一句话的下一句的概率为：{:.2f}%.".format(
        text_a, text_b, prob)
    return ans
