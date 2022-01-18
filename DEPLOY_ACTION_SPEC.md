## What should the action do?

The following steps are the workflow setup for the Apotek1 integration. What we want is to rewrite this into a generic action for deployments.
The sample yaml is just to show what we have to do each step. Possibly we have to rewrite some of it to javascript/python to make it more dynamic. Looking into this.

### Configure AWS credentials

- Access key
- Secret access key
- Region

```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v1
  with:
    aws-access-key-id: ${{ secrets.DEVELOPMENT_GHK8S_AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.DEVELOPMENT_GHK8S_AWS_SECRET_KEY_ID }}
    aws-region: eu-north-1
```

### Sign in to Amazon ECR

We have to sign in to get the registry information

```yaml
- name: Login to Amazon ECR
  id: login-ecr
  uses: aws-actions/amazon-ecr-login@v1
```

### Checkout the repository

Checkout the kubernetes repository to get the manifest files

```yaml
- name: Checkout code
  uses: actions/checkout@v2
  with:
    repository: dignio/kubernetes
    token: ${{ secrets.REPO_TOKEN }}
```

### Install kustomize

```yaml
- name: Install kustomize
  uses: imranismail/setup-kustomize@v1
```

### Build the manifest files with Kustomize

This will edit the kustomize fil and update the docker image tag to the latest one

```yaml
- name: Build the manifest with kustomize
  env:
    ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
    ECR_REPOSITORY: <app-name>
    IMAGE_TAG: ${{ github.sha }}
  run: |
    cd services/<app-name>/dev-k8s-eu-north-1
    kustomize edit set image <app-name>=${{ env.ECR_REGISTRY }}/${{ env.ECR_REPOSITORY }}:${{ env.IMAGE_TAG }}
    kustomize build . > <app-name>-dev-k8s-eu-north-1-manifest.yaml
    cd
```

### Should we commit / push the manifest file to git/s3?

### Apply the manifest to the EKS cluster(s)

The end game is to apply the manifest to the EKS cluster.

TODO: add what cluster to deploy to

```yaml
- name: Deploy to EKS cluster
  uses: Consensys/kubernetes-action@master
  env:
    KUBE_CONFIG_DATA: ${{ secrets.KUBE_CONFIG }}
    DEVELOPMENT_GHK8S_AWS_ACCESS_KEY_ID: ${{ secrets.DEVELOPMENT_GHK8S_AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.DEVELOPMENT_GHK8S_AWS_SECRET_KEY_ID }}
    AWS_REGION: eu-north-1
  with:
    args: apply -f services/prevent-ui/dev-k8s-eu-north-1/prevent-ui-manifest.yaml
```

python discord way of deploying: https://github.com/python-discord/bot/blob/main/.github/workflows/deploy.yml
