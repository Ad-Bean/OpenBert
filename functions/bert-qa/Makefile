deploy: 
	faas-cli build -f bert-qa.yml 
	kind load docker-image bert-qa:latest --name openfaas 
	faas-cli deploy -f bert-qa.yml 
run: 
	cat input.json | faas invoke bert-base | faas-cli invoke bert-qa
