deploy: 
	faas-cli build -f bert-sum.yml 
	kind load docker-image bert-sum:latest --name openfaas 
	faas-cli deploy -f bert-sum.yml 
run: 
	cat input.json | faas-cli invoke bert-sum
