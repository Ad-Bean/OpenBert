from transformers import pipeline
import json
import torch
from transformers import logging, BertModel, AutoTokenizer, BertForMaskedLM, BertForNextSentencePrediction

logging.set_verbosity_error()

model_name = 'bert-large-uncased'
model_state_dict = torch.load('bert_model.pth')

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name, state_dict=model_state_dict)

modelNSP = BertForNextSentencePrediction.from_pretrained(
    model_name, state_dict=model_state_dict)
modelMLM = BertForMaskedLM.from_pretrained(
    model_name, state_dict=model_state_dict)


def handle(req):
    body = json.loads(req)
    type = body["type"]
    if type == "nsp":
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
        tokens = tokenizer.tokenize(text)
        masked_indices = [i for i, x in enumerate(tokens) if x == '[MASK]']
        input_ids = tokenizer.convert_tokens_to_ids(tokens)
        input_tensor = torch.tensor([input_ids])
        with torch.no_grad():
            outputs = modelMLM(input_tensor)
            logits = outputs[0]

        masked_logits = logits[0, masked_indices]
        probs = torch.softmax(masked_logits, dim=1)
        predicted_ids = torch.argmax(probs, dim=1)
        predicted_probs = torch.max(probs, dim=1).values
        predicted_tokens = tokenizer.convert_ids_to_tokens(predicted_ids)
        res = []
        for i in range(len(masked_indices)):
            print('Masked token:', tokens[masked_indices[i]])
            print('Predicted token:', predicted_tokens[i])
            print('Probability:', predicted_probs[i].item())
            print('----------------------')
            res.append({
                "masked_token": tokens[masked_indices[i]],
                "predicted_token": predicted_tokens[i],
                "probability": predicted_probs[i].item(),
            })
        return res


tokenizer = AutoTokenizer.from_pretrained(model_name)
model = BertForMaskedLM.from_pretrained(model_name)

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
text = "The quick brown fox jumps over the [MASK] dog."
unmasker = pipeline('fill-mask', model='bert-base-uncased')
ans = unmasker(text)
print(ans)
