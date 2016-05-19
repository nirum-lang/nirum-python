from nirum.serialize import serialize_boxed_type, serialize_record_type


def test_serialize_boxed_type(fx_offset):
    assert serialize_boxed_type(fx_offset) == fx_offset.value


def test_serialize_record_type(fx_point):
    assert serialize_record_type(fx_point) == {'_type': 'point', 'x': 3.14,
                                               'top': 1.592}
