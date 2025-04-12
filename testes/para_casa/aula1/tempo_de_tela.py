import ast

def test_tempo_de_tela():
    with open("main.py", encoding="utf-8") as f:
        arvore = ast.parse(f.read())

    valores_esperados = {7, 60}
    usados = set()

    class Visitador(ast.NodeVisitor):
        def visit_BinOp(self, node):
            if isinstance(node.op, ast.Mult):
                for lado in [node.left, node.right]:
                    if isinstance(lado, ast.Constant) and isinstance(lado.value, (int, float)):
                        usados.add(int(lado.value))
            self.generic_visit(node)

    Visitador().visit(arvore)

    assert 7 in usados and 60 in usados
