from cdk8s import ApiObjectMetadata
from cdk8s import App

# This external secret is generated from a CRD (custom resource definition)
# https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/
from imports.io import external_secrets

from utils.inputs import Inputs


def create_secrets(manifest: App, inputs: Inputs, data: dict) -> None:
    """This function will add an ingress to the webservice object

    Args:
        manifest (App): The manifest object we attach the ingress to
        inputs (Inputs): The Github action INPUT arguments
        data (dict): Data defined by the service which are using this method. I.e. labels
    """
    secret = external_secrets.ExternalSecret(
        manifest,
        id=f"{inputs.app_name}-secret",
        metadata=ApiObjectMetadata(
            name=inputs.app_name,
            namespace=inputs.namespace,
        ),
        spec=external_secrets.ExternalSecretSpec(
            backend_type=external_secrets.ExternalSecretSpecBackendType.SECRETS_MANAGER,
            data_from=[f"cluster/{inputs.cluster_name}/{inputs.app_name}"],
        ),
    )

    return secret
