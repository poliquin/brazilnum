# -*- coding: utf8 -*-

from distutils.core import setup

setup(
    name='brazilnum',
    packages=['brazilnum'],
    version='0.8.8',
    description="Validate Brazilian CNPJ, CEI, CPF, PIS/PASEP, CEP, and municipal numbers",
    author='Chris Poliquin',
    author_email='cpoliquin@hbs.edu',
    url='https://github.com/poliquin/brazilnum',
    keywords=['brazil', 'brasil', 'cnpj', 'cei', 'cpf', 'pis', 'pasep', 'cep'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Utilities'
        ],
    long_description="""\
Validate and Parse Brazilian Identification Numbers
---------------------------------------------------

Python functions for working with CNPJ, CEI, CPF, PIS/PASEP, CEP, and municipal
(município) codes, which identify firms, people, and places in Brazil.
"""
)
