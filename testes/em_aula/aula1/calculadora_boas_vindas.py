import subprocess

def test_calculadora_boas_vindas():
    resultado = subprocess.run(["python", "main.py"], capture_output=True, text=True)
    saida = resultado.stdout.strip().lower()
    assert "nome" in saida
    assert "idade" in saida
    assert "%" in saida
    assert "tempo" in saida

