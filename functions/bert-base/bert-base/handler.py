import json
import torch
from transformers import pipeline, logging, BertModel, AutoTokenizer, BartForConditionalGeneration, BertForMaskedLM, BertForNextSentencePrediction

logging.set_verbosity_error()

model_name = 'bert-base-uncased'
model_state_dict = torch.load('bert_model.pth')

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name, state_dict=model_state_dict)

modelNSP = BertForNextSentencePrediction.from_pretrained(
    model_name, state_dict=model_state_dict)
modelMLM = BertForMaskedLM.from_pretrained(
    model_name, state_dict=model_state_dict)
modelCG = BartForConditionalGeneration.from_pretrained(
    model_name, state_dict=model_state_dict)


def handle(req):
    body = json.loads(req)
    type = body["type"]
    if type == "nsp":
        # pipeline does not have next sentence prediction task
        text_a = body["text_a"]
        text_b = body["text_b"]
        inputs = tokenizer(text_a, text_b, return_tensors='pt')
        outputs = modelNSP(**inputs)
        probability = torch.softmax(outputs.logits, dim=1)[0][0].item()

        res = {
            "text_a": text_a,
            "text_b": text_b,
            "probability": probability
        }
        return json.dumps(res)
    elif type == "mask":
        text = body["text"]
        unmasker = pipeline("fill-mask", model=model_name)
        ans = unmasker(text, top_k=1)
        res = {
            "text": text,
            "score": ans[0]["score"],
            "token_str": ans[0]["token_str"],
            "sequence": ans[0]["sequence"]
        }
        return json.dumps(res)

        # text = body["text"]
        # tokens = tokenizer.tokenize(text)
        # masked_indices = [i for i, x in enumerate(tokens) if x == '[MASK]']
        # input_ids = tokenizer.convert_tokens_to_ids(tokens)
        # input_tensor = torch.tensor([input_ids])
        # with torch.no_grad():
        #     outputs = modelMLM(input_tensor)
        #     logits = outputs[0]

        # masked_logits = logits[0, masked_indices]
        # probs = torch.softmax(masked_logits, dim=1)
        # predicted_ids = torch.argmax(probs, dim=1)
        # predicted_probs = torch.max(probs, dim=1).values
        # predicted_tokens = tokenizer.convert_ids_to_tokens(predicted_ids)
        # res = []
        # for i in range(len(masked_indices)):
        #     print('Masked token:', tokens[masked_indices[i]])
        #     print('Predicted token:', predicted_tokens[i])
        #     print('Probability:', predicted_probs[i].item())
        #     print('----------------------')
        #     res.append({
        #         "masked_token": tokens[masked_indices[i]],
        #         "predicted_token": predicted_tokens[i],
        #         "probability": predicted_probs[i].item(),
        #     })
        # return res
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

        # # Define text and tokenize it
        # inputs = tokenizer(text, return_tensors='pt')
        # with torch.no_grad():
        #     logits = modelMLM(**inputs).logits

        # mask_token_index = (inputs.input_ids == tokenizer.mask_token_id)[
        #     0].nonzero(as_tuple=True)[0]

        # predicted_token_id = logits[0, mask_token_index].argmax(axis=-1)
        # predicted = tokenizer.decode(predicted_token_id)

        # print(predicted)
        # text = "Hello I'm a [MASK] model."
        # text = "The capital of France is [MASK]."
        # text = "The quick brown fox jumps over the [MASK] dog."
        # text = "The multiline prop transforms the text field into a TextareaAutosize element. Unless the rows prop is set, the height of the text field dynamically matches its content(using TextareaAutosize). You can use the minRows and maxRows props to bound it."
        # unmasker = pipeline('summarization', model=model_name)
        # ans = unmasker(text)
        # print(ans)

        # Not for Bert
        # generator = pipeline("text-generation", model=model_name)
        # ans = generator("In this course, we will teach you how to",
        #                 max_length=30,
        #                 num_return_sequences=1)
        # print(ans)
        # for dict_ in ans:
        # print('score {}'.format(dict_['score']))
        # print('token {}'.format(dict_['token']))
        # print('{}'.format(dict_['token_str']))
        # print('{}'.format(dict_['sequence']))

        # NER Named entity recognition

        # ner = pipeline("ner", model=model_name)
        # ans = ner("I love this great movie")

        # print(ans)
        # for aaa in ans:
        #     print('entity: {}'.format(aaa['entity']))
        #     print('word: {}'.format(aaa['word']))
        #     print('')
