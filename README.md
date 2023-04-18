# OpenBert

My final thesis project

## Requirements

### Docker

### Kind

[kind](https://kind.sigs.k8s.io/) is a tool for running local Kubernetes clusters using Docker container “nodes”.
kind was primarily designed for testing Kubernetes itself, but may be used for local development or CI.

### Faas CLI

[faas-cli](https://github.com/openfaas/faas-cli) is the official CLI for [OpenFaaS](https://github.com/openfaas/faas)

### Helm

[Helm](https://helm.sh/docs/intro/install/) is the best way to find, share, and use software built for Kubernetes.

## Set up environment

```bash
kind create cluster --name openfaas --config kind-config.yml

echo export OPENFAAS_URL=http://127.0.0.1:31112 >> ~/.bashrc

source ~/.bashrc
```

```zsh
echo export OPENFAAS_URL=http://127.0.0.1:31112 >> ~/.zshrc

source ~/.zshrc
```

### Minio

https://github.com/bitnami/charts/tree/main/bitnami/minio

```bash
helm repo add my-repo https://charts.bitnami.com/bitnami
helm install my-release my-repo/minio
```

To get your credentials run:

```bash
export ROOT_USER=$(kubectl get secret --namespace default my-release-minio -o jsonpath="{.data.root-user}" | base64 -d)
export ROOT_PASSWORD=$(kubectl get secret --namespace default my-release-minio -o jsonpath="{.data.root-password}" | base64 -d)
```

Run a MinIO&reg; Client pod and append the desired command (e.g. 'admin info'):

```bash
kubectl run --namespace default my-release-minio-client \
    --rm --tty -i --restart='Never' \
    --env MINIO_SERVER_ROOT_USER=$ROOT_USER \
    --env MINIO_SERVER_ROOT_PASSWORD=$ROOT_PASSWORD \
    --env MINIO_SERVER_HOST=my-release-minio \
    --image docker.io/bitnami/minio-client:2023.4.12-debian-11-r1 -- admin info minio
```

Get the MinIO URL:

```bash
echo "MinIO&reg; web URL: http://127.0.0.1:9001/minio"
kubectl port-forward --namespace default svc/my-release-minio 9001:9001
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

## Expand Gateway timeout

since the default timeout of gateway is 60s, it cannot support large model. We need to expand the `write_timeout`

`/faas-netes/yaml/gateway-dep.yml`

```yaml
env:
  - name: read_timeout
    value: "6500s"
  - name: write_timeout
    value: "6500s"
  - name: upstream_timeout
    value: "6000s"
```

`/faas-netes/chart/openfaas/values.yaml`

```yaml
gateway:
  image: ghcr.io/openfaas/gateway:0.26.3
  readTimeout: "6500s"
  writeTimeout: "6500s"
  upstreamTimeout: "6000s" # Must be smaller than read/write_timeout
```

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
faas-cli new --lang python3-debian hello-world-python
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

Or if you have Make:

```bash
make create-py name=hello-test
```

### Compile, build iamges, and deploy functions to OpenFaas

```bash
faas-cli build -f hello-world-python.yml
kind load docker-image hello-world-python:latest --name openfaas
faas-cli deploy -f hello-world-python.yml
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

### Invoke Functions

```bash
faas-cli list
faas-cli invoke <function>

echo "test" | faas-cli invoke hello-world-python
```

### Delete Functions

```bash
faas-cli remove <function>
```

### Function Chaining

I dont know why it cannot use HTTP request in the function

```bash
echo "" | faas invoke <function> | faas invoke <function>
```

### Function Environments

```yaml
environment:
  minio_hostname: "10.96.130.15:9000"
  minio_access_key: ""
  minio_secret_key: ""
  write_debug: true
  read_timeout: 600000
  write_timeout: 600000
  exec_timeout: 600000
```

### Trouble Shooting

[Openfaas Docs](https://docs.openfaas.com/deployment/troubleshooting/)

```bash
kubectl logs -n openfaas deploy/gateway -c gateway
```

```bash
kubectl logs -n openfaas deploy/gateway -c faas-netes

# Or, if you are using the CRD and Operator:
kubectl logs -n openfaas deploy/gateway -c operator
```
