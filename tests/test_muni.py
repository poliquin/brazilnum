
import pytest
from brazilnum import muni


def test_validate_muni():
    """Check validation of IBGE municipio codes."""

    # confirm a few real municipio codes
    assert muni.validate_muni(3550308) is True   # São Paulo, SP
    assert muni.validate_muni('3550308') is True
    assert muni.validate_muni(1100015) is True   # Alta Floresta D'Oeste, RO
    assert muni.validate_muni(1100023) is True   # Ariquemes, RO

    # codes with incorrect check digits are detected
    assert muni.validate_muni(2100015) is False
    assert muni.validate_muni(2100023) is False
    assert muni.validate_muni(3550309) is False

    # municipal codes must be exactly 7 digits, no autopadding
    assert muni.validate_muni('355030') is False
    assert muni.validate_muni('35503080') is False

    # municipal codes cannot start with zero
    assert muni.validate_muni('0550308') is False


def test_validate_muni_bad_input():
    """Check handling of missing values and unsupported input types."""

    # missing identifiers are invalid, not an error
    assert muni.validate_muni(None) is False
    assert muni.validate_muni(float('nan')) is False

    # other unsupported types raise an error
    for bad in (3550308.0, 12.34, True, b'3550308', []):
        with pytest.raises(TypeError, match=r"must be str or int"):
            muni.validate_muni(bad)

    # missing values have no check digit
    with pytest.raises(TypeError, match=r"must be str or int"):
        muni.muni_check_digit(None)


def test_validate_muni_exceptions():
    """Check the 9 real municipio codes with invalid check digits."""

    # these codes do not follow the verification pattern but are real,
    # so they are validated against an exceptions list; see
    # http://www.sefaz.al.gov.br/nfe/notas_tecnicas/NT2008.004.pdf
    for code in muni.SHIM:
        assert muni.validate_muni(code) is True

    # e.g. Coronel Barros, RS
    assert muni.validate_muni(4305871) is True


def test_muni_check_digit():
    """Test calculation of check digit for a municipio code."""

    assert muni.muni_check_digit('355030') == 8   # São Paulo, SP
    assert muni.muni_check_digit('3550308') == 8

    # exceptional codes return their real, nonconforming check digit,
    # but only when the full 7-digit code is given
    assert muni.muni_check_digit('4305871') == 1  # Coronel Barros, RS
    assert muni.muni_check_digit('430587') == 6

    # codes less than 6 digits produce an error
    with pytest.raises(ValueError, match=r".*6 digits.*"):
        muni.muni_check_digit('55030')
