import os
import datetime

from cdk8s import App

from manifests.generate import GenerateManifest


def cli_string_bool_conversion(string_bool: str) -> bool:
    """Convert string bool to bool

    Args:
        string_bool (str): The string "true" or "false"

    Returns:
        bool: The returning bool True or False
    """
    raw = string_bool.lower()

    if raw == "true":
        return True

    return False


def main():
    """
    Get the environment variables defined by the action.
    """
    name = os.getenv("app_name", "")
    namespace = os.getenv("namespace", "development")
    replicas = int(os.getenv("replicas", "1"))
    image = os.getenv("docker_image", "")
    port = int(os.getenv("port", "3000"))
    ingress = cli_string_bool_conversion(os.getenv("ingress", "false"))
    ingress_host = os.getenv("ingress_host", "")
    ingress_path = os.getenv("ingress_path", "/")

    app = App()

    GenerateManifest(
        app,
        filename=f"{name}-{namespace}-{datetime.datetime.now().replace(microsecond=0).isoformat()}",
        id=name,
        namespace=namespace,
        image=image,
        replicas=replicas,
        port=port,
        container_port=port,
        ingress=ingress,
        ingress_host=ingress_host,
        ingress_path=ingress_path,
    )

    app.synth()

    # print(f"::set-output name=myOutput::{my_output}")


if __name__ == "__main__":
    main()
