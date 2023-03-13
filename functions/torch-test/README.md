```bash
faas-cli build -f torch-test.yml
kind load docker-image torch-test:latest --name openfaas
faas-cli deploy -f torch-test.yml
```

```bash
cat input.txt | faas-cli invoke torch-test
```
