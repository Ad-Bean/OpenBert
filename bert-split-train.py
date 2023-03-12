from transformers import BertTokenizer, BertForSequenceClassification
import torch
import numpy as np

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained(
    'bert-base-uncased', num_labels=2)


def prepare_input(sentences):
    input_ids = []
    attention_masks = []

    for sentence in sentences:
        encoded_dict = tokenizer.encode_plus(
            sentence,
            add_special_tokens=True,
            max_length=64,
            pad_to_max_length=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        input_ids.append(encoded_dict['input_ids'])
        attention_masks.append(encoded_dict['attention_mask'])

    input_ids = torch.cat(input_ids, dim=0)
    attention_masks = torch.cat(attention_masks, dim=0)

    return input_ids, attention_masks


def train_model(train_dataloader):
    model.train()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)

    for epoch in range(5):
        print(f'Epoch {epoch + 1}/{5}')
        for step, batch in enumerate(train_dataloader):
            input_ids = batch[0].to(device)
            attention_mask = batch[1].to(device)
            labels = batch[2].to(device)

            model.zero_grad()

            outputs = model(input_ids,
                            attention_mask=attention_mask,
                            labels=labels)

            loss = outputs.loss
            logits = outputs.logits

            loss.backward()
            optimizer.step()

            if step % 20 == 0:
                print(
                    f'Step {step}/{len(train_dataloader)}: Loss: {loss.item()}')

    return model


def predict(sentences):
    input_ids, attention_masks = prepare_input(sentences)
    input_ids = input_ids.to(device)
    attention_masks = attention_masks.to(device)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_masks)

    logits = outputs.logits
    probs = torch.softmax(logits, dim=1).detach().cpu().numpy()
    preds = np.argmax(probs, axis=1)

    return preds


device = torch.device(
    'cuda') if torch.cuda.is_available() else torch.device('cpu')
train_sentences = ["I really enjoyed this movie.", "This movie was great!",
                   "I hated this movie.", "This movie was terrible."]
train_labels = [1, 1, 0, 0]

input_ids, attention_masks = prepare_input(train_sentences)
labels = torch.tensor(train_labels)

train_dataset = torch.utils.data.TensorDataset(
    input_ids, attention_masks, labels)
train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=32)

model = train_model(train_dataloader)

sentence1 = "I love this movie!"
sentence2 = "This movie is terrible."

sentences = [sentence1, sentence2]
preds = predict(sentences)

for sentence, pred in zip(sentences, preds):
    if pred == 1:
        print(f'{sentence} is positive.')
    else:
        print(f'{sentence} is negative.')
