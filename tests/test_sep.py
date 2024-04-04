from sep.rectangular import RectangleSeparator

sep = RectangleSeparator(1, 1, 1, 0.05)
br = sep._breaks


def test_len():
    assert len(br) == len(sep), "Should be equal count of sides"


def test_center_size():
    for i in range(len(sep)):
        assert len(br[i]) == 3, "Should be square"
