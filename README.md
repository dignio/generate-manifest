# Generate Manifest Action

This is a GitHub Action which can be used to generate the k8s manifest needed to deploy a specified service.

It aims to a generic generator that can generate any manifest we'll need for deployment.

```yaml
- uses: dignio/generate-manifest@v1
  name: Generate the Kubernetes manifest
  id: generate_manifest
  needs: build_and_push
  with:
    # These must be specified for the action to work
    app_name: prevent-ui
    service_type: webservice
    instance: development
    namespace: development
    docker_image: <org-id>.dkr.ecr.<region>.amazonaws.com/<repo-name>:<tag>

    # These are optional
    replicas: 1
    port: 80
    container_port: 80
    ingress: true
    ingress_host: prevent.dev.dignio.dev
    ingress_path: /
```

### Action output

The output from this action is the generated manifest. Can be accessed by other steps by using this command.

```yaml
- uses: ...
  with:
    manifest: ${{ steps.generate_manifest.outputs.manifest }}
```

## Setup

```
pipenv install
```

## Testing this action locally

```bash
pipenv run generate
```

---
