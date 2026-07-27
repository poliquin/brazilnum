import pytest
from brazilnum import caepf
from brazilnum.caepf import CAEPF


def test_validate_caepf():
    """Check validation of CAEPF identifiers."""

    # confirm a few complete, valid CAEPFs
    assert caepf.validate_caepf("36010577900126") is True
    assert caepf.validate_caepf("85463857700279") is True
    assert caepf.validate_caepf("73111988500382") is True

    # check a few complete, invalid CAEPFs
    assert caepf.validate_caepf("28765204600377") is False
    assert caepf.validate_caepf("55369264000419") is False
    assert caepf.validate_caepf("78578133100599") is False

    # should also work by default without leading zeros
    assert caepf.validate_caepf("8996447200193") is True
    assert caepf.validate_caepf("8561811900294") is False

    # and when argument is an integer
    assert caepf.validate_caepf(5934308300443) is True
    assert caepf.validate_caepf(60251677400232) is True
    assert caepf.validate_caepf(270835600105) is True
    assert caepf.validate_caepf(70313415700251) is False
    assert caepf.validate_caepf(2125494200456) is False

    # zero and empty strings are not valid
    assert caepf.validate_caepf(0) is False
    assert caepf.validate_caepf("0") is False
    assert caepf.validate_caepf("") is False


def test_validate_caepf_bad_input():
    """Check handling of missing values and unsupported input types."""

    # None and NaN mark missing identifiers in a data stream, which can
    # happen when using the package correctly, so they are just invalid
    assert caepf.validate_caepf(None) is False
    assert caepf.validate_caepf(float("nan")) is False

    # any other unsupported type suggests an upstream problem with the
    # caller's data, so it raises an error instead of returning False
    for bad in (9237378720025.5, 12.34, True, b"72443315600158", []):
        with pytest.raises(TypeError, match=r"must be str or int"):
            caepf.validate_caepf(bad)

    # missing values cannot be formatted, padded, or parsed
    with pytest.raises(TypeError, match=r"must be str or int"):
        caepf.format_caepf(None)

    with pytest.raises(TypeError, match=r"must be str or int"):
        caepf.parse_caepf(float("nan"))

    with pytest.raises(TypeError, match=r"must be str or int"):
        caepf.caepf_check_digits(None)


def test_caepf_check_digits():
    """Test calculation of check digits for a CAEPF identifier."""

    # CAEPF identifiers have two check digits
    assert caepf.caepf_check_digits("36010577900126") == (2, 6)
    assert caepf.caepf_check_digits("85463857700279") == (7, 9)
    assert caepf.caepf_check_digits("73111988500382") == (8, 2)

    # also works when only given the first 12 digits
    assert caepf.caepf_check_digits("059343083004") == (4, 3)
    assert caepf.caepf_check_digits("602516774002") == (3, 2)
    assert caepf.caepf_check_digits(801175089001) == (1, 6)

    # identifiers less than 12 characters produce an error
    with pytest.raises(ValueError, match=r".*12 characters.*"):
        caepf.caepf_check_digits("50001")


def test_caepf_from_cpf_root():
    """Test construction of full CAEPF from the cpf root CAEPF."""

    assert (
        caepf.caepf_from_cpf_root("752352495", establishment="001") == "75235249500165"
    )

    # can also return formatted identifiers
    assert (
        caepf.caepf_from_cpf_root("752352495", establishment="001", formatted=True)
        == "752.352.495/001-65"
    )


def test_format_caepf():
    """Test 000.000.000/000-00 formatting of CAEPF."""

    # confirm a few complete, valid CAEPFs
    assert caepf.format_caepf("36010577900126") == "360.105.779/001-26"
    assert caepf.format_caepf("85463857700279") == "854.638.577/002-79"

    # formatting does not validate; invalid CAEPF will be formatted
    assert caepf.format_caepf("28765204600377") == "287.652.046/003-77"

    # can format integers
    assert caepf.format_caepf(5934308300443) == "059.343.083/004-43"


def test_pad_caepf():
    """Test padding CAEPF with leading zeros."""

    assert caepf.pad_caepf("00196283200299") == "00196283200299"
    assert caepf.pad_caepf("196283200299") == "00196283200299"
    assert caepf.pad_caepf(196283200299) == "00196283200299"

    assert caepf.pad_caepf("11277555000100") == "11277555000100"
    assert caepf.pad_caepf(11277555000100) == "11277555000100"

    # padding does not validate; invalid CAEPF will be padded OK
    assert caepf.pad_caepf("07619496400115") == "07619496400115"
    assert caepf.pad_caepf("7619496400115") == "07619496400115"
    assert caepf.pad_caepf(7619496400115) == "07619496400115"

    # can pad and validate in one step
    assert caepf.pad_caepf(196283200299, validate=True) == ("00196283200299", True)
    assert caepf.pad_caepf(7619496400115, validate=True) == ("07619496400115", False)


def test_parse_caepf():
    """Test parsing of CAEPF into components."""

    assert caepf.parse_caepf("00196283200299") == CAEPF(
        "001.962.832/002-99", "001.962.832", "002", "99", True
    )
    assert caepf.parse_caepf("00196283200299", formatted=False) == CAEPF(
        196283200299, 1962832, 2, (9, 9), True
    )

    # when CAEPF is invalid, function does not "fix" the check digits
    assert caepf.parse_caepf("07619496400115") == CAEPF(
        "076.194.964/001-15", "076.194.964", "001", "15", False
    )
    assert caepf.parse_caepf("07619496400115", formatted=False) == CAEPF(
        7619496400115, 76194964, 1, (1, 5), False
    )


def test_random_caepf():
    """Test generation of random, valid CAEPF."""

    for i in range(10):
        assert caepf.validate_caepf(caepf.random_caepf()) is True
        assert caepf.validate_caepf(caepf.random_caepf(formatted=True)) is True
        assert caepf.validate_caepf(caepf.random_caepf(formatted=False)) is True

    assert isinstance(caepf.random_caepf(), str) is True
    assert isinstance(caepf.random_caepf(formatted=False), str) is True
