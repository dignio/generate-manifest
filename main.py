import datetime
import os
from distutils.util import strtobool

from cdk8s import App

from manifests.generate import GenerateManifest


def main():
    """Generate a Kubernetes manifest for a requested service."""
    # Prepare input parameters
    inputs = Inputs.from_env()
    current_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    filename = f"{inputs.id}-{inputs.namespace}-{current_time}"

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
