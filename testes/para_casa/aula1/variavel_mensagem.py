import subprocess
import unicodedata

def normalizar(texto):
    return unicodedata.normalize('NFKD', texto.lower()).encode('ascii', 'ignore').decode('utf-8')

def test_variavel_mensagem():
    resultado = subprocess.run(["python", "main.py"], capture_output=True, text=True)
    saida = normalizar(resultado.stdout)
    assert "python" in saida and "divertido" in saida
