import datetime
import os
from distutils.util import strtobool

from cdk8s import App

from manifests.generate import GenerateManifest


def main():
    """Generate a Kubernetes manifest for a requested service."""
    # Mandatory attributes
    name = os.getenv("app_name", "")
    namespace = os.getenv("namespace", "")
    image = os.getenv("docker_image", "")

    # Optional attributes
    replicas = int(os.getenv("replicas", "1"))
    port = int(os.getenv("port", "3000"))
    ingress = bool(strtobool(os.getenv("ingress", "false")))
    ingress_host = os.getenv("ingress_host", "")
    ingress_path = os.getenv("ingress_path", "/")

    app = App()

    GenerateManifest(
        app,
        filename=f"{name}-{namespace}-{datetime.datetime.now().replace(microsecond=0).isoformat()}",
        id=name,
        namespace=namespace,
        image=image,
        replicas=replicas,
        port=port,
        container_port=port,
        ingress=ingress,
        ingress_host=ingress_host,
        ingress_path=ingress_path,
    )

    app.synth()

    # print(f"::set-output name=myOutput::{my_output}")


if __name__ == "__main__":
    main()
