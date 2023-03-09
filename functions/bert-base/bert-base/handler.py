import json

import torch
from d2l import torch as d2l
from models import BERTModel

# https://colab.research.google.com/github/d2l-ai/d2l-zh-pytorch-colab/blob/master/chapter_natural-language-processing-pretraining/bert-pretraining.ipynb#scrollTo=300481a6
# base model
batch_size, max_len = 512, 64
train_iter, vocab = d2l.load_data_wiki(batch_size, max_len)

vocab_size = len(vocab)
devices = d2l.try_all_gpus()
model = BERTModel(vocab_size, num_hiddens=128, norm_shape=[128],
                  ffn_num_input=128, ffn_num_hiddens=256, num_heads=2,
                  num_layers=2, dropout=0.2, key_size=128, query_size=128,
                  value_size=128, hid_in_features=128, mlm_in_features=128,
                  nsp_in_features=128)


def get_bert_encoding(net, tokens_a, tokens_b=None):
    tokens, segments = d2l.get_tokens_and_segments(tokens_a, tokens_b)
    token_ids = torch.tensor(vocab[tokens], device=devices[0]).unsqueeze(0)
    segments = torch.tensor(segments, device=devices[0]).unsqueeze(0)
    valid_len = torch.tensor(len(tokens), device=devices[0]).unsqueeze(0)
    encoded_X = net(token_ids, segments, valid_len)
    return encoded_X


# input_sequence = " The quick ### fox jumps over the lazy dog"
# mask_position = 2

# tokens_a = input_sequence.split()
# encoded_X = get_bert_encoding(model, tokens_a)
# print(encoded_X)


def handle(req):
    try:
        body = json.loads(req)

        if body["type"] == "mask":
            tokens_a = body["input_sequenc"].split()
            encoded_X = get_bert_encoding(model, tokens_a)
            ans = encoded_X
        elif body["type"] == "next":
            ans = 'Not implemented yet'
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps({'answer': ans})
        }
    except Exception as e:
        print(repr(e))
        return {
            "statusCode": 500,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps({"error": repr(e)})
        }
