import subprocess

def test_print_com_soma():
    resultado = subprocess.run(["python", "main.py"], capture_output=True, text=True)
    assert "9" in resultado.stdout
