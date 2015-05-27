
import re

"""
Helper functions for validating identifiers.

"""

NONDIGIT = re.compile(r'[^0-9]')


def clean_id(identifier):
    """Remove non-numeric characters from input."""
    if isinstance(identifier, int):
        return str(identifier)
    return NONDIGIT.sub('', identifier)
