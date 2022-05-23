#!/usr/bin/env python3
import datetime
import base64

from cdk8s import App

from manifests.generic import GenericManifest
from utils.inputs import Inputs


def main():
    """Generate a Kubernetes manifest for a requested service."""
    # Prepare input parameters
    inputs = Inputs.from_env()

    current_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    filename = f"{inputs.app_name}-{inputs.namespace}-{current_time}"

    # Generate the manifest, and save it in a folder called 'output'
    app = App()
    GenericManifest.from_inputs(app, filename, inputs)
    print(app.synth_yaml())
    output = base64.b64encode(app.synth_yaml().encode("utf-8")).decode("utf-8")

    print(f"::set-output name=manifest::{output}")


if __name__ == "__main__":
    main()
