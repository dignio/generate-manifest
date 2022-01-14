from constructs import Construct
from cdk8s import ApiObjectMetadata, Duration
from cdk8s_plus_22 import (
    Service,
    Deployment,
    Ingress,
    IngressRule,
    IngressBackend,
    ServiceType,
    ContainerProps,
    RestartPolicy,
    Protocol,
    Probe,
    HttpIngressPathType,
)


class WebService(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        namespace: str,
        image: str,
        replicas: int,
        port: int,
        container_port: int,
        ingress: bool,
        ingress_host: str,
        ingress_path: str,
        **kwargs,
    ):
        super().__init__(scope, id)

        labels = {"app": id}

        service = Service(
            self,
            id=f"{id}-service",
            metadata=ApiObjectMetadata(
                name=id,
                labels=labels,
                namespace=namespace,
                annotations={"alb.ingress.kubernetes.io/target-type": "ip"},
            ),
            type=ServiceType.NODE_PORT,
        )

        deployment = Deployment(
            self,
            id=f"{id}-deployment",
            metadata=ApiObjectMetadata(
                name=id,
                labels=labels,
                namespace=namespace,
            ),
            containers=[
                ContainerProps(
                    name=id,
                    image=image,
                    port=container_port,
                    liveness=Probe.from_http_get(
                        path="/",
                        failure_threshold=3,
                        period_seconds=Duration.seconds(15),
                        timeout_seconds=Duration.seconds(60),
                        port=container_port,
                    ),
                    readiness=Probe.from_http_get(
                        path="/",
                        failure_threshold=3,
                        period_seconds=Duration.seconds(15),
                        timeout_seconds=Duration.seconds(60),
                        port=container_port,
                    ),
                )
            ],
            restart_policy=RestartPolicy.ALWAYS,
            replicas=replicas,
            default_selector=False,
        )

        deployment.pod_metadata.add_label(value=id, key="app")
        deployment.select_by_label(value=id, key="app")

        service.add_deployment(
            deployment=deployment,
            port=port,
            target_port=container_port,
            protocol=Protocol.TCP,
        )

        if ingress:
            Ingress(
                self,
                id=id,
                metadata=ApiObjectMetadata(
                    name=id,
                    labels=labels,
                    namespace=namespace,
                    annotations={
                        "kubernetes.io/ingress.class": "alb",
                        "alb.ingress.kubernetes.io/scheme": "internet-facing",
                        "alb.ingress.kubernetes.io/listen-ports": '[{"HTTPS":443}]',
                        "alb.ingress.kubernetes.io/ssl-policy": "ELBSecurityPolicy-TLS-1-1-2017-01",
                        "alb.ingress.kubernetes.io/healthcheck-path": "/",
                        "alb.ingress.kubernetes.io/healthcheck-interval-seconds": "20",
                        "alb.ingress.kubernetes.io/success-codes": "200",
                        "alb.ingress.kubernetes.io/load-balancer-name": f"ingress-{id}",
                    },
                ),
                rules=[
                    IngressRule(
                        backend=IngressBackend.from_service(service=service, port=port),
                        host=ingress_host,
                        path=ingress_path,
                        path_type=HttpIngressPathType.PREFIX,
                    )
                ],
            )
