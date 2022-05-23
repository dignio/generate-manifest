import dataclasses
import os
from distutils.util import strtobool


@dataclasses.dataclass
class Inputs:
    """Input variables needed for this action."""

    # Mandatory attributes
    app_name: str
    service_type: str
    instance: str
    namespace: str
    docker_image: str
    healthcheck_path: str

    # Optional attributes
    secretsmanager: bool
    replicas: int
    port: int
    container_port: int
    cluster_name: str
    ingress: bool
    ingress_host: str
    ingress_path: str

    def as_dict(self):
        """Return the dataclass as a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_env(cls):
        return Inputs(
            app_name=os.getenv("INPUT_APP_NAME", ""),
            service_type=os.getenv("INPUT_SERVICE_TYPE", ""),
            instance=os.getenv("INPUT_INSTANCE", ""),
            namespace=os.getenv("INPUT_NAMESPACE", ""),
            docker_image=os.getenv("INPUT_DOCKER_IMAGE"),
            healthcheck_path=os.getenv("INPUT_HEALTHCHECK_PATH"),
            secretsmanager=bool(strtobool(os.getenv("INPUT_SECRETSMANAGER"))),
            replicas=int(os.getenv("INPUT_REPLICAS", "1")),
            port=int(os.getenv("INPUT_PORT", "3000")),
            container_port=int(os.getenv("INPUT_CONTAINER_PORT")),
            cluster_name=os.getenv("INPUT_CLUSTER_NAME"),
            ingress=bool(strtobool(os.getenv("INPUT_INGRESS", "false"))),
            ingress_host=os.getenv("INPUT_INGRESS_HOST"),
            ingress_path=os.getenv("INPUT_INGRESS_PATH", "/"),
        )
