from typing import Optional

from constructs import Construct

from .webservice import WebService

# This maps up which template to use for each service.
# This mapping must be updated when adding support for a new service.
MANIFEST_TEMPLATES = {
    "webservice": WebService,
}


def get_manifest_template(service_type: str) -> Optional[Construct]:
    """Get a manifest template"""
    return MANIFEST_TEMPLATES.get(service_type)
