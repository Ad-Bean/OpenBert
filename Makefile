create-py:
	cd functions && mkdir -p $(name)
	cd functions/$(name) && faas-cli new --lang python $(name)
	cd functions/$(name) && touch Makefile 
	echo "deploy: \n	faas-cli build -f $(name).yml \n	kind load docker-image $(name):latest --name openfaas \n	faas-cli deploy -f $(name).yml \nrun: \n	cat input.json | faas invoke bert-base | faas-cli invoke $(name)" > functions/$(name)/Makefile

create-py3:
	cd functions && mkdir -p $(name)
	cd functions/$(name) && faas-cli new --lang python3 $(name)
	cd functions/$(name) && 
	echo "deploy: \n	faas-cli build -f $(name).yml \n	kind load docker-image $(name):latest --name openfaas \n	faas-cli deploy -f $(name).yml \nrun: \n	cat input.json | faas invoke bert-base | faas-cli invoke $(name)" > functions/$(name)/Makefile

create-torch:
	cd functions && mkdir -p $(name)
	cp -r template/ functions/$(name)
	cd functions/$(name) && faas-cli new --lang python3-torch $(name)
	echo "deploy: \n	faas-cli build -f $(name).yml \n	kind load docker-image $(name):latest --name openfaas \n	faas-cli deploy -f $(name).yml \nrun: \n	cat input.json | faas invoke bert-base | faas-cli invoke $(name)" > functions/$(name)/Makefile

create-py3-debian:
	cd functions && mkdir -p $(name)
	cd functions/$(name) && faas-cli new --lang python3-debian $(name)
	echo "deploy: \n	faas-cli build -f $(name).yml \n	kind load docker-image $(name):latest --name openfaas \n	faas-cli deploy -f $(name).yml \nrun: \n	cat input.json | faas invoke bert-base | faas-cli invoke $(name)" > functions/$(name)/Makefile

create-openfaas:
	kind create cluster --name openfaas --config kind-config.yml
	echo export OPENFAAS_URL=http://127.0.0.1:31112 >> ~/.bashrc
	source ~/.bashrc
