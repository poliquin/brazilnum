#!/usr/bin/env python

import re
from random import randint
from operator import mul

"""
Functions for working with Brazilian PIS/PASEP identifiers.

"""

NONDIGIT = re.compile(r'[^0-9]')
PIS_WEIGHTS = [3, 2, 9, 8, 7, 6, 5, 4, 3, 2]


def clean_pis(pis):
    """Takes a PIS/PASEP and turns it into a string of only numbers."""
    return NONDIGIT.sub('', str(pis))

def validate_pis(pis):
    """Check whether PIS/PASEP is valid."""
    pis = clean_pis(pis)
    # all complete PIS/PASEP are 11 digits long
    if len(pis) != 11:
        return False
    return int(pis[-1]) == pis_check_digit(pis)

def pis_check_digit(pis):
    """Find check digit needed to make a PIS/PASEP valid."""
    pis = clean_pis(pis)
    if len(pis) < 10:
        raise ValueError('PIS/PASEP must be at least 10 digits: {0}'.format(pis))
    digits = [int(k) for k in pis[:11]]
    # find check digit
    cs = sum([mul(*k) for k in zip(PIS_WEIGHTS, digits)]) % 11
    return 0 if cs < 2 else 11 - cs

def pis_check_digits(pis):
    """Alias for pis_check_digit function. PIS/PASEP uses single digit."""
    return pis_check_digit(pis)

def format_pis(pis):
    """Applies typical 000.0000.000-0 formatting to PIS/PASEP."""
    fmt = '{0}.{1}.{2}-{3}'
    pis = clean_pis(pis)
    if len(pis) < 11:
        raise ValueError('Insufficient length for PIS/PASEP: {0}'.format(pis))
    return fmt.format(pis[:3], pis[3:7], pis[7:10], pis[10])

def pad_pis(pis, validate=True):
    """Takes a PIS/PASEP that had leading zeros and pads it."""
    pis = '%0.011i' % int(clean_pis(pis))
    if validate and not validate_pis(pis):
        raise ValueError('Invalid PIS/PASEP: {0}'.format(pis))
    return pis

def random_pis(formatted=True):
    """Create a random, valid PIS identifier."""
    pis = randint(1000000000, 9999999999)
    pis = str(pis) + str(pis_check_digit(pis))
    if formatted:
        return format_pis(pis)
    return pis

