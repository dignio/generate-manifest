import dataclasses
import os
from distutils.util import strtobool


@dataclasses.dataclass
class Inputs:
    """Input variables needed for this action."""
    # Mandatory attributes
    id: str
    namespace: str
    image: str

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
            id=os.getenv("app_name", ""),
            namespace=os.getenv("namespace", ""),
            image=os.getenv("docker_image"),
            replicas=int(os.getenv("replicas", "1")),
            port=int(os.getenv("port", "3000")),
            ingress=bool(strtobool(os.getenv("ingress", "false"))),
            ingress_host=os.getenv("ingress_host"),
            ingress_path=os.getenv("ingress_path", "/"),
        )
