import subprocess

def test_saida_mensagem():
    resultado = subprocess.run(
        ["python", "main.py"],
        capture_output=True,
        text=True
    )
    assert resultado.stdout.strip() == "A vida é bela!"

