deploy: 
	faas-cli build -f distilbert-base.yml 
	kind load docker-image distilbert-base:latest --name openfaas 
	faas-cli deploy -f distilbert-base.yml 
run: 
	cat input.json | faas invoke bert-base | faas-cli invoke distilbert-base
