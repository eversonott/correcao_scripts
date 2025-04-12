import subprocess

def test_erro_aspas_maiusculas_parenteses():
    subprocess.run(["python", "main.py"], check=True)
