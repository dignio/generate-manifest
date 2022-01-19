import dataclasses
import os
from distutils.util import strtobool


@dataclasses.dataclass
class Inputs:
    """Input variables needed for this action."""

    # Mandatory attributes
    app_name: str
    namespace: str
    docker_image: str

    # Optional attributes
    replicas: int
    port: int
    container_port: int
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
            namespace=os.getenv("INPUT_NAMESPACE", ""),
            docker_image=os.getenv("INPUT_DOCKER_IMAGE"),
            replicas=int(os.getenv("INPUT_REPLICAS", "1")),
            port=int(os.getenv("INPUT_PORT", "3000")),
            container_port=int(os.getenv("INPUT_CONTAINER_PORT")),
            ingress=bool(strtobool(os.getenv("INPUT_INGRESS", "false"))),
            ingress_host=os.getenv("INPUT_INGRESS_HOST"),
            ingress_path=os.getenv("INPUT_INGRESS_PATH", "/"),
        )
