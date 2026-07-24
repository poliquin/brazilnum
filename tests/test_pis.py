
import pytest
from brazilnum import pis


def test_validate_pis():
    """Check validation of PIS/PASEP identifiers."""

    # confirm a few complete, valid PIS/PASEP
    assert pis.validate_pis('12536026320') is True
    assert pis.validate_pis('12582456162') is True
    assert pis.validate_pis('12571160380') is True

    # check a few complete, invalid PIS/PASEP
    assert pis.validate_pis('12536026321') is False
    assert pis.validate_pis('12582456163') is False
    assert pis.validate_pis('12571160381') is False

    # formatted input is also fine
    assert pis.validate_pis('125.6124.131-0') is True
    assert pis.validate_pis('111.6124.131-0') is False

    # should also work by default without leading zeros
    assert pis.validate_pis('1253602632', autopad=False) is False

    # and when argument is an integer
    assert pis.validate_pis(12536026320) is True
    assert pis.validate_pis(12536026321) is False

    # identifiers longer than 11 digits are not valid
    assert pis.validate_pis('12536026320999') is False

    # zero and empty strings are not valid
    assert pis.validate_pis(0) is False
    assert pis.validate_pis('0') is False
    assert pis.validate_pis('') is False


def test_validate_pis_bad_input():
    """Check handling of missing values and unsupported input types."""

    # missing identifiers are invalid, not an error
    assert pis.validate_pis(None) is False
    assert pis.validate_pis(float('nan')) is False

    # other unsupported types raise an error
    for bad in (12536026320.0, 12.34, True, b'12536026320', []):
        with pytest.raises(TypeError, match=r"must be str or int"):
            pis.validate_pis(bad)

    # missing values cannot be formatted
    with pytest.raises(TypeError, match=r"must be str or int"):
        pis.format_pis(None)


def test_pis_check_digit():
    """Test calculation of check digit for a PIS/PASEP identifier."""

    # PIS/PASEP identifiers have a single check digit
    assert pis.pis_check_digit('12536026320') == 0
    assert pis.pis_check_digit('125.6124.131-0') == 0

    # also works when only given the first 10 digits
    assert pis.pis_check_digit('1253602632') == 0
    assert pis.pis_check_digit('1256124131') == 0

    # the plural alias works the same way
    assert pis.pis_check_digits('1253602632') == 0

    # identifiers less than 10 digits produce an error
    with pytest.raises(ValueError, match=r".*10 digits.*"):
        pis.pis_check_digit('602632')


def test_format_pis():
    """Test 000.0000.000-0 formatting of PIS/PASEP."""

    assert pis.format_pis('12536026320') == '125.3602.632-0'
    assert pis.format_pis('12561241310') == '125.6124.131-0'

    # formatting pads integers that lost leading zeros
    assert pis.format_pis(1253602632) == '012.5360.263-2'

    # formatting does not validate; invalid PIS/PASEP will be formatted
    assert pis.format_pis('12536026321') == '125.3602.632-1'


def test_pad_pis():
    """Test padding PIS/PASEP with leading zeros."""

    assert pis.pad_pis('12536026320') == '12536026320'
    assert pis.pad_pis('2536026320')  == '02536026320'
    assert pis.pad_pis(2536026320)    == '02536026320'

    # can pad and validate in one step
    assert pis.pad_pis(12536026320, validate=True) == ('12536026320', True)
    assert pis.pad_pis(12536026321, validate=True) == ('12536026321', False)


def test_random_pis():
    """Test generation of random, valid PIS/PASEP."""

    for i in range(10):
        assert pis.validate_pis(pis.random_pis()) is True
        assert pis.validate_pis(pis.random_pis(formatted=False)) is True

    assert isinstance(pis.random_pis(), str) is True
    assert isinstance(pis.random_pis(formatted=False), str) is True
