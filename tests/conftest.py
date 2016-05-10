from pytest import fixture

class offset:

    def __init__(self, value: float) -> None:
        self.value = value

    def __eq__(self, other) -> bool:
        return (isinstance(other, offset) and self.value == other.value)

    def __hash__(self) -> int:
        return hash(self.value)

@fixture
def fx_boxed_type():
    return offset


@fixture
def fx_offset():
    return offset(1.2)
