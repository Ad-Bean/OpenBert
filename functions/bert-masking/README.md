```bash
faas-cli build -f bert-masking.yml
kind load docker-image bert-masking:latest --name openfaas
faas-cli deploy -f bert-masking.yml
```

```bash
cat input.json | faas-cli invoke bert-masking
```
