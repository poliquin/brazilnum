from distutils.core import setup

setup(
        name = 'brazilnum',
        packages = ['brazilnum'],
        version = '0.6.1',
        description = 'Validators for Brazilian CNPJ, CPF, and PIS/PASEP numbers.',
        author = 'Chris Poliquin',
        author_email = 'cpoliquin@hbs.edu',
        url = 'https://github.com/poliquin/brazilnum',
        keywords = ['brazil', 'cnpj', 'cpf', 'pis', 'pasep'],
        classifiers = [
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Utilities'
            ],
        long_description = """\
Validate Brazilian Identification Numbers
-----------------------------------------

Python functions for working with CNPJ, CPF, and PIS/PASEP numbers,
which identify firms and people in Brazil.
"""
)


