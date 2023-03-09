```bash
faas-cli build -f hello-test.yml
kind load docker-image hello-test:latest --name openfaas
faas-cli deploy -f hello-test.yml
```

```bash
echo "" | faas-cli invoke hello-test
```
