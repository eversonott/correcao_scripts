import subprocess
import unicodedata

def normalizar(texto):
    return unicodedata.normalize('NFKD', texto.lower()).encode('ascii', 'ignore').decode('utf-8')

def test_microdesafio_2():
    resultado = subprocess.run(["python", "main.py"], capture_output=True, text=True)
    saida = normalizar(resultado.stdout.strip())
    assert any(padrao in saida for padrao in ["ola", "bem vindo", "seja bem", "oi", "boa tarde", "boa noite", "bom dia"])

