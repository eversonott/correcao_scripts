from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # Limite de 1MB

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    codigo_enviado = ''
    saida = ""

    if request.method == 'POST':
        # Se o aluno enviou um arquivo .py, usamos ele
        if 'arquivo' in request.files:
            arquivo = request.files['arquivo']
            if arquivo and arquivo.filename.endswith('.py'):
                codigo_enviado = arquivo.read().decode('utf-8')

        # Caso contrário, usamos o conteúdo do textarea
        if not codigo_enviado:
            codigo_enviado = request.form['codigo']

        # Salva o código como main.py
        with open("main.py", "w") as f:
            f.write(codigo_enviado)

        try:
            resultado = subprocess.run(
                ["pytest", "test_main.py", "--quiet"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5
            )

            if resultado.returncode == 0:
                saida = "✅ Todos os testes passaram com sucesso!"
            else:
                saida = "❌ Alguns testes falharam. Revise seu código e tente novamente."

        except Exception as e:
            saida = f"❌ Erro ao executar os testes: {e}"

        os.remove("main.py")

        return render_template("index.html", resultado=saida, codigo=codigo_enviado)

    return render_template("index.html", resultado=resultado, codigo=codigo_enviado)

if __name__ == '__main__':
    app.run(debug=True)

