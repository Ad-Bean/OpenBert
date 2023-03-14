import torch
from transformers import BertTokenizer, BertForNextSentencePrediction

model = BertForNextSentencePrediction.from_pretrained('bert-base-uncased')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def predict_nsp(text_a, text_b):
    # Tokenize
    inputs = tokenizer(text_a, text_b, return_tensors='pt')

    # Make a forward pass through the model
    outputs = model(**inputs)

    # Extract the probability that text_b follows text_a
    probability = torch.softmax(outputs.logits, dim=1)[0][0].item()

    return probability


# text_a = "I went to the store to buy some apples."
# text_b = "Then, I went home and made a pie."
# text1 = ("After Abraham Lincoln won the November 1860 presidential election on an "
#         "anti-slavery platform, an initial seven slave states declared their "
#         "secession from the country to form the Confederacy.")
# text2 = ("War broke out in April 1861 when secessionist forces attacked Fort "
#          "Sumter in South Carolina, just over a month after Lincoln's "
#          "inauguration.")

text_a = "The cat sat on the mat."
text_b = "It was a rainny day outside."
# text_a = "I went to the market yesterday and bought some apples."
# text_b = "I thought those apples were very tasty."
probability = predict_nsp(text_a, text_b)

print(f"The probability that text_b follows text_a is {probability:.2f}.")
