import random
import uuid
import requests
import torch
from minio import Minio

from transformers import pipeline, set_seed, AutoTokenizer, AutoModelForCausalLM


model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


prompt = "Hey, are you conscious? Can you talk to me?"
generator = pipeline('text-generation', model=model_name)
set_seed(random.randint(1, 100))

output_text = generator(prompt, max_length=20, num_return_sequences=5)

for text in output_text:
    print(text)

directory = r'./models'
model.save_pretrained(directory)
tokenizer.save_pretrained(directory)

# bucket_name = "models"
# object_name = "bert-base-uncased"
# file_path = "models/bert_model.pth"

# torch.save(model.state_dict(), file_path)
# tokenizer.save_pretrained('models/bert_tokenizer')

#   minio_hostname: "10.96.130.15:9000"
#   minio_access_key: "Q0gVceW8HnRSangH"
#   minio_secret_key: "sLGnsAUHZBLESaFbEnMd4PakrJIpvkGF"
# mc = Minio(endpoint="10.96.130.15:9000",
#            access_key="Q0gVceW8HnRSangH",
#            secret_key="sLGnsAUHZBLESaFbEnMd4PakrJIpvkGF",
#            secure=False)

# mc.fput_object(bucket_name, object_name, file_path)
# print("文件上传成功！")


# def get_temp_file():
#     uuid_value = str(uuid.uuid4())
#     return uuid_value


# r = requests.get(
#     "https://images.pexels.com/photos/72161/pexels-photo-72161.jpeg?dl&fit=crop&w=640&h=318")

# # write to temporary file
# file_name = get_temp_file()
# f = open("/tmp/" + file_name, "wb")
# f.write(r.content)
# f.close()

# # sync to Minio
# mc.fput_object("incoming", file_name, "/tmp/"+file_name)
