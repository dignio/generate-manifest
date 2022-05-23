from cdk8s import ApiObjectMetadata
from cdk8s import Duration, Size

from cdk8s_plus_22 import Service
from cdk8s_plus_22 import Deployment
from cdk8s_plus_22 import ServiceType
from cdk8s_plus_22 import ContainerProps
from cdk8s_plus_22 import ContainerResources
from cdk8s_plus_22 import CpuResources
from cdk8s_plus_22 import Cpu
from cdk8s_plus_22 import MemoryResources
from cdk8s_plus_22 import RestartPolicy
from cdk8s_plus_22 import Protocol
from cdk8s_plus_22 import Probe
from constructs import Construct

from .ingress import create_ingress
from .secret import create_secrets
from utils.inputs import Inputs
from utils.resources import get_resources


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

        memory, cpu = get_resources(inputs.container_size)

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
                        path=inputs.healthcheck_path,
                        failure_threshold=3,
                        period_seconds=Duration.seconds(15),
                        timeout_seconds=Duration.seconds(60),
                        port=inputs.container_port,
                    ),
                    readiness=Probe.from_http_get(
                        path=inputs.healthcheck_path,
                        failure_threshold=3,
                        period_seconds=Duration.seconds(15),
                        timeout_seconds=Duration.seconds(60),
                        port=inputs.container_port,
                    ),
                    resources=ContainerResources(
                        cpu=CpuResources(
                            limit=Cpu.millis(cpu),
                            request=Cpu.millis(cpu),
                        ),
                        memory=MemoryResources(
                            limit=Size.gibibytes(amount=memory),
                            request=Size.gibibytes(amount=memory),
                        ),
                    ),
                )
            ],
            restart_policy=RestartPolicy.ALWAYS,
            replicas=inputs.replicas,
        )

        # Attach the deployment to the service.
        deployment.pod_metadata.add_label(value=inputs.app_name, key="app")

        service.add_deployment(
            depl=deployment,
            port=inputs.port,
            target_port=inputs.container_port,
            protocol=Protocol.TCP,
        )

        # Add an ingress, if necessary.
        if inputs.ingress:
            create_ingress(webservice, inputs, {"service": service, "labels": labels})

        # Use secrets manager
        if inputs.secretsmanager:
            create_secrets(webservice, inputs, {"service": service, "labels": labels})
