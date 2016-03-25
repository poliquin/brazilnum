Validate Brazilian Identification Numbers
=========================================

Python functions for working with CNPJ, CEI, CPF, PIS/PASEP, CEP, and município
numbers, which identify firms, people, and places in Brazil.

Installation
------------

    pip install brazilnum

Usage Examples
--------------

Works with Python 2.7 and 3.


#### Validation Functions
Validate a CNPJ number for a firm, in this case Telefônica Brasil:

    >>> from brazilnum.cnpj import validate_cnpj
    >>> validate_cnpj('02.558.157/0001-62')
    True
    >>> validate_cnpj('02.558.157/0001-55')
    False

Integer input that is too short due to missing zeros is auto-corrected:

    >>> validate_cnpj(2558157000162)
    True
    >>> validate_cnpj(2558157000162, autopad=False)
    False

Validate a CEI number, used for businesses that do not require a CNPJ:

    >>> from brazilnum.cei import validate_cei
    >>> validate_cei('11.583.00249/85')
    True
    >>> validate_cei('11.583.00249/84')
    False
    >>> validate_cei(115830024985)
    True

Validate CPF and PIS/PASEP numbers for individuals:

    >>> from brazilnum.pis import validate_pis
    >>> validate_pis('125.6124.131-0')
    True
    >>> validate_pis('111.6124.131-0')
    False

    >>> from brazilnum.cpf import validate_cpf
    >>> validate_cpf('968.811.342-58')
    True
    >>> validate_cpf('327.861.067-97')
    False

Validation functions work with integer and unformatted input:

    >>> validate_pis(12561241310)
    True
    >>> validate_cpf(96881134258)
    True
    >>> validate_pis('12561241310')
    True
    >>> validate_cpf('32786106797')
    False


#### Formatting and Padding
Use the format function when displaying identifiers:

    >>> from brazilnum.cnpj import format_cnpj
    >>> format_cnpj('02558157000162')
    '02.558.157/0001-62'

    >>> from brazilnum.cei import format_cei
    >>> format_cei('115830024985')
    '11.583.00249/85'

    >>> from brazilnum.pis import format_pis
    >>> format_pis('12561241310')
    '125.6124.131-0'

    >>> from brazilnum.cpf import format_cpf
    >>> format_cpf('96881134258')
    '968.811.342-58'

There is a helper function to remove formatting from identifiers; it always
returns a string:

    >>> from brazilnum.util import clean_id
    >>> clean_id('02.558.157/0001-62')
    '02558157000162'

    >>> clean_id(115830024985)
    '115830024985'

Your data source probably stores identifiers as integers, so leading
zeros are missing. You can pad and validate these in one step:

    >>> from brazilnum.cnpj import pad_cnpj
    >>> pad_cnpj(2558157000162, validate=True)
    ('02558157000162', True)

    >>> pad_cnpj(2558157000155, validate=True)
    ('02558157000155', False)

    >>> from brazilnum.cei import pad_cei
    >>> pad_cei(115830024985, validate=True)
    ('115830024985', True)

You can skip the validation step:

    >>> pad_cnpj(2558157000155, validate=False)
    '02558157000155'

Padding works the same way for PIS/PASEP and CPF numbers:

    >>> from brazilnum.pis import pad_pis
    >>> pad_pis(12561241310, validate=True)
    ('12561241310', True)

    >>> pad_pis(11161241310, validate=True)
    ('11161241310', False)

    >>> from brazilnum.cpf import pad_cpf
    >>> pad_cpf(4193675866, validate=True)
    ('04193675866', True)

    >>> pad_cpf(4193675867, validate=True)
    ('04193675867', False)


#### CNPJ Parsing
The first 8 digits of CNPJs identify a firm, and the following 4 digits
identify a specific business establishment owned by that firm.  Headquarters is
often establishment 0001.  The ``cnpj_from_firm_id`` function will create a
full CNPJ from the first 8 digits and a given establishment number:

    >>> from brazilnum.cnpj import cnpj_from_firm_id
    >>> cnpj_from_firm_id('02.558.157')
    '02558157000162'

    >>> cnpj_from_firm_id('02.558.157', establishment='0002')
    '02558157000243'

    >>> cnpj_from_firm_id('02.558.157', establishment='0002', formatted=True)
    '02.558.157/0002-43'


CNPJ can be parsed into firm, establishment, and check digit components:

    >>> from brazilnum.cnpj import parse_cnpj
    >>> parse_cnpj('02.558.157/0001-62')
    CNPJ(cnpj='02.558.157/0001-62', firm='02.558.157', establishment='0001', check='62', valid=True)

    >>> parse_cnpj('02.558.157/0001-62', formatted=False)
    CNPJ(cnpj=2558157000162, firm=2558157, establishment=1, check=(6, 2), valid=True)


#### CEP Parsing

Códigos de Endereçamentos Postais (zip codes) can be formatted and parsed:

    >>> from brazilnum.cep import format_cep, parse_cep
    >>> format_cep(13165000)
    '13165-000'

    >>> format_cep(1002010)
    '01002-010'

    >>> format_cep(73080)
    '73080-000'

    >>> parse_cep('01255-080', numeric=True)
    CEP(cep=1255080, region=0, subregion=1, sector=12, subsector=125, division=1255, suffix=80)

    >>> parse_cep('01255-080', numeric=False)
    CEP(cep='01255-080', region='0', subregion='01', sector='012', subsector='0125', division='01255', suffix='080')

Correios has more information about the [structure of CEP](http://www.correios.com.br/para-voce/precisa-de-ajuda/o-que-e-cep-e-por-que-usa-lo/estrutura-do-cep).


#### Municípios (Municipalities)

Validation of IBGE município (municipal) identifiers is also possible:

    >>> from brazilnum.muni import validate_muni
    >>> validate_muni(3550308)  # São Paulo
    True

    >>> validate_muni(4305871)  # Coronel Barros (see note below)
    True

**Note** that 9 true codes do not follow the correct verification pattern. ENCAT
has a [technical note](http://www.sefaz.al.gov.br/nfe/notas_tecnicas/NT2008.004.pdf)
about this issue. The program correctly handles special codes like Coronel
Barros, RS (see above).

If you need a list of municípios with names and coordinates, see
[poliquin/br-localidades](https://github.com/poliquin/br-localidades). If you
need historical and current codes with names, see
[paulofreitas/dtb-ibge](https://github.com/paulofreitas/dtb-ibge).


#### Random Identifiers
If you need random CNPJ for database testing, use the ``random_cnpj`` function,
which can return either unformatted or formatted identifiers:

    from brazilnum.cnpj import random_cnpj
    random_cnpj()       # for a random, formatted CNPJ
    random_cnpj(False)  # for a random, unformatted CNPJ

Use ``random_cei`` for random CEI identifiers:

    from brazilnum.cei import random_cei
    random_cei()

The same thing exists for PIS/PASEP and CPF identifiers:

    from brazilnum.pis import random_pis
    random_pis()

    from brazilnum.cpf import random_cpf
    random_cpf()


#### Check Digits
If you're interested in the check digits, there are functions for
calculating them that return integers:

    >>> from brazilnum.cnpj import cnpj_check_digits
    >>> cnpj_check_digits('02.558.157/0001-62')
    (6, 2)

    >>> from brazilnum.cei import cei_check_digit
    >>> cei_check_digit('11.583.00249/85')
    5

    >>> from brazilnum.cpf import cpf_check_digits
    >>> cpf_check_digits('041.936.758-66')
    (6, 6)

    >>> from brazilnum.pis import pis_check_digit
    >>> pis_check_digit('125.6124.131-0')
    0

CNPJ check digits are calculated from the first 12 digits:

    >>> cnpj_check_digits('025581570001')
    (6, 2)

The CEI check digit is calculated from the first 11 digits:

    >>> cei_check_digit('11583002498')
    5

CPF check digits are calculated from the first 9 digits:

    >>> cpf_check_digits('041936758')
    (6, 6)

The PIS/PASEP check digit is calculated from the first 10 digits:

    >>> pis_check_digit('1256124131')
    0
