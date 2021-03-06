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
    app_name: prevent-demo
    service_type: webservice
    instance: previews
    namespace: development
    docker_image: <org-id>.dkr.ecr.<region>.amazonaws.com/<repo-name>:<tag>

    # To fetch secrets from AWS secrets manager, secretsmanager has to be set to true.
    # In order to make it work you need the cluster_name be set to the EKS cluster name
    # Example of how this works:
    # external secrets services looks for "cluster/bogus-cluster/prevent-demo" for the secrets,
    # then it fetches them and injects them to the container for this deployment
    secretsmanager: true
    cluster_name: bogus-cluster

    # These are optional
    replicas: 1
    port: 80
    container_size: medium
    container_port: 80
    container_command: '["curl"]'
    container_args: '["-I", "https://www.dignio.com"]'
    # Only if your instances is running on fargate
    fargate: true
```

Example by using it as a cronjob
```yaml
- uses: dignio/generate-manifest@v3
  name: Generate the Kubernetes manifest
  id: generate_manifest
  needs: build_and_push
  with:
    # These must be specified for the action to work
    app_name: prevent-demo
    service_type: cronjob
    instance: previews
    namespace: development
    docker_image: <org-id>.dkr.ecr.<region>.amazonaws.com/<repo-name>:<tag>

    # To fetch secrets from AWS secrets manager, secretsmanager has to be set to true.
    # In order to make it work you need the cluster_name be set to the EKS cluster name
    # Example of how this works:
    # external secrets services looks for "cluster/bogus-cluster/prevent-demo" for the secrets,
    # then it fetches them and injects them to the container for this deployment
    secretsmanager: true
    cluster_name: bogus-cluster

    # These are optional
    container_command: '["curl"]'
    container_args: '["-I", "https://www.dignio.com"]'
    # Only if your instances is running on fargate
    fargate: true

    # the cron schedule
    schedule: "0 * * * *"
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

This command will use nodemon and the .env file to create a manifest for you. The manifest will be printed to the terminal,
and it will hot reload for continuous feedback.

```bash
npm run dev
```

## Build the dist files for the action

```bash
npm run build
```

## Tests

This action is using the `fixture/prevent-api.yaml` while running the `.github/workflows/test-action.yaml` to validate the output is correct
