from cdk8s import Chart
from constructs import Construct

from utils.inputs import Inputs
from manifests import get_manifest_template


class GenericManifest(Chart):
    @classmethod
    def from_inputs(cls, scope: Construct, filename: str, inputs: Inputs):
        """Create a Manifest from input parameters."""
        # Get the appropriate template
        manifest = GenericManifest(scope, filename)
        template = get_manifest_template(inputs.app_name)

        # Instantiate the template
        template.from_inputs(manifest, inputs)
