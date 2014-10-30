#!/usr/bin/env python

import timeit
import csv

from brazilnum.cnpj import validate_cnpj
from brazilnum.pis import validate_pis

"""
Test speed of CNPJ and PIS/PASEP functions.

"""

# read sample of 200 CNPJ numbers (100 good)
with open('test/cnpj.csv', 'r') as fh:
    rdr = csv.DictReader(fh)
    CNPJ = list(rdr)
    fh.close()

# read sample of 200 fake PIS/PASEP numbers (100 good)
with open('test/pis.csv', 'r') as fh:
    rdr = csv.DictReader(fh)
    PIS = list(rdr)
    fh.close()

def cnpj_speed():
    """Check speed of validating 200 CNPJ, 100 invalid."""
    for c in CNPJ:
        try:
            assert int(c['good']) == validate_cnpj(c['cnpj'])
        except:
            print 'CNPJ Validation failed: {0}'.format(c['cnpj'])

def pis_speed():
    """Check speed of validating 100 fake PIS/PASEP numbers."""
    for c in PIS:
        try:
            assert int(c['good']) == validate_pis(c['pis'])
        except:
            print c
            print 'PIS/PASEP Validation failed: {0}'.format(c['pis'])
            raise

reps = 1000

# time validation of CNPJ, 100 good and 100 bad
cnpj_time = timeit.timeit(cnpj_speed, number=reps)
time_per_thousand_cnpj = (cnpj_time / (200. * reps)) * 1000.

print 'Validate 1,000 CNPJ: {0} seconds'.format(time_per_thousand_cnpj)


# time validation of PIS/PASEP, 100 good and 100 bad
pis_time = timeit.timeit(pis_speed, number=reps)
time_per_thousand_pis = (pis_time / (200. * reps)) * 1000.

print 'Validate 1,000 PIS/PASEP: {0} seconds'.format(time_per_thousand_pis)

