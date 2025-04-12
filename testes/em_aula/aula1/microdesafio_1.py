import subprocess

def test_microdesafio_1():
    resultado = subprocess.run(["python", "main.py"], capture_output=True, text=True)
    saida = resultado.stdout.strip()
    assert "Nome: Ana" in saida
    assert "Idade: 18" in saida

