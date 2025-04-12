import subprocess
import unicodedata

def normalizar(texto):
    return unicodedata.normalize('NFKD', texto.lower()).encode('ascii', 'ignore').decode('utf-8')

def test_mensagem_boas_vindas():
    resultado = subprocess.run(["python", "main.py"], capture_output=True, text=True)
    saida = normalizar(resultado.stdout)
    assert any(p in saida for p in ["ola", "bem vindo", "seja bem"])
