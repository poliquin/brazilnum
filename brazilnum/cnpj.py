#!/usr/bin/env python

import re
import random
from operator import mul

"""
Functions for working with Brazilian company identifiers (CNPJ).

"""

NONDIGIT = re.compile(r'[^0-9]')
CNPJ_FIRST_WEIGHTS  = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
CNPJ_SECOND_WEIGHTS = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]


def clean_cnpj(cnpj):
    """Takes a CNPJ and turns it into a string of only numbers."""
    return NONDIGIT.sub('', str(cnpj))

def validate_cnpj(cnpj):
    """Check whether CNPJ is valid."""
    cnpj = clean_cnpj(cnpj)
    # all complete CNPJ are 14 digits long
    if len(cnpj) != 14:
        return False
    checks = [int(k) for k in cnpj[12:]]  # check digits
    digits = [int(k) for k in cnpj[:13]]  # identifier digits
    # validate the first check digit
    cs = sum([mul(*k) for k in zip(CNPJ_FIRST_WEIGHTS, digits[:-1])]) % 11
    cs = 0 if cs < 2 else 11 - cs
    if cs != checks[0]:
        return False  # first check digit is not correct
    # validate the second check digit
    cs = sum([mul(*k) for k in zip(CNPJ_SECOND_WEIGHTS, digits)]) % 11
    cs = 0 if cs < 2 else 11 - cs
    if cs != checks[1]:
        return False  # second check digit is not correct
    # both check digits are correct
    return True

def cnpj_check_digits(cnpj):
    """Find two check digits needed to make a CNPJ valid."""
    cnpj = clean_cnpj(cnpj)
    if len(cnpj) < 12:
        raise ValueError('CNPJ must have at least 12 digits: {0}'.format(cnpj))
    digits = [int(k) for k in cnpj[:13]]
    # find the first check digit
    cs = sum([mul(*k) for k in zip(CNPJ_FIRST_WEIGHTS, digits)]) % 11
    check = 0 if cs < 2 else 11 - cs
    # find the second check digit
    digits.append(check)
    cs = sum([mul(*k) for k in zip(CNPJ_SECOND_WEIGHTS, digits)]) % 11
    if cs < 2:
        return check, 0
    return check, 11 - cs

def cnpj_from_firm_id(firm, establishment='0001'):
    """Takes first 8 digits of a CNPJ (firm identifier) and builds a valid,
       complete CNPJ by appending an establishment identifier and calculating
       necessary check digits.
    """
    cnpj = clean_cnpj('{0}{1}'.format(firm, establishment))
    checks = ''.join([str(k) for k in cnpj_check_digits(cnpj)])
    return cnpj + checks

def format_cnpj(cnpj):
    """Applies typical 00.000.000/0000-00 formatting to CNPJ."""
    fmt = '{0}.{1}.{2}/{3}-{4}'
    cnpj = clean_cnpj(cnpj)
    return fmt.format(cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:])

def pad_cnpj(cnpj, validate=True):
    """Takes a CNPJ that probably had leading zeros and pads it."""
    cnpj = clean_cnpj(cnpj)
    cnpj = '%0.014i' % int(cnpj)
    if validate and not validate_cnpj(cnpj):
        raise ValueError('Invalid CNPJ: {0}'.format(cnpj))
    return cnpj

def random_cnpj(formatted=True):
    """Create a random, valid CNPJ identifier."""
    firm = random.randint(10000000, 99999999)
    establishment = random.choice(['0001', '0002', '0003', '0004', '0005'])
    cnpj = cnpj_from_firm_id(firm, establishment)
    if formatted:
        return format_cnpj(cnpj)
    return cnpj

