"""ID utility helpers."""

import uuid


def generate_uuid() -> uuid.UUID:
    """Generate a UUID4 value."""

    return uuid.uuid4()
