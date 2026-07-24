
import pytest
from brazilnum import cnpj
from brazilnum.cnpj import CNPJ


def test_validate_cnpj():
    """Check validation of CNPJ identifiers."""

    # confirm a few complete, valid CNPJs
    assert cnpj.validate_cnpj('00360305000104') is True
    assert cnpj.validate_cnpj('00034616000183') is True
    assert cnpj.validate_cnpj('11277555000100') is True

    # check a few complete, invalid CNPJs
    assert cnpj.validate_cnpj('08173643000263') is False
    assert cnpj.validate_cnpj('76694959000241') is False
    assert cnpj.validate_cnpj('00070221000292') is False

    # should also work by default without leading zeros
    assert cnpj.validate_cnpj('360305000104') is True
    assert cnpj.validate_cnpj('70221000292') is False

    # and when argument is an integer
    assert cnpj.validate_cnpj(34616000183) is True
    assert cnpj.validate_cnpj(11277555000100) is True
    assert cnpj.validate_cnpj(76694959000241) is False
    assert cnpj.validate_cnpj(70221000292) is False

    # zero and empty strings are not valid
    assert cnpj.validate_cnpj(0) is False
    assert cnpj.validate_cnpj('0') is False
    assert cnpj.validate_cnpj('') is False


def test_validate_cnpj_bad_input():
    """Check handling of missing values and unsupported input types."""

    # None and NaN mark missing identifiers in a data stream, which can
    # happen when using the package correctly, so they are just invalid
    assert cnpj.validate_cnpj(None) is False
    assert cnpj.validate_cnpj(float('nan')) is False

    # any other unsupported type suggests an upstream problem with the
    # caller's data, so it raises an error instead of returning False
    for bad in (2558157000162.0, 12.34, True, b'02558157000162', []):
        with pytest.raises(TypeError, match=r"must be str or int"):
            cnpj.validate_cnpj(bad)

    # missing values cannot be formatted, padded, or parsed
    with pytest.raises(TypeError, match=r"must be str or int"):
        cnpj.format_cnpj(None)

    with pytest.raises(TypeError, match=r"must be str or int"):
        cnpj.parse_cnpj(float('nan'))

    with pytest.raises(TypeError, match=r"must be str or int"):
        cnpj.cnpj_check_digits(None)


def test_validate_cnpj_alphanumeric():
    """Check validation of alphanumeric CNPJ identifiers (RFB, 07/2026)."""

    assert cnpj.validate_cnpj('XPB30AW3000184') is True
    assert cnpj.validate_cnpj('XP.B30.AW3/0001-84') is True

    # lowercase letters are normalized to uppercase
    assert cnpj.validate_cnpj('xp.b30.aw3/0001-84') is True

    # incorrect check digits are detected
    assert cnpj.validate_cnpj('XPB30AW3000185') is False

    # the two check digits are always numeric, never letters
    assert cnpj.validate_cnpj('XPB30AW30001AB') is False

    # short alphanumeric identifiers are padded with leading zeros
    assert cnpj.validate_cnpj('PB3AW3W000133') is True
    assert cnpj.validate_cnpj('PB3AW3W000133', autopad=False) is False

    # because CNPJ can contain letters, stray letters in the input make
    # an identifier invalid as of version 0.9.0
    assert cnpj.validate_cnpj('CNPJ: 02.558.157/0001-62') is False


def test_cnpj_check_digits():
    """Test calculation of check digits for a CNPJ identifier."""

    # CNPJ identifiers have two check digits
    assert cnpj.cnpj_check_digits('00360305000104') == (0, 4)
    assert cnpj.cnpj_check_digits('00034616000183') == (8, 3)
    assert cnpj.cnpj_check_digits('11277555000100') == (0, 0)

    # also works when only given the first 12 digits
    assert cnpj.cnpj_check_digits('003603050001') == (0, 4)
    assert cnpj.cnpj_check_digits('000346160001') == (8, 3)
    assert cnpj.cnpj_check_digits(112775550001) == (0, 0)

    # check digits for alphanumeric CNPJ are still numeric
    assert cnpj.cnpj_check_digits('XPB30AW30001') == (8, 4)

    # identifiers less than 12 characters produce an error
    with pytest.raises(ValueError, match=r".*12 characters.*"):
        cnpj.cnpj_check_digits('50001')


def test_cnpj_from_firm_id():
    """Test construction of full CNPJ from the firm-level CNPJ."""

    assert cnpj.cnpj_from_firm_id(
        '02341506', establishment='0002'
    ) == '02341506000270'

    # can also return formatted identifiers
    assert cnpj.cnpj_from_firm_id(
        '02341506', establishment='0002', formatted=True
    ) == '02.341.506/0002-70'

    # firm identifiers can be alphanumeric
    assert cnpj.cnpj_from_firm_id('XPB30AW3') == 'XPB30AW3000184'


def test_format_cnpj():
    """Test 00.000.000/0000-00 formatting of CNPJ."""

    # confirm a few complete, valid CNPJs
    assert cnpj.format_cnpj('00360305000104') == '00.360.305/0001-04'
    assert cnpj.format_cnpj('11277555000100') == '11.277.555/0001-00'

    # formatting does not validate; invalid CNPJs will be formatted
    assert cnpj.format_cnpj('08173643000263') == '08.173.643/0002-63'

    # can format integers
    assert cnpj.format_cnpj(11277555000100) == '11.277.555/0001-00'

    # can format alphanumeric identifiers
    assert cnpj.format_cnpj('XPB30AW3000184') == 'XP.B30.AW3/0001-84'


def test_pad_cnpj():
    """Test padding CNPJ with leading zeros."""

    assert cnpj.pad_cnpj('00360305000104') == '00360305000104'
    assert cnpj.pad_cnpj('360305000104')   == '00360305000104'
    assert cnpj.pad_cnpj(360305000104)     == '00360305000104'

    assert cnpj.pad_cnpj('11277555000100') == '11277555000100'
    assert cnpj.pad_cnpj(11277555000100)   == '11277555000100'

    # padding does not validate; invalid CNPJ will be padded OK
    assert cnpj.pad_cnpj('08173643000263') == '08173643000263'
    assert cnpj.pad_cnpj('8173643000263')  == '08173643000263'
    assert cnpj.pad_cnpj(8173643000263)    == '08173643000263'

    # alphanumeric identifiers are padded as strings
    assert cnpj.pad_cnpj('PB3AW3W000133') == '0PB3AW3W000133'

    # can pad and validate in one step
    assert cnpj.pad_cnpj(360305000104, validate=True) == (
        '00360305000104', True
    )
    assert cnpj.pad_cnpj(8173643000263, validate=True) == (
        '08173643000263', False
    )


def test_parse_cnpj():
    """Test parsing of CNPJ into components."""

    assert cnpj.parse_cnpj('00034616000183') == CNPJ(
        '00.034.616/0001-83', '00.034.616', '0001', '83', True
    )
    assert cnpj.parse_cnpj('00034616000183', formatted=False) == CNPJ(
        34616000183, 34616, 1, (8, 3), True
    )

    # when CNPJ is invalid, function does not "fix" the check digits
    assert cnpj.parse_cnpj('76694959000241') == CNPJ(
        '76.694.959/0002-41', '76.694.959', '0002', '41', False
    )
    assert cnpj.parse_cnpj('76694959000241', formatted=False) == CNPJ(
        76694959000241, 76694959, 2, (4, 1), False
    )

    # alphanumeric CNPJ cannot be represented as integers, so components
    # are strings even with formatted=False; check digits remain integers
    assert cnpj.parse_cnpj('XPB30AW3000184') == CNPJ(
        'XP.B30.AW3/0001-84', 'XP.B30.AW3', '0001', '84', True
    )
    assert cnpj.parse_cnpj('XPB30AW3000184', formatted=False) == CNPJ(
        'XPB30AW3000184', 'XPB30AW3', '0001', (8, 4), True
    )


def test_random_cnpj():
    """Test generation of random, valid CNPJ."""

    for i in range(10):
        assert cnpj.validate_cnpj(cnpj.random_cnpj()) is True
        assert cnpj.validate_cnpj(cnpj.random_cnpj(formatted=True)) is True
        assert cnpj.validate_cnpj(cnpj.random_cnpj(formatted=False)) is True
        assert cnpj.validate_cnpj(cnpj.random_cnpj(alphanumeric=True)) is True

    assert isinstance(cnpj.random_cnpj(), str) is True
    assert isinstance(cnpj.random_cnpj(formatted=False), str) is True
