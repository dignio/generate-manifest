# Generate Manifest Action

This is a GitHub Action which can be used to generate the k8s manifest needed to deploy a specified service.

It aims to a generic generator that can generate any manifest we'll need for deployment.

```yaml
- uses: dignio/generate-manifest@v1
  name: Generate the Kubernetes manifest
  needs: build_and_push
  with:
    # These must be specified for the action to work
    app_name: prevent-ui
    namespace: development
    docker_image: 833870238474.dkr.ecr.eu-north-1.amazonaws.com/prevent-ui:9628f958eb4a69571cfee558624fa0a33fa49c4f

    # These are optional
    replicas: 1
    port: 80
    container_port: 80
    ingress: true
    ingress_host: prevent.dev.dignio.dev
    ingress_path: /
```

## Setup

```
pipenv install
```

## Testing this action locally

```bash
app_name=prevent-ui \
namespace=development \
replicas=1 \
docker_image="387308402250.dkr.ecr.eu-north-1.amazonaws.com/prevent-ui:9628f958eb4a69571cfee558624fa0a33fa49c4f" \
port=80 \
container_port=80 \
ingress=true \
ingress_host=prevent.dev.dignio.dev \
pipenv run generate
```

---
