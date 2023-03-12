```bash
faas-cli build -f openbert.yml
kind load docker-image openbert:latest --name openfaas
faas-cli deploy -f openbert.yml
```

```bash
cat input.txt | faas-cli invoke openbert
```
