deploy:
	faas-cli build -f bert-base.yml
	kind load docker-image bert-base:latest --name openfaas
	faas-cli deploy -f bert-base.yml

run:
	cat input.json | faas-cli invoke bert-base
