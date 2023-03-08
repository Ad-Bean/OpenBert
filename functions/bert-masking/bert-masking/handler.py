

import json
from models import MaskLM
import torch

vocab_size, num_hiddens, ffn_num_hiddens, num_heads = 10000, 768, 1024, 4
model = MaskLM(vocab_size, num_hiddens, num_inputs=768)


def get_tokens_and_segments(tokens_a, tokens_b=None):
    tokens = ['<cls>'] + tokens_a + ['<sep>']
    # 0和1分别标记片段A和B
    segments = [0] * (len(tokens_a) + 2)
    if tokens_b is not None:
        tokens += tokens_b + ['<sep>']
        segments += [1] * (len(tokens_b) + 1)
    return tokens, segments


def mask_language(input_sequence, mask_position, model):
    tokens = input_sequence.split()
    input_tensor = torch.tensor(
        [[token_id for token_id, _ in enumerate(tokens)]], dtype=torch.long)
    prediction_positions = torch.tensor([[mask_position]], dtype=torch.long)

    predictions = model(input_tensor, prediction_positions)

    num_predictions = 5
    predicted_word_ids = predictions[0][0].topk(
        num_predictions).indices.tolist()
    predicted_words = [tokens[word_id] for word_id in predicted_word_ids]
    print(f"Top {num_predictions} predicted words: {predicted_words}")

    # 返回预测的目标词汇的概率分布列表
    return predicted_words


input_sequence = "The quick ### fox jumps over the lazy dog"
mask_position = 3

answer = mask_language(input_sequence, mask_position, model)

# def handle(req):
#     try:
#         # loads the incoming event into a dictonary
#         body = json.loads(req)
#         # uses the pipeline to predict the answer
#         answer = mask_language(
#             input_sequence=body['input_sequence'], mask_position=body['mask_position'])
#         return {
#             "statusCode": 200,
#             "headers": {
#                 'Content-Type': 'application/json',
#                 'Access-Control-Allow-Origin': '*',
#                 "Access-Control-Allow-Credentials": True
#             },
#             "body": json.dumps({'answer': answer})
#         }
#     except Exception as e:
#         print(repr(e))
#         return {
#             "statusCode": 500,
#             "headers": {
#                 'Content-Type': 'application/json',
#                 'Access-Control-Allow-Origin': '*',
#                 "Access-Control-Allow-Credentials": True
#             },
#             "body": json.dumps({"error": repr(e)})
#         }
