import ast

with open('app_legacy.py', 'r', encoding='utf-8') as f:
    tree = ast.parse(f.read())

for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        is_route = False
        decorators = []
        for d in node.decorator_list:
            if isinstance(d, ast.Name):
                decorators.append(d.id)
            elif isinstance(d, ast.Call):
                if isinstance(d.func, ast.Attribute):
                    if d.func.attr == 'route':
                        is_route = True
                    decorators.append(d.func.attr)
                elif isinstance(d.func, ast.Name):
                    decorators.append(d.func.id)
        if is_route:
            print(f"{node.name}: {decorators}")
