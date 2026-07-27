#!/usr/bin/env python

import re
import random
from collections import namedtuple

from .util import clean_alphanumeric_id, is_missing, pad_id

"""
Functions for working with Registry of Economic Activities of Individuals (CAEPF).
"""

CAEPF_FIRST_WEIGHTS = [6, 7, 8, 9, 2, 3, 4, 5, 6, 7, 8, 9]
CAEPF_SECOND_WEIGHTS = [5, 6, 7, 8, 9, 2, 3, 4, 5, 6, 7, 8, 9]

CAEPF_PATTERN = re.compile(r"^[0-9]{12}[0-9]{2}$")

CAEPF = namedtuple("CAEPF", ["caepf", "cpf_root", "establishment", "check", "valid"])


def validate_caepf(caepf, autopad=True):
    """Check whether CAEPF is valid. Optionally pad if too short.

    Missing values (None or NaN) are considered invalid; other non-str,
    non-int input raises TypeError.
    """
    if is_missing(caepf):
        return False
    caepf = clean_alphanumeric_id(caepf)

    if len(caepf) < 14:
        if not autopad:
            return False
        caepf = pad_caepf(caepf)

    elif len(caepf) > 14:
        return False

    # first 12 positions: digits; last 2 (check digits):
    # always numeric
    if not CAEPF_PATTERN.match(caepf):
        return False

    # 0 is invalid; smallest valid numeric CAEPF is 100157
    if caepf == "00000000000000":
        return False

    try:
        expected_dv1, expected_dv2 = caepf_check_digits(caepf[:12])
    except ValueError:
        return False

    actual_dv1, actual_dv2 = int(caepf[12]), int(caepf[13])

    return actual_dv1 == expected_dv1 and actual_dv2 == expected_dv2


def caepf_check_digits(caepf):
    """Find two check digits needed to make a CAEPF valid."""
    caepf = clean_alphanumeric_id(caepf)
    if len(caepf) < 12:
        raise ValueError("CAEPF must have at least 12 characters: {0}".format(caepf))

    values = [int(k) for k in caepf[:12]]

    # first check digit
    cs1 = sum(w * v for w, v in zip(CAEPF_FIRST_WEIGHTS, values)) % 11
    dv1 = 0 if cs1 == 10 else cs1

    # second check digit
    values_second = values + [dv1]
    cs2 = sum(w * v for w, v in zip(CAEPF_SECOND_WEIGHTS, values_second)) % 11
    dv2 = 0 if cs2 == 10 else cs2

    # Ajust rule CAEPF + 12
    combined_dv = (dv1 * 10 + dv2) + 12
    if combined_dv > 99:
        combined_dv -= 100

    return combined_dv // 10, combined_dv % 10


def caepf_from_cpf_root(cpf_root, establishment="001", formatted=False):
    """Takes first 9 characters of a CAEPF (cpf root) and builds a
    valid, complete CAEPF by appending an establishment identifier and
    calculating necessary check digits.
    """
    caepf = "{0}{1}".format(cpf_root, establishment)
    checks = "".join([str(k) for k in caepf_check_digits(caepf)])
    if not formatted:
        return caepf + checks
    else:
        return format_caepf(caepf + checks)


def format_caepf(caepf):
    """Applies typical 000.000.000/000-00 formatting to CAEPF."""
    caepf = pad_caepf(caepf)
    fmt = "{0}.{1}.{2}/{3}-{4}"
    return fmt.format(caepf[:3], caepf[3:6], caepf[6:9], caepf[9:12], caepf[12:])


def pad_caepf(caepf, validate=False):
    """Takes a CAEPF and pads it with leading zeros."""
    padded = pad_id(caepf, "%0.014i")

    if validate:
        return padded, validate_caepf(padded)
    return padded


def parse_caepf(caepf, formatted=True):
    """Split CAEPF into cpf_root, establishment, and check digits, and validate."""
    caepf, valid = pad_caepf(caepf, validate=True)
    estbl, check = caepf[9:12], caepf[12:]
    if formatted:
        caepf = format_caepf(caepf)
        cpf_root = caepf[:11]
        return CAEPF(caepf, cpf_root, estbl, check, valid)
    else:
        cpf_root = caepf[:9]
        check = tuple(int(k) for k in check)
        return CAEPF(int(caepf), int(cpf_root), int(estbl), check, valid)


def random_caepf(formatted=True):
    """Create a random, valid CAEPF identifier."""
    cpf_root = random.randint(100000000, 999999999)
    establishment = random.choice(["001", "002", "003", "004", "005"])
    caepf = caepf_from_cpf_root(cpf_root, establishment)
    if formatted:
        return format_caepf(caepf)
    return caepf
