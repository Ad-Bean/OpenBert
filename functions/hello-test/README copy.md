```bash
faas-cli build -f hello-world-python.yml
kind load docker-image hello-world-python:latest --name openfaas
faas-cli deploy -f hello-world-python.yml
```

```bash
cat input.json | faas-cli invoke hello-world-python
```
