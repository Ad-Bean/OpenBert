

import json
from torch import nn
from d2l import torch as d2l
from models import MaskLM
import torch


def _get_batch_loss_bert(net, loss, vocab_size, tokens_X,
                         segments_X, valid_lens_x,
                         pred_positions_X, mlm_weights_X,
                         mlm_Y, nsp_y):
    # 前向传播
    _, mlm_Y_hat, nsp_Y_hat = net(tokens_X, segments_X,
                                  valid_lens_x.reshape(-1),
                                  pred_positions_X)
    # 计算遮蔽语言模型损失
    mlm_l = loss(mlm_Y_hat.reshape(-1, vocab_size), mlm_Y.reshape(-1)) *\
        mlm_weights_X.reshape(-1, 1)
    mlm_l = mlm_l.sum() / (mlm_weights_X.sum() + 1e-8)
    # 计算下一句子预测任务的损失
    nsp_l = loss(nsp_Y_hat, nsp_y)
    l = mlm_l + nsp_l
    return mlm_l, nsp_l, l


def train_bert(train_iter, net, loss, vocab_size, devices, num_steps):
    net = nn.DataParallel(net, device_ids=devices).to(devices[0])
    trainer = torch.optim.Adam(net.parameters(), lr=0.01)
    step, timer = 0, d2l.Timer()
    animator = d2l.Animator(xlabel='step', ylabel='loss',
                            xlim=[1, num_steps], legend=['mlm', 'nsp'])
    # 遮蔽语言模型损失的和，下一句预测任务损失的和，句子对的数量，计数
    metric = d2l.Accumulator(4)
    num_steps_reached = False
    while step < num_steps and not num_steps_reached:
        for tokens_X, segments_X, valid_lens_x, pred_positions_X,\
                mlm_weights_X, mlm_Y, nsp_y in train_iter:
            tokens_X = tokens_X.to(devices[0])
            segments_X = segments_X.to(devices[0])
            valid_lens_x = valid_lens_x.to(devices[0])
            pred_positions_X = pred_positions_X.to(devices[0])
            mlm_weights_X = mlm_weights_X.to(devices[0])
            mlm_Y, nsp_y = mlm_Y.to(devices[0]), nsp_y.to(devices[0])
            trainer.zero_grad()
            timer.start()
            mlm_l, nsp_l, l = _get_batch_loss_bert(
                net, loss, vocab_size, tokens_X, segments_X, valid_lens_x,
                pred_positions_X, mlm_weights_X, mlm_Y, nsp_y)
            l.backward()
            trainer.step()
            metric.add(mlm_l, nsp_l, tokens_X.shape[0], 1)
            timer.stop()
            animator.add(step + 1,
                         (metric[0] / metric[3], metric[1] / metric[3]))
            step += 1
            if step == num_steps:
                num_steps_reached = True
                break

    print(f'MLM loss {metric[0] / metric[3]:.3f}, '
          f'NSP loss {metric[1] / metric[3]:.3f}')
    print(f'{metric[2] / timer.sum():.1f} sentence pairs/sec on '
          f'{str(devices)}')


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


# train_bert(train_iter, net, loss, len(vocab), devices, 50)

# answer = mask_language(input_sequence, mask_position, model)

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
