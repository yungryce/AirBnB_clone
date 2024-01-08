#!/usr/bin/env python3
"""defines all common attributes/methods for other classes"""
from datetime import datetime
import uuid

class BaseModel:
    """
    """
    def __init__(self):
        """
        """
        self.id = uuid.uuid4()

    def __str__(self):
        """
        """
        return f"{}"
