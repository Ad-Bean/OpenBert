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

mlm-imdb:
	cat mlm-imdb.json | faas-cli invoke bert-base | faas-cli invoke bert-mlm-imdb | faas-cli invoke bert-mlm

