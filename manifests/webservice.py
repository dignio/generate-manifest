from cdk8s import ApiObjectMetadata
from cdk8s import Duration
from cdk8s_plus_22 import Service
from cdk8s_plus_22 import Deployment
from cdk8s_plus_22 import Ingress
from cdk8s_plus_22 import IngressRule
from cdk8s_plus_22 import IngressBackend
from cdk8s_plus_22 import ServiceType
from cdk8s_plus_22 import ContainerProps
from cdk8s_plus_22 import RestartPolicy
from cdk8s_plus_22 import Protocol
from cdk8s_plus_22 import Probe
from cdk8s_plus_22 import HttpIngressPathType
from constructs import Construct

from utils.inputs import Inputs


class WebService(Construct):
    """
    A generic kubernetes manifest for a webservice.

    This might be a webapp, or a microservice of some kind.
    """

    @classmethod
    def from_inputs(cls, scope: Construct, inputs: Inputs):
        """Create a webservice from a set of input parameters."""
        webservice = WebService(scope, inputs.app_name)
        labels = {"app": inputs.app_name}

        # Create a service
        service = Service(
            webservice,
            id=f"{inputs.app_name}-service",
            metadata=ApiObjectMetadata(
                name=inputs.app_name,
                labels=labels,
                namespace=inputs.namespace,
                annotations={"alb.ingress.kubernetes.io/target-type": "ip"},
            ),
            type=ServiceType.NODE_PORT,
        )

        # Create a deployment
        deployment = Deployment(
            webservice,
            id=f"{inputs.app_name}-deployment",
            metadata=ApiObjectMetadata(
                name=inputs.app_name,
                labels=labels,
                namespace=inputs.namespace,
            ),
            containers=[
                ContainerProps(
                    name=inputs.app_name,
                    image=inputs.docker_image,
                    port=inputs.container_port,
                    liveness=Probe.from_http_get(
                        path="/",
                        failure_threshold=3,
                        period_seconds=Duration.seconds(15),
                        timeout_seconds=Duration.seconds(60),
                        port=inputs.container_port,
                    ),
                    readiness=Probe.from_http_get(
                        path="/",
                        failure_threshold=3,
                        period_seconds=Duration.seconds(15),
                        timeout_seconds=Duration.seconds(60),
                        port=inputs.container_port,
                    ),
                )
            ],
            restart_policy=RestartPolicy.ALWAYS,
            replicas=inputs.replicas,
            default_selector=False,
        )

        # Attach the deployment to the service.
        deployment.pod_metadata.add_label(value=inputs.app_name, key="app")
        deployment.select_by_label(value=inputs.app_name, key="app")
        service.add_deployment(
            deployment=deployment,
            port=inputs.port,
            target_port=inputs.container_port,
            protocol=Protocol.TCP,
        )

        # Add an ingress, if necessary.
        if inputs.ingress:
            Ingress(
                webservice,
                id=inputs.app_name,
                metadata=ApiObjectMetadata(
                    name=inputs.app_name,
                    labels=labels,
                    namespace=inputs.namespace,
                    annotations={
                        "kubernetes.io/ingress.class": "alb",
                        "alb.ingress.kubernetes.io/scheme": "internet-facing",
                        "alb.ingress.kubernetes.io/listen-ports": '[{"HTTPS":443}]',
                        "alb.ingress.kubernetes.io/ssl-policy": "ELBSecurityPolicy-TLS-1-1-2017-01",
                        "alb.ingress.kubernetes.io/healthcheck-path": "/",
                        "alb.ingress.kubernetes.io/healthcheck-interval-seconds": "20",
                        "alb.ingress.kubernetes.io/success-codes": "200",
                        "alb.ingress.kubernetes.io/load-balancer-name": f"ingress-{inputs.app_name}",
                    },
                ),
                rules=[
                    IngressRule(
                        backend=IngressBackend.from_service(service=service, port=inputs.port),
                        host=inputs.ingress_host,
                        path=inputs.ingress_path,
                        path_type=HttpIngressPathType.PREFIX,
                    )
                ],
            )