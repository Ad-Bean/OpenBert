deploy: 
	faas-cli build -f bert-mlm-imdb.yml 
	kind load docker-image bert-mlm-imdb:latest --name openfaas 
	faas-cli deploy -f bert-mlm-imdb.yml 
run: 
	cat input.json | faas invoke bert-base | faas invoke bert-mlm-imdb | faas invoke bert-mlm
