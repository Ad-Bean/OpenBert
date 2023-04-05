import json
import math
from transformers import logging, AutoModel, AutoModelForMaskedLM, AutoTokenizer, DataCollatorForLanguageModeling, TrainingArguments, Trainer, default_data_collator
from datasets import load_dataset
import collections
import numpy as np
from huggingface_hub import login

logging.set_verbosity_error()
wwm_probability = 0.2
model_name = 'distilbert-base-uncased'
# model = AutoModel.from_pretrained(model_name)
model = AutoModelForMaskedLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

#
chunk_size = 128


def whole_word_masking_data_collator(features):
    for feature in features:
        word_ids = feature.pop("word_ids")

        # Create a map between words and corresponding token indices
        mapping = collections.defaultdict(list)
        current_word_index = -1
        current_word = None
        for idx, word_id in enumerate(word_ids):
            if word_id is not None:
                if word_id != current_word:
                    current_word = word_id
                    current_word_index += 1
                mapping[current_word_index].append(idx)

        # Randomly mask words
        mask = np.random.binomial(1, wwm_probability, (len(mapping),))
        input_ids = feature["input_ids"]
        labels = feature["labels"]
        new_labels = [-100] * len(labels)
        for word_id in np.where(mask)[0]:
            word_id = word_id.item()
            for idx in mapping[word_id]:
                new_labels[idx] = labels[idx]
                input_ids[idx] = tokenizer.mask_token_id
        feature["labels"] = new_labels

    return default_data_collator(features)


def tokenize_function(examples):
    result = tokenizer(examples["text"])
    if tokenizer.is_fast:
        result["word_ids"] = [result.word_ids(
            i) for i in range(len(result["input_ids"]))]
    return result


def group_texts(examples):
    # Concatenate all texts
    concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
    # Compute length of concatenated texts
    total_length = len(concatenated_examples[list(examples.keys())[0]])
    # We drop the last chunk if it's smaller than chunk_size
    total_length = (total_length // chunk_size) * chunk_size
    # Split by chunks of max_len
    result = {
        k: [t[i: i + chunk_size] for i in range(0, total_length, chunk_size)]
        for k, t in concatenated_examples.items()
    }
    # Create a new labels column
    result["labels"] = result["input_ids"].copy()
    return result


def handle(req):
    try:
        body = json.loads(req)
        secret = body["secret"]
        type = body["type"]
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e.msg)

    login(secret)

    if type == "pretrain":
        datasets = body["datasets"]
        imdb_dataset = load_dataset(datasets)
        tokenized_datasets = imdb_dataset.map(
            tokenize_function, batched=True, remove_columns=["text", "label"])
        #
        tokenized_samples = tokenized_datasets["train"][:3]
        #
        concatenated_examples = {
            k: sum(tokenized_samples[k], []) for k in tokenized_samples.keys()}
        total_length = len(concatenated_examples["input_ids"])
        #
        chunk_size = body["chunk_size"]
        chunks = {k: [t[i: i + chunk_size]
                      for i in range(0, total_length, chunk_size)] for k, t in concatenated_examples.items()}

        #
        lm_datasets = tokenized_datasets.map(group_texts, batched=True)

        #
        samples = [lm_datasets["train"][i] for i in range(2)]
        for sample in samples:
            _ = sample.pop("word_ids")
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer, mlm_probability=0.15)

        for chunk in data_collator(samples)["input_ids"]:
            print(f"\n'>>> {tokenizer.decode(chunk)}'")
        #
        samples = [lm_datasets["train"][i] for i in range(2)]
        batch = whole_word_masking_data_collator(samples)
        #
        train_size = 10_000
        test_size = int(0.1 * train_size)

        downsampled_dataset = lm_datasets["train"].train_test_split(
            train_size=train_size, test_size=test_size, seed=42
        )
        batch_size = 64

        # Show the training loss with every epoch
        logging_steps = len(downsampled_dataset["train"]) // batch_size

        training_args = TrainingArguments(
            output_dir=f"{model_name}-finetuned-imdb",
            overwrite_output_dir=True,
            evaluation_strategy="epoch",
            learning_rate=2e-5,
            weight_decay=0.01,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            push_to_hub=True,
            fp16=True,
            logging_steps=logging_steps,
        )
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=downsampled_dataset["train"],
            eval_dataset=downsampled_dataset["test"],
            data_collator=data_collator,
            tokenizer=tokenizer,
        )
        eval_results = trainer.evaluate()
        print(f">>> Perplexity: {math.exp(eval_results['eval_loss']):.2f}")

        trainer.train()

        eval_results = trainer.evaluate()
        print(f">>> Perplexity: {math.exp(eval_results['eval_loss']):.2f}")
        
        trainer.push_to_hub()

    return req
