from cdk8s import Chart
from constructs import Construct

from .webservice import WebService


class GenerateManifest(Chart):
    def __init__(
        self,
        scope: Construct,
        filename: str,
        id: str,
        namespace: str,
        image: str,
        replicas: int,
        port: int,
        containerPort: int,
        ingress: bool,
        ingress_host: str,
        ingress_path: str,
    ):
        super().__init__(scope, filename)

        WebService(
            self,
            id=id,
            namespace=namespace,
            image=image,
            replicas=replicas,
            port=port,
            containerPort=containerPort,
            ingress=ingress,
            ingress_host=ingress_host,
            ingress_path=ingress_path,
        )
