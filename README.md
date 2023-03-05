# OpenBert

My final thesis project

## Requirements

### Docker

### Kind

[kind](https://kind.sigs.k8s.io/) is a tool for running local Kubernetes clusters using Docker container “nodes”.
kind was primarily designed for testing Kubernetes itself, but may be used for local development or CI.

### Faas CLI

faas-cli is the official CLI for [OpenFaaS](https://github.com/openfaas/faas)

## Set up environment

```bash
kind create cluster --name openfaas --config kind-config.yml

echo export OPENFAAS_URL=http://127.0.0.1:31112 >> ~/.bashrc

source ~/.bashrc
```

### Gateway

```bash
git clone https://github.com/openfaas/faas.git
cd faas/gateway
make
kind load docker-image alexellis2/gateway:latest --name openfaas
```

### FaasNet

```bash
git clone https://github.com/openfaas/faas-netes.git
cd faas-netes
make
kind load docker-image ghcr.io/openfaas/faas-netes:latest --name openfaas
```

### Image Pull Policy

If you want to modify the image pull policy, you can modify the imagePullPolicy field in the `faas-netes/yaml/gateway-dep.yml` file.

```yml
# line 36
image: alexellis2/gateway:latest
imagePullPolicy: IfNotPresent

# line 109
image: ghcr.io/openfaas/faas-netes:latest
imagePullPolicy: IfNotPresent

# line 128
- name: image_pull_policy
  value: "IfNotPresent"
```

## Set up OpenFaas

```bash
cd faas-netes

kubectl apply -f namespaces.yml
kubectl -n openfaas create secret generic basic-auth --from-literal=basic-auth-user=admin --from-literal=basic-auth-password=admin

kubectl apply -f ./yaml/
```

Run `kubectl get all -n openfaas` to get all pods

Run `kubectl logs gateway-6787cc5f9-rj9ct -c faas-netes -n openfaas --since 0` to check the logs from openfass-gateway

## Functions

faas-cli login:

```bash
faas-cli login -u admin -p admin
```

```bash
mkdir -p ./functions/hello-world-python && cd ./functions/hello-world-python
```

create functions:

```bash
faas-cli new --lang python hello-world-python
```

You will get `hello-world-python  hello-world-python.yml  template` files.

in `/hello-world-python/hello-world-python/handler.py`:

```python
def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    return ("Hello world!" + req)
```

### Compile, build iamges, and deploy functions to OpenFaas

```bash
faas-cli build -f hello-python.yml
kind load docker-image hello-python:latest --name openfaas
faas-cli deploy -f hello-python.yml
```

## Notes

### Get clusters

```bash
kind get clusters

kind delete cluster --name openfaas
```

### Delete Clusters and OpenFaas

```bash
kubectl delete ns openfaas-fn --force --grace-period=0
kubectl delete ns openfaas --force --grace-period=0
```
