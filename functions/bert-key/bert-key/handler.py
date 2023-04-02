import json
from transformers import (
    TokenClassificationPipeline,
    AutoModelForTokenClassification,
    AutoTokenizer,
    logging
)
from transformers.pipelines import AggregationStrategy
import numpy as np

logging.set_verbosity_error()


class KeyphraseExtractionPipeline(TokenClassificationPipeline):
    def __init__(self, model, *args, **kwargs):
        super().__init__(
            model=AutoModelForTokenClassification.from_pretrained(model),
            tokenizer=AutoTokenizer.from_pretrained(model),
            *args,
            **kwargs
        )

    def postprocess(self, model_outputs):
        results = super().postprocess(
            model_outputs=model_outputs,
            aggregation_strategy=AggregationStrategy.FIRST,
        )
        return np.unique([result.get("word").strip() for result in results])


model_name = "ml6team/keyphrase-extraction-distilbert-inspec"
extractor = KeyphraseExtractionPipeline(model=model_name)


def handle(req):
    body = json.loads(req)
    text = body["text"].replace("\n", " ")
    # model_name = "ml6team/keyphrase-extraction-distilbert-inspec"

    keyphrases = extractor(text)
    res = "\n输入段落：{}\n\n".format(body["text"])
    res += "关键词：{}\n".format(', '.join(keyphrases))
    return res
