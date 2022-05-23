from cdk8s import ApiObjectMetadata
from cdk8s import App
from cdk8s_plus_22 import Ingress
from cdk8s_plus_22 import IngressRule
from cdk8s_plus_22 import IngressBackend
from cdk8s_plus_22 import HttpIngressPathType

from utils.inputs import Inputs


def create_ingress(manifest: App, inputs: Inputs, data: dict) -> None:
    """This function will add an ingress to the webservice object

    Args:
        manifest (App): The manifest object we attach the ingress to
        inputs (Inputs): The Github action INPUT arguments
        data (dict): Data defined by the service which are using this method. I.e. labels
    """
    Ingress(
        manifest,
        id=f"{inputs.app_name}-ingress",
        metadata=ApiObjectMetadata(
            name=f"{inputs.instance}-{inputs.app_name}",
            labels=data["labels"],
            namespace=inputs.namespace,
            annotations={
                "kubernetes.io/ingress.class": "alb",
                "alb.ingress.kubernetes.io/scheme": "internet-facing",
                "alb.ingress.kubernetes.io/listen-ports": '[{"HTTPS":443}]',
                "alb.ingress.kubernetes.io/ssl-policy": "ELBSecurityPolicy-TLS-1-1-2017-01",
                "alb.ingress.kubernetes.io/healthcheck-path": inputs.healthcheck_path,
                "alb.ingress.kubernetes.io/healthcheck-interval-seconds": "20",
                "alb.ingress.kubernetes.io/success-codes": "200",
                "alb.ingress.kubernetes.io/load-balancer-name": f"ingress-{inputs.instance}-{inputs.app_name}",
            },
        ),
        rules=[
            IngressRule(
                backend=IngressBackend.from_service(service=data["service"], port=inputs.port),
                host=inputs.ingress_host,
                path=inputs.ingress_path,
                path_type=HttpIngressPathType.PREFIX,
            )
        ],
    )
