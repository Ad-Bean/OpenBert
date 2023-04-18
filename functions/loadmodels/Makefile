deploy: 
	faas-cli build -f loadmodels.yml 
	kind load docker-image loadmodels:latest --name openfaas 
	faas-cli deploy -f loadmodels.yml 
run: 
	cat input.json | faas-cli invoke loadmodels
