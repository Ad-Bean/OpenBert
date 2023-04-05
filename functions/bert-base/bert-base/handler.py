import json
import torch
from transformers import pipeline, logging, BertModel, AutoTokenizer, BartForConditionalGeneration, BertForMaskedLM, BertForNextSentencePrediction

logging.set_verbosity_error()

model_name = 'bert-base-uncased'
# model_state_dict = torch.load('bert_model.pth')

tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = BertModel.from_pretrained(model_name, state_dict=model_state_dict)
model = BertModel.from_pretrained(model_name)

# modelNSP = BertForNextSentencePrediction.from_pretrained(
#     model_name, state_dict=model_state_dict)
modelNSP = BertForNextSentencePrediction.from_pretrained(
    model_name)


def handle(req):
    try:
        body = json.loads(req)
        type = body["type"]
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e.msg)
        return "failed to process the task"

    if type == "nsp":
        # pipeline does not have next sentence prediction task
        text_a = body["text_a"]
        text_b = body["text_b"]
        inputs = tokenizer(text_a, text_b, return_tensors='pt')
        outputs = modelNSP(**inputs)
        probability = torch.nn.functional.softmax(
            outputs.logits, dim=1)[0][0].item()
        res = {
            "text_a": text_a,
            "text_b": text_b,
            "probability": probability,
        }
        return json.dumps(res)
    elif type == "mask":
        text = body["text"]
        model_name = 'bert-base-uncased'
        unmasker = pipeline("fill-mask", model=model_name)
        ans = unmasker(text, top_k=1)
        res = {
            "text": text,
            "score": ans[0]["score"],
            "token_str": ans[0]["token_str"],
            "sequence": ans[0]["sequence"]
        }
        return json.dumps(res)
    elif type == "mask-imdb":
        text = body["text"]
        res = {
            "text": text,
            "model_name": "huggingface-course/distilbert-base-uncased-finetuned-imdb"
        }
        return json.dumps(res)
    elif type == "ner":
        text = body["text"]
        res = {
            "text": text,
            "model_name": "huggingface-course/bert-finetuned-ner"
        }
        return json.dumps(res)
    elif type == "qa":
        context = body["context"]
        question = body["question"]
        model_name = "huggingface-course/bert-finetuned-squad"
        res = {
            "context": context,
            "question": question,
            "model_name": "huggingface-course/bert-finetuned-squad"
        }
        return json.dumps(res)
    elif type == "sa":
        text = body["text"]
        model_name = 'nickwong64/bert-base-uncased-poems-sentiment'
        res = {
            "text": text,
            "model_name": model_name
        }
        return json.dumps(res)
    elif type == "sum":
        text = body["text"]
        model_name = 'Callidior/bert2bert-base-arxiv-titlegen'
        res = {
            "text": text,
            "model_name": model_name
        }
        return json.dumps(res)
    elif type == "key":
        text = body["text"]
        model_name = 'ml6team/keyphrase-extraction-distilbert-inspec'
        res = {
            "text": text,
            "model_name": model_name
        }
        return json.dumps(res)
    else:
        return "failed to process the task"
