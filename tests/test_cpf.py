
import pytest
from brazilnum import cpf


def test_validate_cpf():
    """Check validation of CPF identifiers."""

    # confirm a few complete, valid CPFs
    assert cpf.validate_cpf('96881134258') is True
    assert cpf.validate_cpf('77922198795') is True
    assert cpf.validate_cpf('28705385881') is True

    # check a few complete, invalid CPFs
    assert cpf.validate_cpf('96881134259') is False
    assert cpf.validate_cpf('77922198796') is False
    assert cpf.validate_cpf('28705385882') is False

    # formatted input is also fine
    assert cpf.validate_cpf('968.811.342-58') is True
    assert cpf.validate_cpf('327.861.067-97') is False

    # should also work by default without leading zeros
    assert cpf.validate_cpf('4193675866') is True
    assert cpf.validate_cpf('4193675866', autopad=False) is False

    # and when argument is an integer
    assert cpf.validate_cpf(96881134258) is True
    assert cpf.validate_cpf(4193675866) is True
    assert cpf.validate_cpf(96881134259) is False

    # identifiers longer than 11 digits are not valid
    assert cpf.validate_cpf('96881134258999') is False

    # zero and empty strings are not valid
    assert cpf.validate_cpf(0) is False
    assert cpf.validate_cpf('0') is False
    assert cpf.validate_cpf('') is False


def test_validate_cpf_bad_input():
    """Check handling of missing values and unsupported input types."""

    # missing identifiers are invalid, not an error
    assert cpf.validate_cpf(None) is False
    assert cpf.validate_cpf(float('nan')) is False

    # other unsupported types raise an error
    for bad in (96881134258.0, 12.34, True, b'96881134258', []):
        with pytest.raises(TypeError, match=r"must be str or int"):
            cpf.validate_cpf(bad)

    # missing values cannot be formatted or padded
    with pytest.raises(TypeError, match=r"must be str or int"):
        cpf.format_cpf(None)

    with pytest.raises(TypeError, match=r"must be str or int"):
        cpf.pad_cpf(None)


def test_cpf_check_digits():
    """Test calculation of check digits for a CPF identifier."""

    # CPF identifiers have two check digits
    assert cpf.cpf_check_digits('96881134258') == (5, 8)
    assert cpf.cpf_check_digits('04193675866') == (6, 6)

    # also works when only given the first 9 digits
    assert cpf.cpf_check_digits('968811342') == (5, 8)
    assert cpf.cpf_check_digits('041936758') == (6, 6)
    assert cpf.cpf_check_digits('041.936.758') == (6, 6)

    # identifiers less than 9 digits produce an error
    with pytest.raises(ValueError, match=r".*9 digits.*"):
        cpf.cpf_check_digits('93675866')


def test_format_cpf():
    """Test 000.000.000-00 formatting of CPF."""

    assert cpf.format_cpf('96881134258') == '968.811.342-58'
    assert cpf.format_cpf('04193675866') == '041.936.758-66'

    # formatting pads integers that lost leading zeros
    assert cpf.format_cpf(4193675866) == '041.936.758-66'

    # formatting does not validate; invalid CPFs will be formatted
    assert cpf.format_cpf('96881134259') == '968.811.342-59'


def test_pad_cpf():
    """Test padding CPF with leading zeros."""

    assert cpf.pad_cpf('96881134258') == '96881134258'
    assert cpf.pad_cpf('4193675866')  == '04193675866'
    assert cpf.pad_cpf(4193675866)    == '04193675866'

    # can pad and validate in one step
    assert cpf.pad_cpf(4193675866, validate=True) == ('04193675866', True)
    assert cpf.pad_cpf(4193675867, validate=True) == ('04193675867', False)


def test_random_cpf():
    """Test generation of random, valid CPF."""

    for i in range(10):
        assert cpf.validate_cpf(cpf.random_cpf()) is True
        assert cpf.validate_cpf(cpf.random_cpf(formatted=False)) is True

    assert isinstance(cpf.random_cpf(), str) is True
    assert isinstance(cpf.random_cpf(formatted=False), str) is True
