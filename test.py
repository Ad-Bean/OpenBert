import json
import torch
from transformers import AutoTokenizer, BertForQuestionAnswering


model_name = "bert-finetuned-squad"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = BertForQuestionAnswering.from_pretrained(model_name)


def handle(req):
    body = json.loads(req)
    context = body["context"]
    question = body["question"]

    inputs = tokenizer(question, context, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)

    answer_start_index = outputs.start_logits.argmax()
    answer_end_index = outputs.end_logits.argmax()

    predict_answer_tokens = inputs.input_ids[0,
                                             answer_start_index: answer_end_index + 1]
    ans = tokenizer.decode(predict_answer_tokens, skip_special_tokens=True)

    target_start_index = torch.tensor([14])
    target_end_index = torch.tensor([15])

    outputs = model(**inputs, start_positions=target_start_index,
                    end_positions=target_end_index)
    loss = outputs.loss

    res = "问题：{}\n\n".format(question)
    res += "答案：{}\n".format(ans)
    res += "损失：{}\n".format(round(loss.item(), 2))

    return res


context = "Transformers is backed by the three most popular deep learning libraries — Jax, PyTorch and TensorFlow — with a seamless integration between them. It's straightforward to train your models with one before loading them for inference with the other."
question = "Which deep learning libraries back Transformers?"
