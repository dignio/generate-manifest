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
    app = App(outdir="output")
    GenericManifest.from_inputs(app, filename, inputs)

    print(f"::set-output name=manifest::{app.synth_yaml()}")


if __name__ == "__main__":
    main()
