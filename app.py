from flask import Flask, render_template, request
from markupsafe import Markup
import subprocess
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # Limite de 1MB

# Mapeamento de aulas e exercícios para os arquivos de teste
EXERCICIOS = {
    "em_aula": {
        "aula1": {
            "microdesafio_1": "testes/em_aula/aula1/microdesafio_1.py",
            "microdesafio_2": "testes/em_aula/aula1/microdesafio_2.py",
            "calculadora_boas_vindas": "testes/em_aula/aula1/calculadora_boas_vindas.py"
        }
    },
    "para_casa": {
        "aula1": {
            "erro_aspas_maiusculas_parenteses": "testes/para_casa/aula1/erro_aspas_maiusculas_parenteses.py",
            "print_com_soma": "testes/para_casa/aula1/print_com_soma.py",
            "variavel_mensagem": "testes/para_casa/aula1/variavel_mensagem.py",
            "operadores_sinais": "testes/para_casa/aula1/operadores_sinais.py",
            "segundos_em_2h30_e_minutos_filme": "testes/para_casa/aula1/segundos_em_2h30_e_minutos_filme.py",
            "metros_em_km": "testes/para_casa/aula1/metros_em_km.py",
            "tempo_de_tela": "testes/para_casa/aula1/tempo_de_tela.py",
            "mensagem_boas_vindas": "testes/para_casa/aula1/mensagem_boas_vindas.py",
            "soma_media_decimais": "testes/para_casa/aula1/soma_media_decimais.py",
            "desafio_criativo": "testes/para_casa/aula1/desafio_criativo.py"
        }
    }
}


def carregar_enunciado(tipo, aula, exercicio):
    raiz = os.path.dirname(__file__)
    caminho = os.path.join(raiz, "templates", "enunciados", tipo, aula, f"{exercicio}.html")
    if os.path.exists(caminho):
        with open(caminho, encoding='utf-8') as f:
            return Markup(f.read())
    return ""


@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    codigo_enviado = ''
    saida = ""
    tipo = request.form.get('tipo') or ''
    aula = request.form.get('aula') or ''
    exercicio = request.form.get('exercicio') or ''
    enunciado_html = carregar_enunciado(tipo, aula, exercicio) if tipo and aula and exercicio else ""

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
            caminho_teste = EXERCICIOS.get(tipo, {}).get(aula, {}).get(exercicio)
            if not caminho_teste:
                saida = "❌ Aula ou exercício inválido."
            else:
                resultado = subprocess.run(
                    #["python", "-m", "pytest", caminho_teste, "--quiet"],
                    ["python", "-m", "pytest", caminho_teste],
                    #stdout=subprocess.DEVNULL,
                    #stderr=subprocess.DEVNULL,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                print(resultado.stdout)
                print(resultado.stderr)
                if resultado.returncode == 0:
                    saida = "✅ Todos os testes passaram com sucesso!"
                else:
                    saida = "❌ Alguns testes falharam. Revise seu código e tente novamente."
        except Exception as e:
            saida = f"❌ Erro ao executar os testes: {e}"

        os.remove("main.py")

        return render_template("index.html", resultado=saida, codigo=codigo_enviado,
                               aula=aula, exercicio=exercicio,
                               exercicios=EXERCICIOS, enunciado_html=enunciado_html, tipo=tipo)

    return render_template("index.html", resultado=resultado, codigo=codigo_enviado,
                           aula=aula, exercicio=exercicio,
                           exercicios=EXERCICIOS, enunciado_html=enunciado_html, tipo=tipo)

@app.route('/enunciado/<tipo>/<aula>/<exercicio>')
def enunciado(tipo, aula, exercicio):
    return carregar_enunciado(tipo, aula, exercicio)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)

