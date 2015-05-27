#!/usr/bin/env python

from __future__ import print_function
import sys
import timeit
import csv

sys.path.append('..')
from brazilnum.cnpj import validate_cnpj, parse_cnpj, pad_cnpj
from brazilnum.pis import validate_pis, pad_pis
from brazilnum.cpf import validate_cpf, pad_cpf

"""
Test speed of CNPJ, CPF, and PIS/PASEP functions.

"""

# read sample of 200 CNPJ numbers (100 good)
with open('cnpj.csv', 'r') as fh:
    rdr = csv.DictReader(fh)
    CNPJ = list(rdr)
    fh.close()

# read sample of 200 fake PIS/PASEP numbers (100 good)
with open('pis.csv', 'r') as fh:
    rdr = csv.DictReader(fh)
    PIS = list(rdr)
    fh.close()

# read sample of 200 fake CPF numbers (100 good)
with open('cpf.csv', 'r') as fh:
    rdr = csv.DictReader(fh)
    CPF = list(rdr)
    fh.close()


def cnpj_speed():
    """Check speed of validating 200 CNPJ, 100 invalid."""
    for c in CNPJ:
        try:
            assert int(c['good']) == validate_cnpj(c['cnpj'])
        except:
            print('CNPJ Validation failed: {0}'.format(c['cnpj']))


def pis_speed():
    """Check speed of validating 200 fake PIS/PASEP numbers, 100 invalid."""
    for c in PIS:
        try:
            assert int(c['good']) == validate_pis(c['pis'])
        except:
            print('PIS/PASEP Validation failed: {0}'.format(c['pis']))


def cpf_speed():
    """Check speed of validating 200 fake CPF numbers, 100 invalid."""
    for c in CPF:
        try:
            assert int(c['good']) == validate_cpf(c['cpf'])
        except:
            print('CPF Validation failed: {0}'.format(c['cpf']))


reps = 1000

# time validation of CNPJ, 100 good and 100 bad
cnpj_time = timeit.timeit(cnpj_speed, number=reps)
time_per_thousand_cnpj = (cnpj_time / (200. * reps)) * 1000.

print('Validate 1,000 CNPJ: {0} seconds'.format(time_per_thousand_cnpj))


# time validation of PIS/PASEP, 100 good and 100 bad
pis_time = timeit.timeit(pis_speed, number=reps)
time_per_thousand_pis = (pis_time / (200. * reps)) * 1000.

print('Validate 1,000 PIS/PASEP: {0} seconds'.format(time_per_thousand_pis))


# time validation of CPF, 100 good and 100 bad
cpf_time = timeit.timeit(cpf_speed, number=reps)
time_per_thousand_cpf = (cpf_time / (200. * reps)) * 1000.

print('Validate 1,000 CPF: {0} seconds'.format(time_per_thousand_cpf))


# time parsing of CNPJ
def parse_cnpj_speed():
    """Parse CNPJ read from file."""
    for i in CNPJ:
        parse_cnpj(int(i['cnpj']))


cnpj_parse_time = timeit.timeit(parse_cnpj_speed, number=reps)
print('Parse 200 CNPJ: {0} seconds'.format(cnpj_parse_time))


# time padding of all identifiers
def pad_speed():
    """Pad integer identifiers."""
    for i in CNPJ:
        pad_cnpj(int(i['cnpj']), validate=False)
    for i in PIS:
        pad_pis(int(i['pis']), validate=False)
    for i in CPF:
        pad_cpf(int(i['cpf']), validate=False)


pad_time = timeit.timeit(pad_speed, number=reps)
print('Pad identifiers: {0} seconds'.format(pad_time))
