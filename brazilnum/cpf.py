#!/usr/bin/env python

import re
import random
from operator import mul

"""
Functions for working with Brazilian CPF identifiers.

"""

NONDIGIT = re.compile(r'[^0-9]')
CPF_WEIGHTS  = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def clean_cpf(cpf):
    """Takes a CPF and turns it into a string of only numbers."""
    return NONDIGIT.sub('', str(cpf))

def validate_cpf(cpf):
    """Check whether CPF is valid."""
    cpf = clean_cpf(cpf)
    # all complete CPF are 11 digits long
    if len(cpf) != 11:
        return False
    digits = [int(k) for k in cpf]  # identifier digits
    checks = digits[-2:]  # last two digits are check digits
    # validate the first check digit
    cs = (sum([mul(*k) for k in zip(CPF_WEIGHTS, digits[:-2])]) % 11) % 10
    if cs != checks[0]:
        return False  # first check digit is not correct
    # validate the second check digit
    cs = (sum([mul(*k) for k in zip(CPF_WEIGHTS, digits[1:-1])]) % 11) % 10
    if cs != checks[1]:
        return False  # second check digit is not correct
    # both check digits are correct
    return True

def cpf_check_digits(cpf):
    """Find two check digits needed to make a CPF valid."""
    cpf = clean_cpf(cpf)
    if len(cpf) < 9:
        raise ValueError('CPF must have at least 9 digits: {0}'.format(cpf))
    digits = [int(k) for k in cpf[:10]]
    # find the first check digit
    cs = (sum([mul(*k) for k in zip(CPF_WEIGHTS, digits)]) % 11) % 10
    # find the second check digit
    digits.append(cs)
    return cs, (sum([mul(*k) for k in zip(CPF_WEIGHTS, digits[1:])]) % 11) % 10

def format_cpf(cpf):
    """Applies typical 000.000.000-00 formatting to CPF."""
    fmt = '{0}.{1}.{2}-{3}'
    cpf = clean_cpf(cpf)
    return fmt.format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])

def pad_cpf(cpf, validate=True):
    """Takes a CPF that probably had leading zeros and pads it."""
    cpf = clean_cpf(cpf)
    cpf = '%0.011i' % int(cpf)
    if validate and not validate_cpf(cpf):
        raise ValueError('Invalid CPF: {0}'.format(cpf))
    return cpf

def random_cpf(formatted=True):
    """Create a random, valid CPF identifier."""
    stem = random.randint(100000000, 999999999)
    cpf = str(stem) + '{0}{1}'.format(*cpf_check_digits(stem))
    if formatted:
        return format_cpf(cpf)
    return cpf

