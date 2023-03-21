create-py:
	cd functions && mkdir -p $(name)
	cd functions/$(name) && faas-cli new --lang python $(name)

create-py3:
	cd functions && mkdir -p $(name)
	cd functions/$(name) && faas-cli new --lang python3 $(name)

create-torch:
	cd functions && mkdir -p $(name)
	cp -r template/ functions/$(name)/
	faas-cli new --lang python3-torch $(name)

create-py3-debian:
	cd functions && mkdir -p $(name)
	cd functions/$(name) && faas-cli new --lang python3-debian $(name)

