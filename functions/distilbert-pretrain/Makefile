deploy: 
	faas-cli build -f distilbert-pretrain.yml 
	kind load docker-image distilbert-pretrain:latest --name openfaas 
	faas-cli deploy -f distilbert-pretrain.yml 
run: 
	cat input.json | faas invoke bert-base | faas-cli invoke distilbert-pretrain
