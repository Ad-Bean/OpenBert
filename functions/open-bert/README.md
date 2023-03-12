```bash
faas-cli build -f open-bert.yml
kind load docker-image open-bert:latest --name openfaas
faas-cli deploy -f open-bert.yml
```

```bash
cat input.txt | faas-cli invoke open-bert
```
