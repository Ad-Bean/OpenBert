deploy: 
	faas-cli build -f torch-test.yml 
	kind load docker-image torch-test:latest --name openfaas 
	faas-cli deploy -f torch-test.yml 
run: 
	cat input.json | faas invoke bert-base | faas-cli invoke torch-test
