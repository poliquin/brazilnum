#!/usr/bin/env python

import sys
import timeit
import csv

sys.path.append('..')
from brazilnum.cnpj import validate_cnpj, parse_cnpj, pad_cnpj
from brazilnum.pis import validate_pis, pad_pis
from brazilnum.cpf import validate_cpf, pad_cpf
from brazilnum.muni import validate_muni

"""
Test speed of CNPJ, CPF, PIS/PASEP, and municipio functions.

"""

# read sample of numeric and alphanumeric CNPJ, both valid and invalid
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

# read all municipio codes along with bad versions
with open('munis.csv', 'r') as fh:
    rdr = csv.DictReader(fh)
    MUNI = list(rdr)
    fh.close()


def cnpj_speed():
    """Check speed of validating sample CNPJ, valid and invalid."""
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


def muni_speed():
    """Check speed of validating all municipio numbers plus bad versions."""
    for m in MUNI:
        try:
            assert int(m['good']) == validate_muni(m['muni'])
        except:
            print('Municipio validation failed: {0}'.format(m['muni']))


reps = 1000

# time validation of CNPJ
cnpj_time = timeit.timeit(cnpj_speed, number=reps)
time_per_thousand_cnpj = (cnpj_time / (len(CNPJ) * reps)) * 1000.

print('Validate 1,000 CNPJ: {0} seconds'.format(time_per_thousand_cnpj))


# time validation of PIS/PASEP
pis_time = timeit.timeit(pis_speed, number=reps)
time_per_thousand_pis = (pis_time / (len(PIS) * reps)) * 1000.

print('Validate 1,000 PIS/PASEP: {0} seconds'.format(time_per_thousand_pis))


# time validation of CPF
cpf_time = timeit.timeit(cpf_speed, number=reps)
time_per_thousand_cpf = (cpf_time / (len(CPF) * reps)) * 1000.

print('Validate 1,000 CPF: {0} seconds'.format(time_per_thousand_cpf))


# time validation of municipios
muni_time = timeit.timeit(muni_speed, number=2)
print('Validate municipios: {0} seconds'.format(muni_time))


# time parsing of CNPJ
def parse_cnpj_speed():
    """Parse CNPJ read from file."""
    for i in CNPJ:
        # numeric CNPJ often arrive as integers from data files, but
        # alphanumeric CNPJ can only be strings
        c = i['cnpj']
        parse_cnpj(int(c) if c.isdigit() else c)


cnpj_parse_time = timeit.timeit(parse_cnpj_speed, number=reps)
print('Parse {0} CNPJ: {1} seconds'.format(len(CNPJ), cnpj_parse_time))


# time padding of all identifiers
def pad_speed():
    """Pad identifiers."""
    for i in CNPJ:
        c = i['cnpj']
        pad_cnpj(int(c) if c.isdigit() else c, validate=False)
    for i in PIS:
        pad_pis(int(i['pis']), validate=False)
    for i in CPF:
        pad_cpf(int(i['cpf']), validate=False)


pad_time = timeit.timeit(pad_speed, number=reps)
print('Pad identifiers: {0} seconds'.format(pad_time))
