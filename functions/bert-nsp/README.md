```bash
faas-cli build -f bert-nsp.yml
kind load docker-image bert-nsp:latest --name openfaas
faas-cli deploy -f bert-nsp.yml
```

```bash
cat input.json | faas-cli invoke bert-base | faas-cli invoke bert-nsp
```
