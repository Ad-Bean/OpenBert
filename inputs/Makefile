all: mlm mlm-imdb nsp qa sa ner key 

tasks: qa sa ner key sum

mlm:
	cat mlm.json | faas-cli invoke distilbert-base | faas-cil invoke bert-mlm-imdb | faas-cli invoke bert-mlm

nsp:
	cat nsp.json | faas-cli invoke bert-base | faas-cli invoke bert-nsp
	
qa:
	cat qa.json | faas-cli invoke bert-base | faas-cli invoke bert-qa

sa:
	cat sa.json | faas-cli invoke bert-base | faas-cli invoke bert-sa

ner:
	cat ner.json | faas-cli invoke bert-base | faas-cli invoke bert-ner

key:
	cat key.json | faas-cli invoke bert-base | faas-cli invoke bert-key 

sum:
	cat sum.json | faas-cli invoke bert-base | faas-cli invoke bert-sum 

mlm-imdb:
	cat mlm-imdb.json | faas-cli invoke bert-base | faas-cli invoke bert-mlm-imdb | faas-cli invoke bert-mlm



performance: qa-t sa-t ner-t key-t sum-t

qa-t:
	cat qa.json | httpstat $(OPENFAAS_URL)/function/bert-qa -X POST -H "Content-Type: application/json" -d @- | grep total
sa-t:
	cat sa.json | httpstat $(OPENFAAS_URL)/function/bert-sa -X POST -H "Content-Type: application/json" -d @- | grep total
ner-t:
	cat ner.json | httpstat $(OPENFAAS_URL)/function/bert-ner -X POST -H "Content-Type: application/json" -d @- | grep total
key-t:
	cat key.json | httpstat $(OPENFAAS_URL)/function/bert-key -X POST -H "Content-Type: application/json" -d @- | grep total
sum-t:
	cat sum.json | httpstat $(OPENFAAS_URL)/function/bert-sum -X POST -H "Content-Type: application/json" -d @- | grep total