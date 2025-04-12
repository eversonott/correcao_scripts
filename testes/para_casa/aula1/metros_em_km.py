import subprocess

def test_metros_em_km():
    resultado = subprocess.run(["python", "main.py"], capture_output=True, text=True)
    saida = resultado.stdout
    assert any(valor in saida for valor in ["1.387", "1.39", "1.386"])
