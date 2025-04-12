import ast

def test_operadores_sinais():
    with open("main.py", encoding="utf-8") as f:
        arvore = ast.parse(f.read())

    operadores_usados = set()

    class Visitador(ast.NodeVisitor):
        def visit_BinOp(self, node):
            op = type(node.op)
            operadores_usados.add(op)
            self.generic_visit(node)

    Visitador().visit(arvore)

    assert ast.Add in operadores_usados
    assert ast.Sub in operadores_usados
    assert ast.Mult in operadores_usados
    assert ast.Div in operadores_usados
