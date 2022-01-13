# Create manifest action

```yaml
- uses: dignio/create-manifest@v1
  name: Create the Kubernetes manifest
  needs: build_and_push
  with:
    app_name: prevent-ui
    namespace: development
    replicas: 1
    docker_image: 833870238474.dkr.ecr.eu-north-1.amazonaws.com/prevent-ui:9628f958eb4a69571cfee558624fa0a33fa49c4f
    port: 80
    ingress: true
    ingress_path: /
    ingress_host: prevent.dev.dignio.dev
```
