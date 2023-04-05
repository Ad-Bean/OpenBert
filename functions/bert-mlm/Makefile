deploy:
	faas-cli build -f bert-mlm.yml
	kind load docker-image bert-mlm:latest --name openfaas
	faas-cli deploy -f bert-mlm.yml

run:
	cat input.json | faas-cli invoke bert-base | faas-cli invoke bert-mlm
