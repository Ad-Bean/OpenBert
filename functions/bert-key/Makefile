deploy: 
	faas-cli build -f bert-key.yml 
	kind load docker-image bert-key:latest --name openfaas 
	faas-cli deploy -f bert-key.yml 
run: 
	cat input.json | faas invoke bert-base | faas-cli invoke bert-key
