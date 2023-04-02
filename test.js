const payload = {
  "type": "qa",
  "context": "Transformers is backed by the three most popular deep learning libraries — Jax, PyTorch and TensorFlow — with a seamless integration between them. It's straightforward to train your models with one before loading them for inference with the other.",
  "question": "Which deep learning libraries back Transformers?",
  "model_name": "huggingface-course/bert-finetuned-squad"
}

const URL = "http://127.0.0.1:31112/function/"

fetch(URL + "bert-base", {
  method: "POST",
  body: JSON.stringify(payload),
})
  .then((res) => res.json())
  .then((res) => {
    fetch(URL + "bert-qa", {
      method: "POST",
      body: JSON.stringify(payload),
    }).then(res => res.text()).then(res => console.log(res))
  });
