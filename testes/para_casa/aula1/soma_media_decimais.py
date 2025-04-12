import ast

def test_soma_media_decimais():
    with open("main.py", encoding="utf-8") as f:
        arvore = ast.parse(f.read())

    floats_encontrados = 0
    soma_encontrada = False
    media_por_3 = False

    class Visitador(ast.NodeVisitor):
        def visit_Constant(self, node):
            nonlocal floats_encontrados
            if isinstance(node.value, float):
                floats_encontrados += 1
        def visit_BinOp(self, node):
            nonlocal soma_encontrada, media_por_3
            if isinstance(node.op, ast.Add):
                soma_encontrada = True
            if isinstance(node.op, ast.Div):
                if isinstance(node.right, ast.Constant) and node.right.value == 3:
                    media_por_3 = True
            self.generic_visit(node)

    Visitador().visit(arvore)

    assert floats_encontrados >= 3
    assert soma_encontrada
    assert media_por_3
