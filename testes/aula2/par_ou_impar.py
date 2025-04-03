from main import par_ou_impar

def test_par():
    assert par_ou_impar(4) == "par"

def test_impar():
    assert par_ou_impar(3) == "ímpar"

