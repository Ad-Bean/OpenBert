deploy: 
	faas-cli build -f bert-sa.yml 
	kind load docker-image bert-sa:latest --name openfaas 
	faas-cli deploy -f bert-sa.yml 
run: 
	cat input.json | faas invoke bert-base | faas-cli invoke bert-sa
