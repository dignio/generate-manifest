# Generate Manifest Action

This is a GitHub Action which can be used to generate the k8s manifest needed to deploy a specified service.

It aims to a generic generator that can generate any manifest we'll need for deployment.

```yaml
- uses: dignio/generate-manifest@v3
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

    # Add secret config. Optional.
    # Both has to be set.
    secretsmanager: true
    cluster_name: dev-k8s

    # These are optional
    replicas: 1
    port: 80
    container_size: medium
    container_port: 80
    container_command: '["curl"]'
    container_args: '["-I", "https://www.dignio.com"]'
```

## Action output

The output from this action is the generated manifest. Can be accessed by other steps by using this command.

```yaml
- uses: ...
  with:
    manifest: ${{ steps.generate_manifest.outputs.manifest }}
```

## Setup

```bash
npm install
```

## Testing this action locally

```bash
npm run dev
```

## Build the dist files for the action

```bash
npm run build
```

## Tests

This action is using the `fixture/prevent-api.yaml` while running the `.github/workflows/test-action.yaml` to validate the output is correct
