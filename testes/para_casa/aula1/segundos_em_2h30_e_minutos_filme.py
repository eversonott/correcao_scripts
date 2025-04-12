import subprocess

def test_segundos_minutos():
    resultado = subprocess.run(["python", "main.py"], capture_output=True, text=True)
    saida = resultado.stdout
    assert "9000" in saida and "107" in saida
