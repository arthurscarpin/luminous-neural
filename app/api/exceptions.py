from typing import Any

class NotFoundException(Exception):
    """Exception raised when a requested resource is not found."""

    def __init__(self, resource: str, resource_id: Any):
        """Initialize the exception with resource details.

        Args:
            resource (str): Name of the missing resource.
            resource_id (Any): Identifier of the missing resource.
        """
        self.resource = resource
        self.resource_id = resource_id
        self.message = f"{resource} with ID {resource_id} not found."
        super().__init__(self.message)
