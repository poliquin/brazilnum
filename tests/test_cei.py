
import pytest
from brazilnum import cei


def test_validate_cei():
    """Check validation of CEI identifiers."""

    # confirm a valid CEI, formatted and unformatted
    assert cei.validate_cei('11.583.00249/85') is True
    assert cei.validate_cei('115830024985') is True

    # an incorrect check digit is detected
    assert cei.validate_cei('11.583.00249/84') is False
    assert cei.validate_cei('115830024984') is False

    # should also work when argument is an integer
    assert cei.validate_cei(115830024985) is True
    assert cei.validate_cei(115830024984) is False

    # identifiers longer than 12 digits are not valid
    assert cei.validate_cei('1158300249850') is False

    # short identifiers are padded with leading zeros by default
    assert cei.validate_cei('15830024985', autopad=False) is False

    # zero and empty strings are not valid
    assert cei.validate_cei(0) is False
    assert cei.validate_cei('0') is False
    assert cei.validate_cei('') is False


def test_validate_cei_bad_input():
    """Check handling of missing values and unsupported input types."""

    # missing identifiers are invalid, not an error
    assert cei.validate_cei(None) is False
    assert cei.validate_cei(float('nan')) is False

    # other unsupported types raise an error
    for bad in (115830024985.0, 12.34, True, b'115830024985', []):
        with pytest.raises(TypeError, match=r"must be str or int"):
            cei.validate_cei(bad)

    # missing values cannot be formatted
    with pytest.raises(TypeError, match=r"must be str or int"):
        cei.format_cei(None)


def test_cei_check_digit():
    """Test calculation of check digit for a CEI identifier."""

    # CEI identifiers have a single check digit
    assert cei.cei_check_digit('11.583.00249/85') == 5
    assert cei.cei_check_digit('115830024985') == 5

    # also works when only given the first 11 digits
    assert cei.cei_check_digit('11583002498') == 5

    # identifiers less than 11 digits produce an error
    with pytest.raises(ValueError, match=r".*11 digits.*"):
        cei.cei_check_digit('3002498')


def test_format_cei():
    """Test 00.000.00000/00 formatting of CEI."""

    assert cei.format_cei('115830024985') == '11.583.00249/85'

    # formatting pads integers that lost leading zeros
    assert cei.format_cei(115830024985) == '11.583.00249/85'

    # formatting does not validate; invalid CEI will be formatted
    assert cei.format_cei('115830024984') == '11.583.00249/84'


def test_pad_cei():
    """Test padding CEI with leading zeros."""

    assert cei.pad_cei('115830024985') == '115830024985'
    assert cei.pad_cei('15830024985')  == '015830024985'
    assert cei.pad_cei(15830024985)    == '015830024985'

    # can pad and validate in one step
    assert cei.pad_cei(115830024985, validate=True) == ('115830024985', True)
    assert cei.pad_cei(115830024984, validate=True) == ('115830024984', False)


def test_random_cei():
    """Test generation of random, valid CEI."""

    for i in range(10):
        assert cei.validate_cei(cei.random_cei()) is True
        assert cei.validate_cei(cei.random_cei(formatted=False)) is True

    assert isinstance(cei.random_cei(), str) is True
    assert isinstance(cei.random_cei(formatted=False), str) is True
