from flatten import flatten


def test_flatten():
    assert flatten([]) == []
    assert flatten([1]) == [1]
    assert flatten([[]]) == []
    assert flatten([[1]]) == [1]
    assert flatten([[1, [2, 3], [[4, 5], 6], [7, 8]]]) == [1, 2, 3, 4, 5, 6, 7, 8]
