from main import soma

def test_soma_basica():
    assert soma(2, 3) == 5

def test_soma_zeros():
    assert soma(0, 0) == 0

def test_soma_negativos():
    assert soma(-1, -2) == -3

