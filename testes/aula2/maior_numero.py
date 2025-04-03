from main import maior_numero

def test_maior_numero():
    assert maior_numero(10, 5) == 10
    assert maior_numero(2, 8) == 8
    assert maior_numero(7, 7) == 7

