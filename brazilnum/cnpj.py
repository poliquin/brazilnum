#!/usr/bin/env python

import re
import random
import string
from collections import namedtuple

from .util import clean_alphanumeric_id, is_missing, pad_id, pad_alphanumeric_id

"""
Functions for working with Brazilian company identifiers (CNPJ).

"""

CNPJ_FIRST_WEIGHTS = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
CNPJ_SECOND_WEIGHTS = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

# CNPJ may contain letters in the first 12 positions (IN RFB nº 2.229/2024),
# but the two check digits are always numeric
CNPJ_PATTERN = re.compile(r'^[0-9A-Z]{12}[0-9]{2}$')

CNPJ = namedtuple('CNPJ', ['cnpj', 'firm', 'establishment', 'check', 'valid'])


def _char_value(c):
    """Value of a character for check-digit calculation: ord(c) - 48.
    Digits 0-9 -> 0-9 (same as the plain numeric value).
    Letters A-Z -> 17-42 (alphanumeric CNPJ, RFB, from 07/2026).
    """
    return ord(c) - 48


def validate_cnpj(cnpj, autopad=True):
    """Check whether CNPJ is valid. Optionally pad if too short.

    Accepts both the legacy numeric-only CNPJ and the new alphanumeric
    CNPJ format introduced by Receita Federal (Instrução Normativa RFB
    nº 2.229/2024), effective from 07/2026.

    Missing values (None or NaN) are considered invalid; other non-str,
    non-int input raises TypeError.
    """
    if is_missing(cnpj):
        return False
    cnpj = clean_alphanumeric_id(cnpj)

    # all complete CNPJ are 14 characters long
    if len(cnpj) < 14:
        if not autopad:
            return False
        cnpj = pad_cnpj(cnpj)

    elif len(cnpj) > 14:
        return False

    # first 12 positions: digits or A-Z letters; last 2 (check digits):
    # always numeric
    if not CNPJ_PATTERN.match(cnpj):
        return False

    # 0 is invalid; smallest valid numeric CNPJ is 191
    if cnpj == '00000000000000':
        return False

    values = [_char_value(k) for k in cnpj[:13]]  # 12 identifier chars + DV1
    # validate the first check digit
    cs = sum(w * v for w, v in zip(CNPJ_FIRST_WEIGHTS, values[:-1])) % 11
    cs = 0 if cs < 2 else 11 - cs
    if cs != int(cnpj[12]):
        return False  # first check digit is not correct
    # validate the second check digit
    cs = sum(w * v for w, v in zip(CNPJ_SECOND_WEIGHTS, values)) % 11
    cs = 0 if cs < 2 else 11 - cs
    if cs != int(cnpj[13]):
        return False  # second check digit is not correct
    # both check digits are correct
    return True


def cnpj_check_digits(cnpj):
    """Find two check digits needed to make a CNPJ valid."""
    cnpj = clean_alphanumeric_id(cnpj)
    if len(cnpj) < 12:
        raise ValueError('CNPJ must have at least 12 characters: {0}'.format(cnpj))
    values = [_char_value(k) for k in cnpj[:13]]
    # find the first check digit
    cs = sum(w * v for w, v in zip(CNPJ_FIRST_WEIGHTS, values)) % 11
    check = 0 if cs < 2 else 11 - cs
    # find the second check digit
    values.append(check)
    cs = sum(w * v for w, v in zip(CNPJ_SECOND_WEIGHTS, values)) % 11
    if cs < 2:
        return check, 0
    return check, 11 - cs


def cnpj_from_firm_id(firm, establishment='0001', formatted=False):
    """Takes first 8 characters of a CNPJ (firm identifier) and builds a
       valid, complete CNPJ by appending an establishment identifier and
       calculating necessary check digits.
    """
    cnpj = clean_alphanumeric_id('{0}{1}'.format(firm, establishment))
    checks = ''.join([str(k) for k in cnpj_check_digits(cnpj)])
    if not formatted:
        return cnpj + checks
    else:
        return format_cnpj(cnpj + checks)


def format_cnpj(cnpj):
    """Applies typical 00.000.000/0000-00 formatting to CNPJ."""
    cnpj = pad_cnpj(cnpj)
    fmt = '{0}.{1}.{2}/{3}-{4}'
    return fmt.format(cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:])


def pad_cnpj(cnpj, validate=False):
    """Takes a CNPJ and pads it with leading zeros.

    Supports both the legacy fully-numeric CNPJ (padded via pad_id, for
    backwards compatibility) and the new alphanumeric CNPJ format, which
    is padded as a string since it may contain letters.
    """
    if clean_alphanumeric_id(cnpj).isdigit():
        padded = pad_id(cnpj, '%0.014i')
    else:
        padded = pad_alphanumeric_id(cnpj, 14)

    if validate:
        return padded, validate_cnpj(padded)
    return padded


def parse_cnpj(cnpj, formatted=True):
    """Split CNPJ into firm, establishment, and check digits, and validate.

    With formatted=False, fully numeric CNPJ are returned as integers for
    backwards compatibility, while alphanumeric CNPJ are returned as
    strings. Check digits are always numeric and returned as integers.
    """
    cnpj, valid = pad_cnpj(cnpj, validate=True)
    estbl, check = cnpj[8:12], cnpj[12:]
    if formatted:
        cnpj = format_cnpj(cnpj)
        firm = cnpj[:10]
        return CNPJ(cnpj, firm, estbl, check, valid)
    else:
        firm = cnpj[:8]
        check = tuple(int(k) for k in check)  # check digits are always numeric
        if cnpj.isdigit():
            return CNPJ(int(cnpj), int(firm), int(estbl), check, valid)
        return CNPJ(cnpj, firm, estbl, check, valid)


def random_cnpj(formatted=True, alphanumeric=False):
    """Create a random, valid CNPJ identifier.

    With alphanumeric=True, the identifier follows the alphanumeric CNPJ
    format issued by Receita Federal starting in July 2026.
    """
    if alphanumeric:
        chars = string.digits + string.ascii_uppercase
        firm = ''.join(random.choice(chars) for _ in range(8))
        establishment = ''.join(random.choice(chars) for _ in range(4))
    else:
        firm = random.randint(10000000, 99999999)
        establishment = random.choice(['0001', '0002', '0003', '0004', '0005'])
    cnpj = cnpj_from_firm_id(firm, establishment)
    if formatted:
        return format_cnpj(cnpj)
    return cnpj
