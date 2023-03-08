
import torch

from Bert.Bert import NextSentencePred


def mask_language(input_sequence, mask_position, model):
    # 将输入序列和需要被遮蔽的位置创建为torch张量
    input_tensor = torch.tensor(input_sequence).unsqueeze(0)
    mask_position_tensor = torch.tensor([mask_position])

    # 使用模型进行遮蔽语言建模
    predictions = model(input_tensor, mask_position_tensor)

    # 获取预测结果中预测的目标单词的概率分布
    target_word_prob = predictions.squeeze()[mask_position]

    # 返回预测的目标单词的概率分布列表
    return target_word_prob.tolist()


model = NextSentencePred()


def mask_language(input_sequence, mask_position, model):
    # 将输入序列和需要被遮蔽的位置创建为torch张量
    input_tensor = torch.tensor(input_sequence).unsqueeze(0)
    mask_position_tensor = torch.tensor([mask_position])

    # 使用模型进行遮蔽语言建模
    predictions = model(input_tensor, mask_position_tensor)

    # 获取预测结果中预测的目标单词的概率分布
    target_word_prob = predictions.squeeze()[mask_position]

    # 返回预测的目标词汇的概率分布列表
    return target_word_prob


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    return req
