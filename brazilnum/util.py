import re

"""
Helper functions for validating identifiers.

"""

NONDIGIT = re.compile(r'[^0-9]')
NONALNUM = re.compile(r'[^0-9A-Za-z]')


def clean_id(identifier):
    """Remove non-numeric characters from input."""
    if isinstance(identifier, int):
        return str(identifier)
    return NONDIGIT.sub('', identifier)


def clean_alphanumeric_id(identifier):
    """Remove non-alphanumeric characters from input, preserving letters
    and normalizing to uppercase. Used for identifiers that may contain
    letters, such as the alphanumeric CNPJ format introduced by Receita
    Federal (Instrução Normativa RFB nº 2.229/2024), effective 07/2026.
    """
    if isinstance(identifier, int):
        return str(identifier)
    return NONALNUM.sub('', identifier).upper()


def pad_id(identifier, fmt):
    """Pad an identifier with leading zeros."""
    if not isinstance(identifier, int):
        identifier = clean_id(identifier)

        if identifier == '':
            identifier = 0
        else:
            identifier = int(identifier)

    return fmt % identifier


def pad_alphanumeric_id(identifier, length):
    """Pad an alphanumeric identifier with leading zeros as a string.
    Unlike pad_id, this does not coerce to int, since alphanumeric
    identifiers (e.g. the new CNPJ format) cannot be represented as one.
    """
    identifier = clean_alphanumeric_id(identifier)
    return identifier.zfill(length)