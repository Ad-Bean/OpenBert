deploy: 
	faas-cli build -f distilbert-pretrain.yml 
	kind load docker-image distilbert-pretrain:latest --name openfaas 
	faas-cli deploy -f distilbert-pretrain.yml 
run: 
	cat pretrain.json | faas-cli invoke distilbert-pretrain

pretrain:
	cat pretrain.json | faas-cli invoke distilbert-pretrain