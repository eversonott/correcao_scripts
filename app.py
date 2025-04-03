from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    codigo_enviado = ''

    if request.method == 'POST':
        codigo_enviado = request.form['codigo']

        # Salva o código enviado como main.py temporário
        with open("main.py", "w") as f:
            f.write(codigo_enviado)

        saida = ''

        # Executa os testes com pytest
        try:
            resultado = subprocess.run(
                ["pytest", "test_main.py", "--quiet"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5
            )
            # Simplificação para alunos
            if resultado.returncode == 0:
                saida = "✅ Todos os testes passaram com sucesso!\n\n" + saida
            else:
                saida = "❌ Alguns testes falharam. Revise seu código e tente novamente.\n\n" + saida
        except Exception as e:
            saida = f"Erro ao executar os testes: {e}"

        # Remove o arquivo main.py após os testes
        os.remove("main.py")

        return render_template("index.html", resultado=saida, codigo=codigo_enviado)

    return render_template("index.html", resultado=resultado, codigo=codigo_enviado)

if __name__ == '__main__':
    app.run(debug=True)

