
import pytest
from brazilnum import cep
from brazilnum.cep import CEP


def test_format_cep():
    """Test 00000-000 formatting of CEP."""

    # complete, 8-digit CEP
    assert cep.format_cep('13165000') == '13165-000'
    assert cep.format_cep(13165000) == '13165-000'

    # 7-digit input lost a leading zero
    assert cep.format_cep(1002010) == '01002-010'

    # 5-digit input is an old-style CEP without the suffix
    assert cep.format_cep(73080) == '73080-000'

    # 4-digit input is an old-style CEP missing a leading zero
    assert cep.format_cep('1310') == '01310-000'

    # existing formatting is ignored
    assert cep.format_cep('13165-000') == '13165-000'

    # other lengths are ambiguous and produce an error
    with pytest.raises(ValueError, match=r"Invalid CEP.*"):
        cep.format_cep('123456')

    with pytest.raises(ValueError, match=r"Invalid CEP.*"):
        cep.format_cep(131650000)

    # missing values and unsupported types cannot be formatted
    with pytest.raises(TypeError, match=r"must be str or int"):
        cep.format_cep(None)

    with pytest.raises(TypeError, match=r"must be str or int"):
        cep.format_cep([13165000])


def test_parse_cep():
    """Test parsing of CEP into geographic components."""

    assert cep.parse_cep('01255-080') == CEP(
        1255080, 0, 1, 12, 125, 1255, 80
    )

    # components can be returned as strings, preserving leading zeros
    assert cep.parse_cep('01255-080', numeric=False) == CEP(
        '01255-080', '0', '01', '012', '0125', '01255', '080'
    )

    # unformatted and integer input is also fine
    assert cep.parse_cep(13165000) == CEP(
        13165000, 1, 13, 131, 1316, 13165, 0
    )
    assert cep.parse_cep('13165000', numeric=False) == CEP(
        '13165-000', '1', '13', '131', '1316', '13165', '000'
    )
