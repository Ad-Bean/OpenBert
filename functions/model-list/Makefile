deploy: 
	faas-cli build -f model-list.yml 
	kind load docker-image model-list:latest --name openfaas 
	faas-cli deploy -f model-list.yml 
run: 
	cat input.json | faas-cli invoke model-list
