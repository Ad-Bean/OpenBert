deploy: 
	faas-cli build -f bert-ner.yml 
	kind load docker-image bert-ner:latest --name openfaas 
	faas-cli deploy -f bert-ner.yml 
run: 
	cat input.json | faas invoke bert-base | faas-cli invoke bert-ner
