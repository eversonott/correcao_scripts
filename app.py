from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # Limite de 1MB

# Mapeamento de aulas e exercícios para os arquivos de teste
EXERCICIOS = {
    "aula1": {
        "soma": "testes/aula1/soma.py",
        "subtracao": "testes/aula1/subtracao.py"
    },
    "aula2": {
        "par_ou_impar": "testes/aula2/par_ou_impar.py",
        "maior_numero": "testes/aula2/maior_numero.py"
    }
}

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    codigo_enviado = ''
    saida = ""
    aula = request.form.get('aula') or ''
    exercicio = request.form.get('exercicio') or ''

    if request.method == 'POST':
        if 'arquivo' in request.files:
            arquivo = request.files['arquivo']
            if arquivo and arquivo.filename.endswith('.py'):
                codigo_enviado = arquivo.read().decode('utf-8')

        if not codigo_enviado:
            codigo_enviado = request.form.get('codigo', '')

        with open("main.py", "w") as f:
            f.write(codigo_enviado)

        try:
            caminho_teste = EXERCICIOS.get(aula, {}).get(exercicio)
            if not caminho_teste:
                saida = "❌ Aula ou exercício inválido."
            else:
                resultado = subprocess.run(
                    ["python", "-m", "pytest", caminho_teste, "--quiet"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    #text=True,
                    #capture_output=True,
                    timeout=5
                )
                #saida = resultado.stdout + '\n' + resultado.stderr
                if resultado.returncode == 0:
                    saida = "✅ Todos os testes passaram com sucesso!"
                else:
                    saida = "❌ Alguns testes falharam. Revise seu código e tente novamente."
        except Exception as e:
            saida = f"❌ Erro ao executar os testes: {e}"

        os.remove("main.py")

        return render_template("index.html", resultado=saida, codigo=codigo_enviado, aula=aula, exercicio=exercicio, exercicios=EXERCICIOS)

    return render_template("index.html", resultado=resultado, codigo=codigo_enviado, aula=aula, exercicio=exercicio, exercicios=EXERCICIOS)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

